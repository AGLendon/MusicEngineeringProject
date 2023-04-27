from multiprocessing import Process,Pipe
import time 
import rtmidi
import re

def f(child_conn):            #not functional? not sure how this works in a script like this, probalby need to look into the queuing functionality
    midi_in = rtmidi.MidiIn()
    ports = midi_in.get_ports() 
    ports_dict = {k: v for (v,k) in enumerate(ports)}
    name_Keyword = "Beatstep" #Change this to the name or part of the name of your midi device e.g "Arturia" or "Beatstep" would also work here.
    #Was having issues with the port number being attached to the name

    for k  in ports_dict:
        if name_Keyword in k:         
            port_name = k
            print(port_name)
            break
        
    midi_in.open_port(ports_dict[k])
    #midi_in.open_port(2)

    record = False;     # Set record catch off
    hold = False;       # Set hold note catch off
    midi_chan = 0;      # 0-15 -> 1-16 make sure you are playing on correct midi channel
    output = []         # Init output
    dur = [0]*127;      # Init duration list
    sleep_st = time.time(); # Init sleep time start reference
    sleep_t = 0;            # Init sleep timer to 0
    t_end = time.time()*2;  # Init 'recording' timer end time (will be set to 5s with no input on startup)
    count = 0
    t_beforeSleep = 20
    stp = 0.5
    dr = 0.5
    

    while midi_in.is_port_open() and sleep_t <t_beforeSleep:
        while time.time() < t_end and sleep_t < t_beforeSleep: 
                msg_and_dt = midi_in.get_message()
                #Process the message        ([cmd, pitch, vel], dt)
                if msg_and_dt:
                    #print(sleep_t)
                    sleep_st = time.time()
                    record = True
                    print(msg_and_dt)
                    (msg, dt) = msg_and_dt      #Split up message and delay time
                    command = hex(msg[0])       #Convert into hex
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
                        else:
                            output = [(26, 0, dr), (26, stp, dr), (26, stp, dr), (46, stp, dr), (26, stp, dr)]
                        
                        hold = True #Set hold note catch on
                        output.append((msg[1],dur_last+dt,dur))

                        
                    elif command == hex(int(0x80)+midi_chan) and hold and output: #force monophonic keyboard with hold bool
                        if msg[1] == output[len(output)-1][0]:
                            #print(msg_and_dt)
                            lst_t = list(output[len(output)-1])
                            lst_t[2] = dur[msg[1]]+dt
                            #print('duration',lst_t[2],dur[msg[1]])
                            output[len(output)-1] = tuple(lst_t)
                            dur[msg[1]] = 0
                            hold = False
                        
                    else: #Ignore other midi messages but keep the duration stored. This may be useful for polyphony
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
            if sleep_t <= t_beforeSleep and not hold:
                
                print('sent') #send output here
                child_conn.send(output)
                #child_conn.close()
                #def f(child_conn):            #not functional not sure how this works best
                #    child_conn.send(output)
                #    child_conn.close()
                
                output = []
                record = False
                t_end = time.time() + 5
                
            elif hold:
            #if a note is being held - either extend time or force the output
                t_end = time.time() + 0.1   #extend time to wait for note off
                #print('time extended-held note:',msg[1],sum(dur),'seconds') 
                
            elif sleep_t > t_beforeSleep:
                #print('sleepy time')
                break
    #print('thanks for playing')
    midi_in.close_port()
    time.sleep(1)