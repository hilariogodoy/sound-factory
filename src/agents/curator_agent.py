import json
import os
from typing import Dict, Any

PROMPT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config", "system_prompts", "curator_critic.txt",
)
TASTE_PROFILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "config", "reference_taste_profile.json",
)


def curator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    iterations = state.get("iterations_count", 0) + 1
    analysis = state.get("analysis_metrics", {})
    errors = state.get("compilation_errors", [])
    track_spec = state.get("track_specification", {})
    previous_report = state.get("curator_report", {})

    print(f"[CURATOR] Iteration {iterations}: evaluating track")

    if errors:
        report = {
            "approved": False,
            "score": 0.0,
            "feedback": f"Compilation errors: {'; '.join(errors)}",
            "iteration": iterations,
        }
        print(f"[CURATOR] Auto-rejected: compilation errors")
        return {"curator_report": report, "iterations_count": iterations}

    if not analysis:
        report = {
            "approved": False,
            "score": 0.0,
            "feedback": "No audio analysis available — track could not be rendered.",
            "iteration": iterations,
        }
        print(f"[CURATOR] Auto-rejected: no analysis metrics")
        return {"curator_report": report, "iterations_count": iterations}

    try:
        with open(TASTE_PROFILE_PATH) as f:
            taste_profile = json.load(f)
    except Exception as e:
        print(f"[CURATOR] Failed to load taste profile: {e}")
        taste_profile = {"metrics": {}}

    try:
        with open(PROMPT_PATH) as f:
            system_prompt = f.read()
    except Exception as e:
        print(f"[CURATOR] Failed to read prompt: {e}")
        return {
            "curator_report": {"approved": False, "score": 0.0,
                               "feedback": "Internal error: missing evaluation criteria.",
                               "iteration": iterations},
            "iterations_count": iterations,
        }

    context = (
        f"TRACK SPECIFICATION:\n"
        f"- BPM: {track_spec.get('bpm', 'N/A')}\n"
        f"- Key: {track_spec.get('key', 'N/A')}\n"
        f"- Energy: {track_spec.get('energy', 'N/A')}\n"
        f"- Mood: {track_spec.get('mood', 'N/A')}\n"
        f"- Iteration: {iterations} / 3\n"
        f"\n"
        f"ANALYSIS METRICS:\n"
        f"{json.dumps(analysis, indent=2)}\n"
        f"\n"
        f"REFERENCE TASTE PROFILE THRESHOLDS:\n"
        f"{json.dumps(taste_profile.get('metrics', {}), indent=2)}\n"
        f"\n"
        f"PREVIOUS FEEDBACK:\n"
        f"{json.dumps(previous_report.get('feedback', 'None'), indent=2)}\n"
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

        result = json.loads(content)

        report = {
            "approved": bool(result.get("approved", False)),
            "score": float(result.get("score", 0.0)),
            "feedback": result.get("feedback", {}),
            "metrics": result.get("metrics", {}),
            "iteration": iterations,
        }

        print(f"[CURATOR] Score={report['score']:.2f}, "
              f"approved={report['approved']}")
        return {"curator_report": report, "iterations_count": iterations}

    except json.JSONDecodeError as e:
        print(f"[CURATOR] JSON parse failed: {e}")
        return _fallback_evaluation(analysis, taste_profile, iterations)
    except ImportError as e:
        print(f"[CURATOR] LLM dependencies missing: {e}")
        return _fallback_evaluation(analysis, taste_profile, iterations)
    except Exception as e:
        print(f"[CURATOR] LLM call failed: {e}")
        return _fallback_evaluation(analysis, taste_profile, iterations)


def _fallback_evaluation(
    analysis: Dict[str, float],
    taste_profile: Dict[str, Any],
    iterations: int,
) -> Dict[str, Any]:
    metrics_config = taste_profile.get("metrics", {})
    score = 1.0
    violations = []

    for metric, config in metrics_config.items():
        value = analysis.get(metric)
        if value is None:
            continue
        min_t = config.get("min_threshold")
        max_t = config.get("max_threshold")
        strict = config.get("strict", False)
        penalty = 0.25 if strict else 0.10

        if min_t is not None and value < min_t:
            score -= penalty
            violations.append(f"{metric}={value:.2f} < min={min_t}")
        if max_t is not None and value > max_t:
            score -= penalty
            violations.append(f"{metric}={value:.2f} > max={max_t}")

    score = max(0.0, min(1.0, score))
    approved = score >= 0.70
    feedback = "; ".join(violations) if violations else "All metrics within acceptable ranges."

    report = {
        "approved": approved,
        "score": score,
        "feedback": feedback,
        "iteration": iterations,
    }

    print(f"[CURATOR] Fallback evaluation: score={score:.2f}, "
          f"approved={approved}, violations={len(violations)}")
    return {"curator_report": report, "iterations_count": iterations}
