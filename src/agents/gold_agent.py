import json
import os
import re
from typing import Dict, Any

PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config", "system_prompts", "gold_mixer.txt",
)


def gold_mixer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    track_spec = state.get("track_specification", {})
    instruments = state.get("bronze_instruments", {})
    patterns = state.get("silver_patterns", {})
    branch = state.get("active_branch_name", "N/A")
    track_id = track_spec.get("track_id", "track_001")

    output_wav = os.path.join("warehouse", "gold_outputs", track_id, "master_output.wav")
    script_path = os.path.join("warehouse", "gold_outputs", track_id, "_gold_arrangement.py")

    print(f"[GOLD] Mixing arrangement for branch '{branch}'")

    try:
        with open(PROMPT_PATH) as f:
            system_prompt = f.read()
    except Exception as e:
        print(f"[GOLD] Failed to read prompt: {e}")
        return {"gold_arrangement": ""}

    context = (
        f"TRACK CONTEXT:\n"
        f"- BPM: {track_spec.get('bpm', 'N/A')}\n"
        f"- Key: {track_spec.get('key', 'N/A')}\n"
        f"- Energy: {track_spec.get('energy', 'N/A')}\n"
        f"- Mood: {track_spec.get('mood', 'N/A')}\n"
        f"- Human feedback: {track_spec.get('human_feedback', 'none')}\n"
        f"\n"
        f"INSTRUMENTS_JSON:\n"
        f"{json.dumps(instruments, indent=2) if instruments else 'No instruments defined — use generic Sine/Noise oscillators.'}\n"
        f"\n"
        f"PATTERNS_JSON:\n"
        f"{json.dumps(patterns, indent=2) if patterns else 'No patterns defined — create simple 4-on-the-floor patterns.'}\n"
        f"\n"
        f"OUTPUT_WAV_PATH:\n"
        f"{output_wav}\n"
    )

    try:
        from src.llm_factory import get_llm
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = get_llm()
        response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=context)])
        content = response.content.strip()

        match = re.search(r"```python\s*\n(.*?)\n```", content, re.DOTALL)
        if match:
            code = match.group(1).strip()
        elif "```" in content:
            code = content.split("```")[1].strip()
            if code.startswith("python\n"):
                code = code[7:]
            code = code.strip()
        else:
            code = content

        os.makedirs(os.path.dirname(script_path), exist_ok=True)
        with open(script_path, "w") as f:
            f.write(code)

        file_size = os.path.getsize(script_path)
        print(f"[GOLD] Written arrangement script ({file_size} bytes): {script_path}")
        return {"gold_arrangement": script_path}

    except ImportError as e:
        print(f"[GOLD] LLM dependencies missing: {e}")
        return {"gold_arrangement": ""}
    except Exception as e:
        print(f"[GOLD] LLM call failed: {e}")
        return {"gold_arrangement": ""}
