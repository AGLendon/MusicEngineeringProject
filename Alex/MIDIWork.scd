MIDIClient.init;
MIDIClient.destinations
MIDIIn.connectAll;
MIDIOut.findPort
MIDIOut.connect
MIDIOut.new(1,1)

MIDIEvent.new(,1,1

MIDIdef.noteOn(\noteOnTest, {"Key Down".postln})
MIDIdef(\noteOnTest).free;



	(
    // substitute your own device here
var    mOut = MIDIOut.newByName("loopMIDI Port", "loopMIDI Port").latency_(Server.default.latency);

p = Pbind(
    \type, \midi,
        // this line is optional b/c noteOn is the default
        // just making it explicit here
    \midicmd, \noteOn,
    \midiout, mOut,    // must provide the MIDI target here
    \chan, 0,
        // degree is converted to midinote, not just frequency
    \degree, Pwhite(-7, 12, inf),
    \dur, Pwrand([0.25, Pn(0.125, 2)], #[0.8, 0.2], inf),
    \legato, sin(Ptime(inf) * 0.5).linexp(-1, 1, 1/3, 3),
    \amp, Pexprand(0.5, 1.0, inf)
).play(quant: 1);
)

p.stop;


	Platform.userExtensionDir
	m = SimpleMIDIFile.read("RNN_test_5.mid");