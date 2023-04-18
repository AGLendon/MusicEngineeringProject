#pip install python-rtmidi
#pip install MIDIFile

import time
import rtmidi
import pretty_midi #handling midi files
import mido #loggin midi messages
import MIDIFIle

midi_data = pretty_midi.PrettyMIDI('RNN_test_5.mid');
chroma = midi_data.get_chroma(fs=100, times=None, pedal_threshold=64);

noteStart = midi_data.get_onsets();

midi_file = MIDI.MIDIFile.__init__(self, filename)



MIDI.MIDIFile.parse('RNN_test_5.mid');
MIDI.Track.__init__(self, data, containsTiming = True)
