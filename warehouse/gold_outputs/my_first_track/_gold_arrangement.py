from pyo import *
import time

# Initialize server
s = Server(audio="offline").boot()
s.start()

# Track parameters
BPM = 140
KEY = "C minor"
ENERGY = 0.9
MOOD = "dark"
OUTPUT_WAV_PATH = "warehouse\\gold_outputs\\my_first_track\\master_output.wav"

# Calculate timing
beat_dur = 60.0 / BPM
total_dur = (16 + 16 + 32 + 16 + 32 + 16) * beat_dur

# Create instruments
kick = Sine(freq=55, mul=0.4).mix(2)
hihat = Noise(mul=0.1).mix(2)
bass = Saw(freq=80, mul=0.4).mix(2)

# Pattern playback function
def play_pattern(instrument, pattern, gate=None, notes=None, automation=None):
    if gate is None:
        gate = [1] * len(pattern)
    if notes is None:
        notes = [0] * len(pattern)
    if automation is None:
        automation = [1.0] * len(pattern)
    for i in range(len(pattern)):
        if pattern[i] and gate[i]:
            if notes:
                instrument.freq = notes[i]
            instrument.out().mix(automation[i])
        time.sleep(beat_dur / 4)

# Intro section
s.recordOptions(dur=total_dur, filename=OUTPUT_WAV_PATH, fileformat=0, sampletype=1)
s.record()
time.sleep(16 * beat_dur)
s.stop()

# Build section
s.start()
time.sleep(16 * beat_dur)
s.stop()

# Drop section
s.start()
time.sleep(32 * beat_dur)
s.stop()

# Breakdown section
s.start()
time.sleep(16 * beat_dur)
s.stop()

# Drop 2 section
s.start()
time.sleep(32 * beat_dur)
s.stop()

# Outro section
s.start()
time.sleep(16 * beat_dur)
s.stop()

# Clean shutdown
s.shutdown()