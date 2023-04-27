import time 
import rtmidi

midi_in = rtmidi.MidiIn()
ports = midi_in.get_ports() 
ports_dict = {k: v for (v,k) in enumerate(ports)}
print(ports_dict)
midi_in.open_port(ports_dict.get("loopMIDI Port 0 0"))
#midi_in.open_port(1)
