import os
import json
import subprocess
import sys
from typing import Dict, Any


def _fallback_render(state, output_wav, branch_name, track_spec):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    render_script = os.path.join(script_dir, "_render.py")
    params = {
        "bpm": track_spec.get("bpm", 133),
        "key": track_spec.get("key", "A minor"),
        "energy": track_spec.get("energy", 0.8),
        "mood": track_spec.get("mood", "hypnotic"),
        "output_path": output_wav,
        "branch_name": branch_name,
    }
    print(f"[COMPILER] Fallback render script: {render_script}")
    try:
        result = subprocess.run(
            [sys.executable, render_script, json.dumps(params)],
            capture_output=True, text=True, timeout=120,
        )
        if result.stdout:
            for line in result.stdout.strip().splitlines():
                print(f"[COMPILER] {line}")
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                print(f"[COMPILER] stderr: {line}")
        if result.returncode != 0:
            msg = result.stderr.strip() or f"Fallback failed with code {result.returncode}"
            return {"compilation_errors": [msg], "gold_arrangement": ""}
        if os.path.exists(output_wav):
            print(f"[COMPILER] WAV file created ({os.path.getsize(output_wav)} bytes)")
            return {"gold_arrangement": output_wav, "compilation_errors": []}
        return {"compilation_errors": ["Fallback output not found"], "gold_arrangement": ""}
    except Exception as e:
        return {"compilation_errors": [f"Fallback failed: {e}"], "gold_arrangement": ""}


def execute_audio_compilation(state: Dict[str, Any]) -> Dict[str, Any]:
    track_spec = state.get("track_specification", {})
    track_id = track_spec.get("track_id", "track_001")
    branch_name = state.get("active_branch_name", track_id)
    gold_arrangement = state.get("gold_arrangement", "")
    output_root = track_spec.get("output_dir", "warehouse")

    output_dir = os.path.join(output_root, "gold_outputs", track_id)
    os.makedirs(output_dir, exist_ok=True)
    output_wav = os.path.join(output_dir, "master_output.wav")

    if gold_arrangement and gold_arrangement.endswith(".py") and os.path.exists(gold_arrangement):
        render_script = gold_arrangement
        params = {}
        print(f"[COMPILER] Using Gold-generated script: {render_script}")
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        render_script = os.path.join(script_dir, "_render.py")
        params = {
            "bpm": track_spec.get("bpm", 133),
            "key": track_spec.get("key", "A minor"),
            "energy": track_spec.get("energy", 0.8),
            "mood": track_spec.get("mood", "hypnotic"),
            "output_path": output_wav,
            "branch_name": branch_name,
        }
        print(f"[COMPILER] Using default render script: {render_script}")

    if os.path.exists(output_wav):
        os.remove(output_wav)
    print(f"[COMPILER] Output: {output_wav}")

    try:
        args = [sys.executable, render_script]
        if params:
            args.append(json.dumps(params))

        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.stdout:
            for line in result.stdout.strip().splitlines():
                print(f"[COMPILER] {line}")
        if result.stderr:
            for line in result.stderr.strip().splitlines():
                print(f"[COMPILER] stderr: {line}")

        if result.returncode != 0:
            error_msg = result.stderr.strip() or f"Subprocess exited with code {result.returncode}"
            print(f"[COMPILER] Compilation failed: {error_msg}")
            if gold_arrangement and gold_arrangement.endswith(".py") and os.path.exists(gold_arrangement):
                print(f"[COMPILER] Gold script failed — falling back to default render")
                return _fallback_render(state, output_wav, branch_name, track_spec)
            return {
                "compilation_errors": [error_msg],
                "gold_arrangement": "",
            }

        if os.path.exists(output_wav):
            file_size = os.path.getsize(output_wav)
            print(f"[COMPILER] WAV file created ({file_size} bytes)")
            return {"gold_arrangement": output_wav, "compilation_errors": []}
        else:
            msg = f"Output file not found: {output_wav}"
            print(f"[COMPILER] {msg}")
            return {"compilation_errors": [msg], "gold_arrangement": ""}

    except subprocess.TimeoutExpired:
        msg = "Audio compilation timed out after 120s"
        print(f"[COMPILER] {msg}")
        if gold_arrangement and gold_arrangement.endswith(".py") and os.path.exists(gold_arrangement):
            print(f"[COMPILER] Gold script failed — falling back to default render")
            return _fallback_render(state, output_wav, branch_name, track_spec)
        return {"compilation_errors": [msg], "gold_arrangement": ""}
    except Exception as e:
        msg = f"Compilation failed: {e}"
        print(f"[COMPILER] {msg}")
        if gold_arrangement and gold_arrangement.endswith(".py") and os.path.exists(gold_arrangement):
            print(f"[COMPILER] Gold script failed — falling back to default render")
            return _fallback_render(state, output_wav, branch_name, track_spec)
        return {"compilation_errors": [msg], "gold_arrangement": ""}
