from multiprocess import Process,Queue,Pipe
from MIDITest import f

lastOut = []

while True:
    parent_conn,child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    out = parent_conn.recv()
    #print(out)   
    if out != lastOut:
        print(out[len(out)-5:] )  
    
    lastOut = out 
    
