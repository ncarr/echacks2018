# Library imports
import time
import mido
import json
import asyncio
import websockets

# Get the midi file
songFile = mido.MidiFile('mad_world.mid')
sockets = set()
valves = ''

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
    for msg in midi_file:
        if msg.type == 'note_on' and msg.velocity == 0:
            # Set the new note
            global expected
            expected = fingerings[str(msg.note)]
            await asyncio.sleep(msg.time)
            # Calculate the accuracy for the last note
            try:
                accuracy_percentage = sum(currentNoteAccuracy) / len(currentNoteAccuracy)
                songAccuracy.append(accuracy_percentage)
                currentNoteAccuracy.clear()
            except ZeroDivisionError:
                pass
    songActive = False
    print(songAccuracy)


async def counter(websocket, path):
    sockets.add(websocket)
    try:
        async for message in websocket:
            global valves
            valves = message
            print("Current: " + valves)
            print("Expected: " + expected)
            print("Active: " + str(songActive))
            if songActive:
                if valves == expected:
                    currentNoteAccuracy.append(1)
                else:
                    currentNoteAccuracy.append(0)
    except Exception as e:
        print(e)


asyncio.get_event_loop().run_until_complete(
    websockets.serve(counter, '0.0.0.0', 6789))
asyncio.get_event_loop().run_until_complete(iterate_over_file(songFile))
asyncio.get_event_loop().run_forever()
