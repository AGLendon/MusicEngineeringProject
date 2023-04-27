from multiprocessing import Process,Pipe
import time 
import rtmidi
import re

midi_in = rtmidi.MidiIn()

#midi_in.get_ports() # See possible devices to use, that are connected
midi_in.open_port(2) #bajs port
#ports = midi_in.get_ports() 
#ports_dict = {k: v for (v,k) in enumerate(ports)}
#midi_in.open_port(ports_dict["loopMIDI Port 0"])


record = False;     # Set record catch off
midi_chan = 0;      # 0-15 -> 1-16
output = []
dur = [0]*127       #note duration memory
t_end = time.time()*2

while midi_in.is_port_open():  # Sucessfully connected if true
    # add sleep timer
    
    #Wait for first key input
    if not midi_in.get_message() and not record:            
            t_end = time.time() + 5 #Define first listening time
            print(t_end)
            
    elif midi_in.get_message():            
        record = True;  # Set record catch on
        print("rec active...")
        
    #need some conditional to end any held notes or extend t_end (prob just end them)
        while time.time() < t_end: 
            msg_and_dt = midi_in.get_message()
            #Process the message        ([cmd, pitch, vel], dt)
            if msg_and_dt:
                (msg, dt) = msg_and_dt      #Split up message and delay time
                command = hex(msg[0])   #Convert into hex
                print(msg_and_dt)
                if command == hex(int(0x90)+midi_chan): #0x90 note on midi chan 1
                    dur[msg[1]] = 0
                    output.append((msg[1],dt,dur))
                elif command == hex(int(0x80)+midi_chan):
                    lst_t = list(output[len(output)-1])
                    lst_t[2] = dur[msg[1]]+dt
                    output[len(output)-1] = tuple(lst_t)                
                
                else: #Ignore other midi messages but keep the duration stored
                    dur[msg[1]] = dur[msg[1]]+dt                
            else:
                time.sleep(0.001)
    elif time.time() > t_end and record: #ToDo
        record = False;
        print("rec stop...")
        print(output)
        #input_notes = ([(26, 0, dur), (86, stp, dur)...])
        #Export the note data
        #def f(child_conn):
         #   msg = (3,4,5)
          #  child_conn.send(msg)
           # child_conn.close()

           
