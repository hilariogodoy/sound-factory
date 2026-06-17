import json
import os
from typing import Dict, Any, List

PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config", "system_prompts", "silver_sequencer.txt",
)


def silver_sequencer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    track_spec = state.get("track_specification", {})
    instruments = state.get("bronze_instruments", {})
    branch = state.get("active_branch_name", "N/A")

    print(f"[SILVER] Sequencing patterns for branch '{branch}'")

    try:
        with open(PROMPT_PATH) as f:
            system_prompt = f.read()
    except Exception as e:
        print(f"[SILVER] Failed to read prompt: {e}")
        return {"silver_patterns": {}}

    context = (
        f"TRACK CONTEXT:\n"
        f"- BPM: {track_spec.get('bpm', 'N/A')}\n"
        f"- Key: {track_spec.get('key', 'N/A')}\n"
        f"- Energy: {track_spec.get('energy', 'N/A')}\n"
        f"- Mood: {track_spec.get('mood', 'N/A')}\n"
        f"- Human feedback: {track_spec.get('human_feedback', 'none')}\n"
        f"\n"
        f"AVAILABLE INSTRUMENTS:\n"
        f"{json.dumps(list(instruments.keys()), indent=2) if instruments else 'No instruments available — create patterns for a generic kick, hihat, clap, and bass.'}\n"
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

        patterns = json.loads(content)

        if not isinstance(patterns, dict):
            print(f"[SILVER] LLM returned non-dict, falling back to empty")
            return {"silver_patterns": {}}

        validated: Dict[str, Any] = {}
        for k, v in patterns.items():
            if isinstance(v, list) and len(v) > 0:
                validated[k] = v
            else:
                print(f"[SILVER] Skipping pattern '{k}': not a non-empty list")

        print(f"[SILVER] Generated {len(validated)} pattern(s): {list(validated.keys())}")
        return {"silver_patterns": validated}

    except json.JSONDecodeError as e:
        print(f"[SILVER] JSON parse failed: {e}")
        return {"silver_patterns": {}}
    except ImportError as e:
        print(f"[SILVER] LLM dependencies missing: {e}")
        return {"silver_patterns": {}}
    except Exception as e:
        err_msg = str(e)
        for line in err_msg.splitlines():
            if "sk-or-" in line or "api-key" in line.lower():
                continue
            print(f"[SILVER] LLM call failed: {line}")
        return {"silver_patterns": {}}
