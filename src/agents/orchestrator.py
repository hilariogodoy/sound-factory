import os
from datetime import datetime
from typing import Dict, Any


def orchestrator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    track_spec = state.get("track_specification", {})
    track_id = track_spec.get("track_id", "track_001")
    output_dir = track_spec.get("output_dir", "warehouse")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch_name = f"{track_id}_{timestamp}"
    bronze_dir = os.path.join(output_dir, "bronze_patches", branch_name)
    silver_dir = os.path.join(output_dir, "silver_loops", branch_name)
    gold_dir = os.path.join(output_dir, "gold_outputs", track_id)

    for d in [bronze_dir, silver_dir, gold_dir]:
        os.makedirs(d, exist_ok=True)

    print(f"[ORCHESTRATOR] Initialized branch '{branch_name}'")
    print(f"[ORCHESTRATOR] Dirs: {bronze_dir}, {silver_dir}, {gold_dir}")
    print(f"[ORCHESTRATOR] Track: {track_spec.get('bpm')} BPM, "
          f"Key: {track_spec.get('key')}, "
          f"Energy: {track_spec.get('energy')}, "
          f"Mood: {track_spec.get('mood')}")

    return {
        "active_branch_name": branch_name,
        "iterations_count": 0,
        "compilation_errors": [],
    }
