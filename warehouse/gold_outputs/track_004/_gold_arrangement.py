from pyo import *
import time

s = Server(audio="offline").boot()
BPM = 140
beat_dur = 60.0 / BPM
total_beats = 128
total_dur = total_beats * beat_dur
WAV = r"warehouse\gold_outputs\track_004\master_output.wav"
s.recordOptions(dur=total_dur, filename=WAV, fileformat=0, sampletype=1)

# Create base oscillators for instruments
kick_osc = Sine(freq=50, mul=0.5)
hihat_noise = Noise(mul=0.3)
bass_osc = Osc(table=SawTable(), freq=100, mul=0.2)

# Apply stereo mixing
kick = kick_osc.mix(2)
hihat = hihat_noise.mix(2)
bass = bass_osc.mix(2)

# Patterns
kick_pat = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
hihat_pat = [1, 0.8, 0, 0.7, 1, 0.9, 0, 0.6, 1, 0.7, 0, 0.8, 1, 0.9, 0, 0.7]
bass_notes = [36, 36, 39, 36, 36, 36, 43, 36, 36, 36, 39, 36, 36, 36, 43, 36]
bass_gate = [1, 0.7, 1, 0.6, 1, 0.8, 1, 0.5, 1, 0.7, 1, 0.6, 1, 0.9, 1, 0.5]
automation_filter = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
automation_volume = [0.8, 0.85, 0.9, 0.95, 1.0, 0.95, 0.9, 0.85, 0.8, 0.85, 0.9, 0.95, 1.0, 0.95, 0.9, 0.85]

step_dur = beat_dur / 4

def play_pattern(pat, inst, velocities=None):
    for i, g in enumerate(pat):
        if g > 0:
            if velocities:
                inst.out()
            else:
                inst.out()
        time.sleep(step_dur)

def play_bass_pattern():
    for i, g in enumerate(bass_gate):
        if g > 0:
            freq = 55.0 * (2 ** ((bass_notes[i] - 36) / 12.0))
            bass_osc.freq = freq
            bass_osc.mul = 0.2 * g
            bass.out()
        time.sleep(step_dur)

s.start()

# Intro (16 beats) - hihat and atmosphere
for _ in range(16):
    play_pattern(hihat_pat, hihat)

# Build (16 beats) - add kick
for _ in range(16):
    play_pattern(kick_pat, kick)
    play_pattern(hihat_pat, hihat)

# Drop (32 beats) - full arrangement
for _ in range(32):
    play_pattern(kick_pat, kick)
    play_pattern(hihat_pat, hihat)
    play_bass_pattern()

# Breakdown (16 beats) - strip back with filter sweeps
for _ in range(16):
    play_pattern(hihat_pat, hihat)
    play_bass_pattern()

# Drop 2 (32 beats) - full again
for _ in range(32):
    play_pattern(kick_pat, kick)
    play_pattern(hihat_pat, hihat)
    play_bass_pattern()

# Outro (16 beats) - fade out
for _ in range(16):
    play_pattern(hihat_pat, hihat)

time.sleep(1)
s.stop()
s.shutdown()