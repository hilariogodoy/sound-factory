from pyo import *
import time
import os

# Track parameters
BPM = 140
KEY = "C minor"
ENERGY = 0.9
MOOD = "dark"
OUTPUT_WAV_PATH = r"warehouse\gold_outputs\track_003\master_output.wav"

# Timing calculations
beat_dur = 60.0 / BPM
step_dur = beat_dur / 4

# Total arrangement duration
total_beats = 16 + 16 + 32 + 16 + 32 + 16  # 128 beats
total_dur = total_beats * beat_dur

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_WAV_PATH), exist_ok=True)

# Initialize server
s = Server(audio="offline").boot()

# Create instruments
kick_sine = Sine(freq=140, mul=0.6)
kick_env = TrigEnv(kick_sine.play(), table=LinTable(), dur=0.1, mul=0.6)
kick = kick_env.mix(2)

hihat_noise = Noise(mul=0.15)
hihat_env = TrigEnv(hihat_noise.play(), table=LinTable(), dur=0.05, mul=0.15)
hihat_filter = Biquad(hihat_env, freq=8000, q=5)
hihat = hihat_filter.mix(2)

bass_saw = RCOsc(table=SawTable(), freq=40, mul=0.1)
bass_env = TrigEnv(bass_saw.play(), table=LinTable(), dur=0.3, mul=0.1)
bass_filter = Biquad(bass_env, freq=80, q=2, type=0)
bass = bass_filter.mix(2)

# Master mixer
master = Mixer(chnls=2, sizein=3)

# Patterns
kick_pattern = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
hihat_pattern = [1, 0.5, 1, 0, 1, 0.5, 1, 0, 1, 0.5, 1, 0, 1, 0.5, 1, 0]
bass_pattern = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

# Automation patterns
automation_filter = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
automation_volume = [0.9, 0.85, 0.9, 0.85, 0.9, 0.85, 0.9, 0.85, 0.9, 0.85, 0.9, 0.85, 0.9, 0.85, 0.9, 0.85]

# Setup recording
s.recordOptions(dur=total_dur, filename=OUTPUT_WAV_PATH, fileformat=0, sampletype=1)

# Global mix level
mix_level = SigTo(0, time=0.1)

def play_step(pattern, instrument, step_idx, velocity=1.0):
    """Play a step if gate is active"""
    if pattern[step_idx % len(pattern)] > 0:
        vel = pattern[step_idx % len(pattern)] if isinstance(pattern[step_idx % len(pattern)], float) else 1.0
        instrument.out(chnls=2)

def play_section(steps, kick_active=True, hihat_active=True, bass_active=True, filter_automate=False, volume_automate=False):
    """Play a section for given number of steps"""
    for step in range(steps):
        if kick_active:
            play_step(kick_pattern, kick_env, step)
        if hihat_active:
            play_step(hihat_pattern, hihat_env, step)
        if bass_active:
            play_step(bass_pattern, bass_env, step)
        
        if filter_automate and step < len(automation_filter):
            bass_filter.freq = 50 + automation_filter[step] * 150
        
        if volume_automate and step < len(automation_volume):
            mix_level.value = automation_volume[step]
        
        time.sleep(step_dur)

# Start server for recording
s.start()

# Intro - 16 beats (sparse, hihat and atmosphere)
for step in range(64):  # 16 beats = 64 steps
    play_step(hihat_pattern, hihat_env, step)
    time.sleep(step_dur)

# Build - 16 beats (add kick, slowly introduce more elements)
for step in range(64):  # 16 beats = 64 steps
    play_step(kick_pattern, kick_env, step)
    play_step(hihat_pattern, hihat_env, step)
    if step > 32:  # Add bass in second half of build
        play_step(bass_pattern, bass_env, step)
    time.sleep(step_dur)

# Drop - 32 beats (full arrangement)
for step in range(128):  # 32 beats = 128 steps
    play_step(kick_pattern, kick_env, step)
    play_step(hihat_pattern, hihat_env, step)
    play_step(bass_pattern, bass_env, step)
    time.sleep(step_dur)

# Breakdown - 16 beats (strip back, filter sweeps)
for step in range(64):  # 16 beats = 64 steps
    if step % 2 == 0:  # Sparse kick
        kick_env.out(chnls=2)
    play_step(hihat_pattern, hihat_env, step)
    
    # Filter sweep on bass
    sweep_freq = 100 + (step % 16) * 25
    bass_filter.freq = sweep_freq
    
    time.sleep(step_dur)

# Drop 2 - 32 beats (full again)
for step in range(128):  # 32 beats = 128 steps
    play_step(kick_pattern, kick_env, step)
    play_step(hihat_pattern, hihat_env, step)
    play_step(bass_pattern, bass_env, step)
    time.sleep(step_dur)

# Outro - 16 beats (fade out)
for step in range(64):  # 16 beats = 64 steps
    # Gradually reduce volume
    fade = 1.0 - (step / 64.0)
    if step % 4 == 0:  # Sparse kick
        kick_env.out(chnls=2)
    if step % 2 == 0:  # Sparse hihat
        play_step(hihat_pattern, hihat_env, step)
    if step % 8 == 0:  # Very sparse bass
        play_step(bass_pattern, bass_env, step)
    time.sleep(step_dur)

# Stop and shutdown
s.stop()
s.shutdown()