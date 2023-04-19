

s.boot;

NetAddr.langPort
Server.default.latency
Server.default.options.hardwareBufferSize

m = NetAddr("127.0.0.1", NetAddr.langPort); // loopback
m.sendMsg("/chat", "Hello App 1");

ScampUtils.instrumentFromSynthDef(
	SynthDef( "cloud", {

		arg panCenter = 0, panWidth = 0.3, sustain = 0.3, pitch = 440, volume = 0.1, gate = 0;

		var sig;

		var env = EnvGate(gate:gate, fadeTime: 0.1);

		sig = LFPar.ar( pitch * [1,2,3,5], 0, volume/[2,4,5,7] );

		Out.ar( 0, Env([0,1,1,0], [0.025,sustain,0.025]).kr(1) * sig.dup )
}))

ScampUtils.instrumentFromSynthDef(
	SynthDef( "organ", { |pitch = 440, sustain = 1, amp = 0.1, gate = 0, volume = 0.1|

		var sig;

		var env = EnvGate(gate:gate, fadeTime: 0.1);

		sig = LFPar.ar( pitch * [1,2,3,5], 0, amp/[2,4,5,7] );

		Out.ar( 0, Env([0,1,1,0], [0.025,sustain,0.025]).kr(1) * sig.dup )

}))

s.quit;