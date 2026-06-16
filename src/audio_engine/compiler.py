import os
import json
import subprocess
import sys
from typing import Dict, Any


def execute_audio_compilation(state: Dict[str, Any]) -> Dict[str, Any]:
    track_spec = state.get("track_specification", {})
    track_id = track_spec.get("track_id", "track_001")
    branch_name = state.get("active_branch_name", track_id)

    output_dir = os.path.join("warehouse", "gold_outputs", track_id)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "master_output.wav")

    params = {
        "bpm": track_spec.get("bpm", 133),
        "key": track_spec.get("key", "A minor"),
        "energy": track_spec.get("energy", 0.8),
        "mood": track_spec.get("mood", "hypnotic"),
        "output_path": output_path,
        "branch_name": branch_name,
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    render_script = os.path.join(script_dir, "_render.py")

    print(f"[COMPILER] Compiling audio for branch '{branch_name}'")
    print(f"[COMPILER] Render script: {render_script}")
    print(f"[COMPILER] Output: {output_path}")

    try:
        result = subprocess.run(
            [sys.executable, render_script, json.dumps(params)],
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
            return {
                "compilation_errors": [error_msg],
                "gold_arrangement": "",
            }

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"[COMPILER] WAV file created ({file_size} bytes)")
            return {"gold_arrangement": output_path, "compilation_errors": []}
        else:
            msg = f"Output file not found: {output_path}"
            print(f"[COMPILER] {msg}")
            return {"compilation_errors": [msg], "gold_arrangement": ""}

    except subprocess.TimeoutExpired:
        msg = "Audio compilation timed out after 120s"
        print(f"[COMPILER] {msg}")
        return {"compilation_errors": [msg], "gold_arrangement": ""}
    except Exception as e:
        msg = f"Compilation failed: {e}"
        print(f"[COMPILER] {msg}")
        return {"compilation_errors": [msg], "gold_arrangement": ""}
