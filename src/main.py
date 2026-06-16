import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.graph import build_graph, AudioWarehouseState


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audio Warehouse Engine — Autonomous AI Techno Producer"
    )
    parser.add_argument("--bpm", type=int, default=133, help="Target BPM (default: 133)")
    parser.add_argument("--key", type=str, default="A minor", help="Musical key (default: A minor)")
    parser.add_argument("--energy", type=float, default=0.8, help="Energy level 0.0-1.0 (default: 0.8)")
    parser.add_argument("--mood", type=str, default="hypnotic", help="Mood descriptor (default: hypnotic)")
    parser.add_argument("--track-id", type=str, default="track_001", help="Track identifier (default: track_001)")
    parser.add_argument("--human-feedback", type=str, default="", help="Human feedback for retry")
    parser.add_argument("--dry-run", action="store_true", help="Print node sequence without invoking")
    return parser.parse_args()


def build_initial_state(args: argparse.Namespace) -> AudioWarehouseState:
    return {
        "track_specification": {
            "bpm": args.bpm,
            "key": args.key,
            "energy": args.energy,
            "mood": args.mood,
            "track_id": args.track_id,
            "human_feedback": args.human_feedback,
        },
        "active_branch_name": "",
        "bronze_instruments": {},
        "silver_patterns": {},
        "gold_arrangement": "",
        "compilation_errors": [],
        "curator_report": {},
        "iterations_count": 0,
        "analysis_metrics": {},
    }


def main() -> None:
    args = parse_args()
    initial_state = build_initial_state(args)

    if args.dry_run:
        print("[DRY RUN] Graph structure:")
        print("  Primary: orchestrator -> bronze_designer -> silver_sequencer ->")
        print("           gold_mixer -> audio_compiler -> audio_analyzer ->")
        print("           taste_curator")
        print("  Conditional routing from taste_curator:")
        print("    - approved (score >= 0.7):         -> END")
        print("    - rejected (score < 0.7, iters<3): -> bronze_designer (retry)")
        print("    - rejected (iters >= 3):           -> error_termination -> END")
        print("[DRY RUN] No LLM calls or compilation performed.")
        sys.exit(0)

    app = build_graph()

    try:
        final_state = app.invoke(initial_state, {"recursion_limit": 100})
        print("\n[SESSION COMPLETE]")
        print(f"  Track ID:       {args.track_id}")
        print(f"  BPM:            {args.bpm}")
        print(f"  Key:            {args.key}")
        print(f"  Energy:         {args.energy}")
        print(f"  Mood:           {args.mood}")
        print(f"  Iterations:     {final_state.get('iterations_count', 'N/A')}")
        print(f"  Approved:       {final_state.get('curator_report', {}).get('approved', 'N/A')}")
        print(f"  Score:          {final_state.get('curator_report', {}).get('score', 'N/A')}")
        print(f"  Compilation errors: {len(final_state.get('compilation_errors', []))}")
        if final_state.get("analysis_metrics"):
            m = final_state["analysis_metrics"]
            print(f"  Tempo:          {m.get('tempo_bpm', 'N/A'):.1f} BPM")
            print(f"  Centroid:       {m.get('spectral_centroid_mean', 0):.0f} Hz")
            print(f"  RMS variance:   {m.get('rms_energy_variance', 0):.4f}")
            print(f"  ZCR mean:       {m.get('zero_crossing_rate_mean', 0):.4f}")
        print(f"  Output:         warehouse/gold_outputs/{args.track_id}/master_output.wav")
    except Exception as e:
        print(f"[FATAL ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
