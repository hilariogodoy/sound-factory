from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

from src.agents.orchestrator import orchestrator_node
from src.agents.bronze_agent import bronze_designer_node
from src.agents.silver_agent import silver_sequencer_node
from src.agents.gold_agent import gold_mixer_node
from src.agents.curator_agent import curator_node
from src.audio_engine.compiler import execute_audio_compilation


class AudioWarehouseState(TypedDict):
    track_specification: Dict[str, Any]
    active_branch_name: str
    bronze_instruments: Dict[str, str]
    silver_patterns: Dict[str, Any]
    gold_arrangement: str
    compilation_errors: List[str]
    curator_report: Dict[str, Any]
    iterations_count: int


def build_graph() -> StateGraph:
    graph = StateGraph(AudioWarehouseState)

    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("bronze_designer", bronze_designer_node)
    graph.add_node("silver_sequencer", silver_sequencer_node)
    graph.add_node("gold_mixer", gold_mixer_node)
    graph.add_node("audio_compiler", execute_audio_compilation)
    graph.add_node("taste_curator", curator_node)

    graph.set_entry_point("orchestrator")

    graph.add_edge("orchestrator", "bronze_designer")
    graph.add_edge("bronze_designer", "silver_sequencer")
    graph.add_edge("silver_sequencer", "gold_mixer")
    graph.add_edge("gold_mixer", "audio_compiler")
    graph.add_edge("audio_compiler", "taste_curator")
    graph.add_edge("taste_curator", END)

    return graph.compile()
