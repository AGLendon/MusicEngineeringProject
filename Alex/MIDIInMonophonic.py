import time 
import rtmidi
import re

midi_in = rtmidi.MidiIn()
ports = midi_in.get_ports() 
ports_dict = {k: v for (v,k) in enumerate(ports)}
name_Keyword = "Arturia BeatStep Pro" #Change this to the name or part of the name of your midi device e.g "Arturia" or "Beatstep" would also work here.
#Was having issues with the port number being attached to the name

for k  in ports_dict:
    if name_Keyword in k:         
        port_name = k
        print(port_name)
        break
    
midi_in.open_port(ports_dict[k])
#midi_in.open_port(2)

record = False;      # Set record catch off
hold = False;       # Set hold note catch off
midi_chan = 0;      # 0-15 -> 1-16
output = []  # Init output with some size to remove later
dur = [0]*127
sleep_st = time.time()
sleep_t = 0
t_end = time.time()*2
count = 0

while midi_in.is_port_open() and sleep_t <10:
    while time.time() < t_end and sleep_t < 10: 
            msg_and_dt = midi_in.get_message()
            #Process the message        ([cmd, pitch, vel], dt)
            if msg_and_dt:
                #print(sleep_t)
                sleep_st = time.time()
                record = True
                #print(msg_and_dt)
                (msg, dt) = msg_and_dt      #Split up message and delay time
                command = hex(msg[0])   #Convert into hex
                #print(msg_and_dt)
                if command == hex(int(0x90)+midi_chan) and not hold: #0x90 note on midi chan 1
                    #print('note on')
                    dur[msg[1]] = 0
                    dur_last = 0
                    if output:
                        dur_last = output[len(output)-1][2]
                        if type(dur_last)==list:
                            print('message breaking1',msg[0])
                            break
                    hold = True #Set hold note catch on
                    output.append((msg[1],dur_last+dt,dur))

                    
                elif command == hex(int(0x80)+midi_chan) and hold and output: #force monophonic keyboard with hold bool
                    if msg[1] == output[len(output)-1][0]:
                        #print(msg_and_dt)
                        lst_t = list(output[len(output)-1])
                        lst_t[2] = dur[msg[1]]+dt
                        print('duration',lst_t[2],dur[msg[1]])
                        output[len(output)-1] = tuple(lst_t)
                        dur[msg[1]] = 0
                        hold = False

                    
                    
                else: #Ignore other midi messages but keep the duration stored
                    dur[msg[1]]= dur[msg[1]]+dt
                    if not (type(dur[msg[1]])== int or type(dur[msg[1]])== float):
                            print('message breaking2',msg[0])
                            break
                    
                    
                    
                    
            
            else:                
                if record == False:
                    t_end = time.time() + 5
                    sleep_t = 0
                
                sleep_t = time.time() - sleep_st
                time.sleep(0.001)
    else:#if sleep_t < 10:
        if sleep_t <= 10 and not hold:
            
            print(output) #send output here
            output = []
            record = False
            t_end = time.time() + 5
        elif hold:
        #if a note is being held - either extend time or force the output
            t_end = time.time() + 0.1   #extend time to wait for note off
            print('time extended-held note:',msg[1],sum(dur),'seconds')
            
            count += 1
            #if count ==30:
                #break
            
        elif sleep_t > 10:
            print('sleepy time')
            break
print('thanks for playing')
midi_in.close_port()
time.sleep(1)
