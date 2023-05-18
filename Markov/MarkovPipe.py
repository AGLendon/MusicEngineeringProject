#!/usr/bin/env python
# coding: utf-8

# In[17]:


def make_markov_model(recorded_stream, n_gram):
    markov_model = {}
    for i in range(len(recorded_stream)-(n_gram)-1):
        curr_state, next_state = [],[]
        for j in range(n_gram):
            curr_state.append(recorded_stream[i+j])            
            ref = i+j
            next_state.append(recorded_stream[ref+2])
        curr_state = tuple(curr_state)
        next_state = tuple(next_state)
        if curr_state not in markov_model:
            markov_model[curr_state] = {}
            markov_model[curr_state][next_state] = 1
        else:
            if next_state in markov_model[curr_state]:
                markov_model[curr_state][next_state] += 1
            else:
                markov_model[curr_state][next_state] = 1
    
    #Calculating transition probabilities
    for curr_state, transition in markov_model.items():
        total = sum(transition.values())
        for state, count in transition.items():
            markov_model[curr_state][state] = count/total
    
    return markov_model  


# In[3]:


def MidiIn(n, p_input): 
    import rtmidi
    import time
    #Setup midi port
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
    
    nNotes = 0         
    
    while midi_in.is_port_open() and sleep_t <10 :
        while sleep_t < 10 and nNotes < n+1:            
            msg_and_dt = midi_in.get_message()
            #Process the message        ([cmd, pitch, vel], dt)
            if msg_and_dt:
                sleep_st = time.time()
                record = True
                
                (msg, dt) = msg_and_dt      #Split up message and delay time
                command = hex(msg[0])   #Convert into hex
                
                if command == hex(int(0x90)+midi_chan) and not hold: #0x90 note on midi chan 1
                    dur[msg[1]] = 0
                    dur_last = 0
                    
                    if output:
                        dur_last = output[len(output)-1][2]
                        if type(dur_last)==list:
                            print('message breaking1',msg[0])
                            break
                    hold = True #Set hold note catch on
                    output.append([msg[1],dur_last+dt,dur])#((msg[1],dur_last+dt,dur))

                    
                elif command == hex(int(0x80)+midi_chan) and hold and output: #force monophonic keyboard with hold bool
                    if msg[1] == output[len(output)-1][0]:
                        lst_t = list(output[len(output)-1])    #list with [pitch, step, dur]
                        lst_t[2] = dur[msg[1]]+dt              #update the duration
                        #print('duration',lst_t[2],dur[msg[1]]) # Note duration check                                                       
                        
                        #Add individual note data to queue
                        p_input.send(lst_t) 
                        print(lst_t)
                        output[len(output)-1] = tuple(lst_t) 
                        
                        #Reset variable
                        dur[msg[1]] = 0
                        hold = False
                        nNotes += 1
                        print(nNotes)
                    
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
                #Output 5 notes list of tuples
                #q5.put(output)               
                print(output) #send output here
                #Reset variables
                nNotes = 0
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
    p_input.send('DONE')


# In[2]:


def setup():
    import time 
    import rtmidi
    import re
    import multiprocessing
    import mpire
    import time
    


# In[ ]:


#def inst():
    #pip install mpire
    #pip install rtmidi


# In[4]:


def reader_proc(pipe):
    ## Read from the pipe; this will be spawned as a separate Process
    p_output, p_input = pipe
    p_input.close()    # We are only reading
    while True:
        msg = p_output.recv()    # Read from the output pipe and do nothing
        if msg=='DONE':
            break

def main():
    import time 
    import rtmidi
    import re
    import mpire
    import time
    import multiprocessing as mp
    from multiprocessing import Process, Pipe
    
    setup()
    n=5
    p_output, p_input = mp.Pipe()  # writer() writes to p_input from _this_ process
    reader_p = Process(target=reader_proc, args=((p_output, p_input),))
    reader_p.daemon = True
    reader_p.start()     # Launch the reader process

    p_output.close()       # We no longer need this part of the Pipe()
    _start = time.time()
    MidiIn(n,p_input) # Send a lot of stuff to reader_proc()
    p_input.close()
    reader_p.join()
    print("Sending {0} numbers to Pipe() took {1} seconds".format(n,
        (time.time() - _start)))


# In[5]:


if __name__ == '__main__':
    main() 

