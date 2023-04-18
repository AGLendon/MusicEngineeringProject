import mido #logging midi messages

instrument = mido.get_input_names()
inport = mido.open_input(instrument[0])
events = []
while len(events)<6:
    msg = inport.receive()
    events.append(msg)
else:
  print("6 events recorded")

