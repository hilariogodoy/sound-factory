#!/usr/bin/env python
"""
Standalone Pyo render script — spawned as subprocess by compiler.py.
Accepts JSON params as first CLI argument.

Usage:
    python _render.py '{"bpm": 133, "key": "A minor", "energy": 0.8,
                        "mood": "hypnotic", "output_path": "out.wav"}'
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
branch_name = params.get("branch_name", "")

try:
    from pyo import Server, Sine, RCOsc, Mixer, Record

    s = Server(audio="offline").boot()

    beat_dur = 60.0 / bpm
    total_beats = 64
    total_dur = total_beats * beat_dur

    freq_map = {
        "C": 261.63, "C#": 277.18, "D": 293.66, "D#": 311.13,
        "E": 329.63, "F": 349.23, "F#": 369.99, "G": 392.00,
        "G#": 415.30, "A": 440.00, "A#": 466.16, "B": 493.88,
    }
    root = key.split()[0]
    freq = freq_map.get(root, 220.0)

    amp = max(0.05, energy * 0.4)
    osc = Sine(freq=freq, mul=amp).out()

    s.recordOptions(dur=total_dur, filename=output_path, fileformat=0, sampletype=1)
    s.start()
    time.sleep(total_dur)
    s.stop()
    s.shutdown()

    if os.path.exists(output_path):
        print(f"WAV written: {output_path}")
    else:
        print(f"Error: output not found at {output_path}", file=sys.stderr)
        sys.exit(1)

except ImportError as e:
    print(f"Pyo not available: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Render error: {e}", file=sys.stderr)
    sys.exit(1)
