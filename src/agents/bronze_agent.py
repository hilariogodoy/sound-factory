import json
import os
from typing import Dict, Any

PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config", "system_prompts", "bronze_designer.txt",
)


def bronze_designer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    track_spec = state.get("track_specification", {})
    analysis = state.get("analysis_metrics", {})
    branch = state.get("active_branch_name", "N/A")
    iteration = state.get("iterations_count", 0)

    print(f"[BRONZE] Designing instruments for branch '{branch}' (iteration {iteration})")

    try:
        with open(PROMPT_PATH) as f:
            system_prompt = f.read()
    except Exception as e:
        print(f"[BRONZE] Failed to read prompt: {e}")
        return {"bronze_instruments": {}}

    context = (
        f"TRACK CONTEXT:\n"
        f"- BPM: {track_spec.get('bpm', 'N/A')}\n"
        f"- Key: {track_spec.get('key', 'N/A')}\n"
        f"- Energy: {track_spec.get('energy', 'N/A')}\n"
        f"- Mood: {track_spec.get('mood', 'N/A')}\n"
        f"- Human feedback: {track_spec.get('human_feedback', 'none')}\n"
        f"\n"
        f"ANALYSIS METRICS FROM PREVIOUS ITERATION:\n"
        f"{json.dumps(analysis, indent=2) if analysis else 'No previous analysis available.'}\n"
    )

    try:
        from src.llm_factory import get_llm
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = get_llm()
        response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=context)])
        content = response.content.strip()

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        instruments = json.loads(content)

        if not isinstance(instruments, dict):
            print(f"[BRONZE] LLM returned non-dict, falling back to empty")
            return {"bronze_instruments": {}}

        validated = {}
        for k, v in instruments.items():
            if isinstance(v, str) and len(v) > 0:
                validated[k] = v
            else:
                print(f"[BRONZE] Skipping instrument '{k}': not a non-empty string")

        print(f"[BRONZE] Generated {len(validated)} instrument(s): {list(validated.keys())}")
        return {"bronze_instruments": validated}

    except json.JSONDecodeError as e:
        print(f"[BRONZE] JSON parse failed: {e}")
        return {"bronze_instruments": {}}
    except ImportError as e:
        print(f"[BRONZE] LLM dependencies missing: {e}")
        return {"bronze_instruments": {}}
    except Exception as e:
        print(f"[BRONZE] LLM call failed: {e}")
        return {"bronze_instruments": {}}
