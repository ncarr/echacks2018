# Library imports
import time
import mido

# Get the midi file
songFile = mido.MidiFile('mad_world.mid')

# For reference = Bb is note 46, High Bb is 58, Middle C is 60

# Iterate over messages in it
for msg in songFile:
    time.sleep(msg.time)
    print(msg)
