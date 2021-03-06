# Library imports
import mido
import json
import asyncio
import websockets

sockets = set()
valves = ''
volume = 0
songFile = mido.MidiFile('Music/Birdland.mid')
midiJSON = None

def readMidi(fileName):
    global songFile
    global midiJSON
    # Get the midi file
    songFile = mido.MidiFile('Music/' + fileName)

    # Convert the midi file into a JSON that we can send to the Vue server via socket
    midiList = []
    for msg in songFile:
        if msg.type == 'note_on':
            noteTime = round(msg.time*4)/4
            if msg.velocity == 0:
                midiList.append({
                    'note': msg.note,
                    # Round note to nearest .25 because musescore is odd
                    'time': noteTime,
                })
            elif msg.velocity == 80 and noteTime:
                midiList.append({
                    'note': 00,
                    'time': noteTime
                })
    # Convert it to JSON
    midiJSON = json.dumps(midiList)
    print(midiJSON)

# For reference = Bb is note 46, High Bb is 58, Middle C is 60
# Load the fingerings file for the baritone
with open('fingerings.json') as json_file:
    fingerings = json.load(json_file)

songActive = False
currentNoteAccuracy = []
songAccuracy = []
expected = ''


async def iterate_over_file(midi_file):
    # Iterate over messages in the song
    global songActive
    songActive = True
    for message in midi_file:
        if message.type == 'note_on':
            noteTime = round(message.time*4)/4
            if message.velocity == 0:
                # Set the new note
                global expected
                expected = fingerings[str(message.note)]
                await asyncio.sleep(message.time)
                try:
                    # Calculate the accuracy for the previous note
                    accuracy_percentage = sum(currentNoteAccuracy) / len(currentNoteAccuracy)
                    # Send message and accuracy to clients
                    await broadcast(json.dumps({'type': 'note', 'accuracy': accuracy_percentage, 'note': message.note, 'time': noteTime }))
                    # Add it to the list of the whole song
                    songAccuracy.append(accuracy_percentage)
                    currentNoteAccuracy.clear()
                except ZeroDivisionError:
                    await broadcast(json.dumps({'type': 'note', 'note': message.note, 'time': noteTime}))
            elif message.velocity == 80:
                await asyncio.sleep(message.time)
                if noteTime != 0:
                    await broadcast(json.dumps({'type': 'note', 'note': 0, 'time': noteTime}))
                currentNoteAccuracy.clear()
    songActive = False
    print(songAccuracy)


async def counter(websocket, path):
    sockets.add(websocket)
    try:
        async for message in websocket:
            if message.startswith('json'):
                readMidi(message[5:])
                await websocket.send(midiJSON)
            elif message == 'start':
                asyncio.get_event_loop().create_task(iterate_over_file(songFile))
            else:
                global valves
                print("message " + message)
                valves = message[0:5]
                if songActive:
                    print("Current: " + valves)
                    print("Expected: " + expected)
                    # Log whether the player hit the note
                    if valves == expected:
                        currentNoteAccuracy.append(1)
                    else:
                        currentNoteAccuracy.append(0)
                await broadcast(message)
    except Exception as e:
        print(e)

async def broadcast(message):
    if len(sockets) != 0:
        await asyncio.wait([sendMessage(socket, message) for socket in sockets])

async def sendMessage(socket, message):
    try:
        await socket.send(message)
    except websockets.ConnectionClosed:
        sockets.discard(socket)


asyncio.get_event_loop().run_until_complete(websockets.serve(counter, '0.0.0.0', 6789))
asyncio.get_event_loop().run_forever()
