from pyo import *
import time

s = Server(audio="offline").boot()
beat_dur = 60.0 / BPM  # BPM from track context
total_beats = 128
total_dur = total_beats * beat_dur
OUTPUT_WAV_PATH = "warehouse/gold_outputs/track_005/master_output.wav"
s.recordOptions(dur=total_dur, filename=OUTPUT_WAV_PATH, fileformat=0, sampletype=1)

# Define instrument objects using provided DSP snippets and pattern data
INSTRUMENTS_GO_HERE = {
    "kick": "Sine(freq=Linseg([(0,150),(0.05,50)]), mul=0.4).mix(2).out()",
    "hihat": "Noise(mul=0.15).mix(2).out()",
    "bass": "ButLP(Saw(freq=80, mul=0.35), freq=200).mix(2).out()"
}

PATTERNS_GO_HERE = {
    "kick": [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    "hihat": [1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1],
    "bass": [36, 36, 43, 36, 36, 43, 36, 36, 43, 36, 43, 36, 43, 36, 36],
    "bass_gate": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "automation_filter": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
    "automation_volume": [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]
}

step_dur = beat_dur / 4
def play(inst, pat):
    for g in pat:
        if g > 0:
            inst.out()
        time.sleep(step_dur)

s.start()
for section, insts, reps in [
    ("Intro", [INSTRUMENTS_GO_HERE["kick"], INSTRUMENTS_GO_HERE["hihat"]], 16),
    ("Build", [INSTRUMENTS_GO_HERE["kick"], INSTRUMENTS_GO_HERE["bass"], INSTRUMENTS_GO_HERE["hihat"]], 16),
    ("Drop", [INSTRUMENTS_GO_HERE["kick"], INSTRUMENTS_GO_HERE["bass"], INSTRUMENTS_GO_HERE["bass_gate"]], 32),
    ("Breakdown", [INSTRUMENTS_GO_HERE["hihat"], INSTRUMENTS_GO_HERE["bass"]], 16),
    ("Drop2", [INSTRUMENTS_GO_HERE["kick"], INSTRUMENTS_GO_HERE["hihat"], INSTRUMENTS_GO_HERE["bass_gate"]], 32),
    ("Outro", [INSTRUMENTS_GO_HERE["hihat"], INSTRUMENTS_GO_HERE["bass"]], 16),
]

time.sleep(total_dur + 1)
s.stop(); s.shutdown()