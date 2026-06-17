from pyo import *
import time
import os

# Initialize server
s = Server(audio="offline").boot()

# Track parameters
BPM = 140
beat_dur = 60.0 / BPM
total_beats = 128  # 16+16+32+16+32+16
total_dur = total_beats * beat_dur

# Output path
OUTPUT_WAV_PATH = r"warehouse\gold_outputs\track_002\master_output.wav"
os.makedirs(os.path.dirname(OUTPUT_WAV_PATH), exist_ok=True)

# Patterns
kick_pattern = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
hihat_pattern = [1, 0.7, 1, 0.8, 1, 0.6, 1, 0.9, 1, 0.7, 1, 0.8, 1, 0.6, 1, 0.9]
clap_pattern = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
bass_notes = [36, 36, 43, 36, 36, 43, 36, 36, 36, 36, 43, 36, 36, 43, 36, 36]
bass_gate = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
filter_automation = [0.2, 0.3, 0.5, 0.7, 0.9, 1.0, 0.8, 0.6, 0.4, 0.3, 0.5, 0.7, 0.9, 1.0, 0.8, 0.5]
volume_automation = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]

# Global mixer for stereo output
mixer = Mixer(2, 2, 16)
master_volume = Sig(0.0)

# Create base sound sources
noise_src = Noise(mul=0.0)
sine_src = Sine(freq=55, mul=0.0)

# Hihat: filtered noise
hihat_noise = Noise(mul=0.0)
hihat_filter = Biquad(hihat_noise, freq=8000, q=2)
hihat_out = Mul(hihat_filter, 0.12)

# Kick: low sine with quick decay
kick_sine = Sine(freq=55, mul=0.0)
kick_env = Sig(0.0)
kick_out = Mul(kick_sine, kick_env)

# Clap: noise burst
clap_noise = Noise(mul=0.0)
clap_env = Sig(0.0)
clap_out = Mul(clap_noise, clap_env, 0.25)

# Bass: sine oscillator with filter
bass_sine = Sine(freq=36, mul=0.0)
bass_filter = Biquad(bass_sine, freq=100, q=2)
bass_env = Sig(0.0)
bass_out = Mul(bass_filter, bass_env, 0.4)

# Atmosphere pad
pad_sine1 = Sine(freq=65.4, mul=0.0)
pad_sine2 = Sine(freq=130.8, mul=0.0)
pad_mix = Mix([pad_sine1, pad_sine2], voices=2)
pad_out = Mul(pad_mix, 0.15)

# Add all outputs to mixer
hihat_out.mix(2)
kick_out.mix(2)
clap_out.mix(2)
bass_out.mix(2)
pad_out.mix(2)

# Master output
Out = Mix([hihat_out, kick_out, clap_out, bass_out, pad_out], voices=2)
Out.out()

# Record setup
s.recordOptions(dur=total_dur, filename=OUTPUT_WAV_PATH, fileformat=0, sampletype=1)

# Helper function to play pattern
def play_pattern(pattern, gate_array, trig_func, step_dur):
    for i, gate in enumerate(gate_array):
        if gate > 0:
            trig_func(i, gate)
        time.sleep(step_dur)

# Trigger functions
def trigger_kick(step, velocity):
    freq = 55
    dur = 0.1
    env = LinTable(size=512)
    env[0] = 0
    env[int(512 * 0.1 / dur)] = 1
    env[511] = 0
    k = Sine(freq=freq, mul=velocity * 0.3)
    e = TableToSig(env, time=dur)
    o = k * e
    o.out()

def trigger_hihat(step, velocity):
    n = Noise(mul=velocity * 0.12)
    f = Biquad(n, freq=8000, q=2)
    f.out()

def trigger_clap(step, velocity):
    n = Noise(mul=velocity * 0.25)
    env = ExpTable(size=512)
    env[0] = 1
    env[511] = 0.001
    e = TableToSig(env, time=0.05)
    o = n * e
    o.out()

def trigger_bass(step, velocity):
    note = bass_notes[step % 16]
    freq = 32.7 * (2 ** (note / 12))
    n = Sine(freq=freq, mul=velocity * 0.4)
    env = ExpTable(size=512)
    env[0] = 1
    env[511] = 0.001
    e = TableToSig(env, time=0.5)
    o = n * e
    o.out()

def trigger_pad(step, velocity):
    # Atmospheric pad with filter sweep
    base_freq = 65.4 * (2 ** (step / 16))
    n1 = Sine(freq=base_freq, mul=velocity * 0.08)
    n2 = Sine(freq=base_freq * 1.5, mul=velocity * 0.06)
    f = Biquad(n1 + n2, freq=200 + 1800 * filter_automation[step % 16], q=1)
    f.out()

# Section durations
step_dur = beat_dur / 4
intro_steps = 64  # 16 beats * 4 steps
build_steps = 64
drop_steps = 128
breakdown_steps = 64
drop2_steps = 128
outro_steps = 64

# Start server and record
s.start()

print("Starting intro...")
# Intro: hihat and pad only
for step in range(intro_steps):
    if hihat_pattern[step % 16] > 0:
        trigger_hihat(step, hihat_pattern[step % 16])
    if step % 8 == 0:
        trigger_pad(step, 0.3)
    time.sleep(step_dur)

print("Starting build...")
# Build: add kick
for step in range(build_steps):
    if kick_pattern[step % 16] > 0:
        trigger_kick(step, 1.0)
    if hihat_pattern[step % 16] > 0:
        trigger_hihat(step, hihat_pattern[step % 16])
    if step % 8 == 0:
        trigger_pad(step, 0.4)
    time.sleep(step_dur)

print("Starting drop...")
# Drop: full arrangement
for step in range(drop_steps):
    if kick_pattern[step % 16] > 0:
        trigger_kick(step, 1.0)
    if hihat_pattern[step % 16] > 0:
        trigger_hihat(step, hihat_pattern[step % 16])
    if clap_pattern[step % 16] > 0:
        trigger_clap(step, 1.0)
    if bass_gate[step % 16] > 0:
        trigger_bass(step, 1.0)
    trigger_pad(step, 0.5)
    time.sleep(step_dur)

print("Starting breakdown...")
# Breakdown: stripped back with filter sweeps
for step in range(breakdown_steps):
    if hihat_pattern[step % 16] > 0:
        trigger_hihat(step, hihat_pattern[step % 16] * 0.7)
    if bass_gate[step % 16] > 0:
        trigger_bass(step, 0.7)
    trigger_pad(step, 0.2 + 0.3 * filter_automation[step % 16])
    time.sleep(step_dur)

print("Starting drop 2...")
# Drop 2: full arrangement again
for step in range(drop2_steps):
    if kick_pattern[step % 16] > 0:
        trigger_kick(step, 1.0)
    if hihat_pattern[step % 16] > 0:
        trigger_hihat(step, hihat_pattern[step % 16])
    if clap_pattern[step % 16] > 0:
        trigger_clap(step, 1.0)
    if bass_gate[step % 16] > 0:
        trigger_bass(step, 1.0)
    trigger_pad(step, 0.5)
    time.sleep(step_dur)

print("Starting outro...")
# Outro: fade out
for step in range(outro_steps):
    vel = max(0, 0.9 - (step / outro_steps) * 0.9)
    if kick_pattern[step % 16] > 0:
        trigger_kick(step, vel)
    if hihat_pattern[step % 16] > 0:
        trigger_hihat(step, hihat_pattern[step % 16] * vel)
    if step % 8 == 0:
        trigger_pad(step, vel * 0.3)
    time.sleep(step_dur)

# Wait for recording to complete
time.sleep(1)
s.stop()
s.shutdown()

print(f"Track rendered to {OUTPUT_WAV_PATH}")