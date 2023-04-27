import time 
import rtmidi
import re

midi_in = rtmidi.MidiIn()

midi_in.open_port(2)

record = False;     # Set record catch off
midi_chan = 0;      # 0-15 -> 1-16
output = []
dur = [0]*127
t_end = time.time()*2

while midi_in.is_port_open():
    while time.time() < t_end: 
            msg_and_dt = midi_in.get_message()
            #Process the message        ([cmd, pitch, vel], dt)
            if msg_and_dt:
                #print(msg_and_dt)
                (msg, dt) = msg_and_dt      #Split up message and delay time
                command = hex(msg[0])   #Convert into hex
                #print(msg_and_dt)
                if command == hex(int(0x90)+midi_chan): #0x90 note on midi chan 1
                    dur[msg[1]] = 0
                    output.append((msg[1],dt,dur))
                elif command == hex(int(0x80)+midi_chan):
                    lst_t = list(output[len(output)-1])
                    lst_t[2] = dur[msg[1]]+dt
                    output[len(output)-1] = tuple(lst_t)
                    
                    if len(output)>4:
                        output = []
                    
                
                else: #Ignore other midi messages but keep the duration stored
                    dur[msg[1]] = float(dur[msg[1]])+dt
                    
            else:
                time.sleep(0.001)
