import time
import rtmidi
import pretty_midi #handling midi files
import mido #loggin midi messages

out = rtmidi.MidiOut()
ports = out.get_ports()
ports_dict = {k: v for (v,k) in enumerate(out.get_ports())}
out.open_port(ports_dict["loopMIDI Port 1"])
# out.open_port(ports_dict["DEVICE_NAME"])
# out.open_port(0)

with out:
    note_on = [0x94, 48, 100]
    note_off = [0x84, 48, 0]
    out.send_message(note_on)
    time.sleep(1.0)
    out.send_message(note_off)
    time.sleep(0.1)
del out


midi_data = pretty_midi.PrettyMIDI('..\Users\lendo\Documents\GitHub\MusicEngineeringProject\Alex\')
print(midi_data.estimate_tempo())
midi_proll = midi_data.get_piano_roll(fs=100, times=None, pedal_threshold=64);




