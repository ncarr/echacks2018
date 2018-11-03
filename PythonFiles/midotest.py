# Library imports
import time
import mido
import json

# Get the midi file
songFile = mido.MidiFile('mad_world.mid')

# For reference = Bb is note 46, High Bb is 58, Middle C is 60

# Load the fingerings file for the baritone
with open('fingerings.json') as json_file:
    fingerings = json.load(json_file)

# Iterate over messages in it
for msg in songFile:
    if msg.type == 'note_on' and msg.velocity == 0:
        time.sleep(msg.time)
        print(fingerings[str(msg.note)])
