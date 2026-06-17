#!/usr/bin/env python
"""
Standalone Pyo render script — spawned as subprocess by compiler.py.
Uses Pyo offline rendering with signal-graph-based pattern generation
(no time.sleep loops, so rendering is fast).
"""
import sys
import json
import os
import time

params = json.loads(sys.argv[1])
bpm = params["bpm"]
key = params.get("key", "A minor")
energy = params.get("energy", 0.8)
mood = params.get("mood", "hypnotic")
output_path = params["output_path"]

try:
    from pyo import *

    s = Server(audio="offline").boot()
    beat_dur = 60.0 / bpm
    total_beats = 64
    total_dur = total_beats * beat_dur

    freq_map = {
        "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13,
        "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00,
        "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88,
    }
    root_pitch = freq_map.get(key.split()[0], 220.0)
    amp = max(0.3, energy * 0.6)

    # --- Kick drum: sine sweep with exponential decay ---
    kick_freq = SigTo(value=60, time=0.001, init=60)
    kick_env = Expseg([(0, 1), (0.05, 0.3), (0.3, 0)], exp=4).play()
    kick_sig = Sine(freq=kick_freq, mul=kick_env * amp * 0.5)
    kick_freq.value = 40

    # --- Hi-hat: filtered noise with fast decay ---
    hat_env = Expseg([(0, 1), (0.02, 0.1), (0.15, 0)], exp=6).play()
    hat_sig = Biquad(Noise(mul=hat_env * amp * 0.2), freq=8000, q=0.5, type=2)

    # --- Bass: saw wave with filter ---
    bass_freq = SigTo(value=root_pitch * 0.5, time=0.02, init=root_pitch * 0.5)
    bass_saw = RCOsc(freq=bass_freq, mul=amp * 0.3)
    bass_filt = Biquad(bass_saw, freq=300, q=2, type=0)

    # --- Pad: detuned sines with slow filter sweep ---
    lfo_freq = Sine(freq=0.05, mul=200, add=400)
    pad1 = Sine(freq=root_pitch * 0.25, mul=amp * 0.15)
    pad2 = Sine(freq=root_pitch * 0.25 * 1.01, mul=amp * 0.15)
    pad = Biquad(pad1 + pad2, freq=lfo_freq, q=3)

    # --- 16-step trigger generator ---
    metro = Metro(time=beat_dur / 4).play()
    step_counter = Counter(metro, min=0, max=15)
    beat_counter = Counter(Counter(metro, min=0, max=3), min=0, max=63)

    # --- Kick pattern: 4-on-the-floor ---
    kick_trig = TrigFunc(metro, function=lambda: None)
    def kick_callback():
        step = int(step_counter.get())
        if step in [0, 4, 8, 12]:
            kick_env.play()
            kick_freq.value = 60
    kick_trig = TrigFunc(metro, function=kick_callback)

    # --- Hi-hat pattern: 8th notes ---
    def hat_callback():
        step = int(step_counter.get())
        if step % 2 == 0:
            hat_env.play()
    hat_trig = TrigFunc(metro, function=hat_callback)

    # --- Bass pattern: change note every 4 beats ---
    bass_notes = [0, 0, 7, 5, 0, 0, 7, 3, 0, 0, 7, 5, 0, 0, 7, 3]
    def bass_callback():
        beat = int(beat_counter.get())
        note = bass_notes[beat % 16]
        bass_freq.value = root_pitch * 0.25 * (2 ** (note / 12))
    bass_trig = TrigFunc(metro, function=bass_callback)

    # --- Output mix ---
    mixer = Mixer(outs=2, chnls=4)
    mixer.addInput(0, kick_sig)
    mixer.addInput(1, hat_sig)
    mixer.addInput(2, bass_filt)
    mixer.addInput(3, pad)
    mixer.setAmp(0, 0, 0.7, 1, 0.7)
    mixer.setAmp(1, 0, 0.5, 1, 0.5)
    mixer.setAmp(2, 0, 0.6, 1, 0.6)
    mixer.setAmp(3, 0, 0.4, 1, 0.4)
    stereo_out = mixer[0].out()

    s.recordOptions(dur=total_dur, filename=output_path, fileformat=0, sampletype=1)
    s.start()
    time.sleep(total_dur)
    s.stop()
    s.shutdown()

    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        print(f"WAV written: {output_path} ({size} bytes)")
    else:
        print(f"Error: output not found at {output_path}", file=sys.stderr)
        sys.exit(1)

except ImportError as e:
    print(f"Pyo not available: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Render error: {e}", file=sys.stderr)
    sys.exit(1)
