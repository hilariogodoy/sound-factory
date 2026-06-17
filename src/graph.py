import json
import os
from typing import TypedDict, List, Dict, Any, Literal
from langgraph.graph import StateGraph, END

from src.agents.orchestrator import orchestrator_node
from src.agents.bronze_agent import bronze_designer_node
from src.agents.silver_agent import silver_sequencer_node
from src.agents.gold_agent import gold_mixer_node
from src.agents.curator_agent import curator_node
from src.audio_engine.compiler import execute_audio_compilation
from src.audio_engine.analyzer import analyze_audio_node


class AudioWarehouseState(TypedDict):
    track_specification: Dict[str, Any]
    active_branch_name: str
    bronze_instruments: Dict[str, str]
    silver_patterns: Dict[str, Any]
    gold_arrangement: str
    compilation_errors: List[str]
    curator_report: Dict[str, Any]
    iterations_count: int
    analysis_metrics: Dict[str, float]


def decide_next_after_curator(
    state: AudioWarehouseState,
) -> Literal["bronze_designer", "error_termination", "__end__"]:
    iterations = state.get("iterations_count", 0)
    if iterations >= 3:
        print(f"[ROUTER] iterations_count={iterations} >= 3 -> error_termination")
        return "error_termination"
    if state.get("curator_report", {}).get("approved", False):
        print(f"[ROUTER] Curator approved -> END")
        return END
    print(f"[ROUTER] Curator rejected, iterations={iterations} -> retry bronze_designer")
    return "bronze_designer"


def error_termination_node(state: AudioWarehouseState) -> Dict[str, Any]:
    track_spec = state.get("track_specification", {})
    track_id = track_spec.get("track_id", "track_001")
    output_root = track_spec.get("output_dir", "warehouse")
    manifest_dir = os.path.join(output_root, "gold_outputs", track_id)
    os.makedirs(manifest_dir, exist_ok=True)

    manifest = {
        "track_id": track_id,
        "status": "failed",
        "iterations_count": state.get("iterations_count", 0),
        "compilation_errors": state.get("compilation_errors", []),
        "curator_report": state.get("curator_report", {}),
    }
    manifest_path = os.path.join(manifest_dir, "failure_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"[ERROR_TERMINATION] Circuit breaker tripped after "
          f"{state.get('iterations_count', 0)} iteration(s)")
    print(f"[ERROR_TERMINATION] Failure manifest written to {manifest_path}")
    return {}


def build_graph() -> StateGraph:
    graph = StateGraph(AudioWarehouseState)

    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("bronze_designer", bronze_designer_node)
    graph.add_node("silver_sequencer", silver_sequencer_node)
    graph.add_node("gold_mixer", gold_mixer_node)
    graph.add_node("audio_compiler", execute_audio_compilation)
    graph.add_node("audio_analyzer", analyze_audio_node)
    graph.add_node("taste_curator", curator_node)
    graph.add_node("error_termination", error_termination_node)

    graph.set_entry_point("orchestrator")

    graph.add_edge("orchestrator", "bronze_designer")
    graph.add_edge("bronze_designer", "silver_sequencer")
    graph.add_edge("silver_sequencer", "gold_mixer")
    graph.add_edge("gold_mixer", "audio_compiler")
    graph.add_edge("audio_compiler", "audio_analyzer")
    graph.add_edge("audio_analyzer", "taste_curator")

    graph.add_conditional_edges(
        "taste_curator",
        decide_next_after_curator,
        {
            "bronze_designer": "bronze_designer",
            "error_termination": "error_termination",
            END: END,
        }
    )

    graph.add_edge("error_termination", END)

    return graph.compile()
