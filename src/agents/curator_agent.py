from typing import Dict, Any


def curator_node(state: Dict[str, Any]) -> Dict[str, Any]:
    iterations = state.get("iterations_count", 0) + 1

    report = {
        "approved": False,
        "score": 0.4,
        "feedback": "Mock rejection — insufficient spectral variety and rhythmic drive.",
        "iteration": iterations,
    }

    print(f"[CURATOR] Iteration {iterations}: score={report['score']}, "
          f"approved={report['approved']}")
    print(f"[CURATOR] Feedback: {report['feedback']}")

    return {
        "curator_report": report,
        "iterations_count": iterations,
    }
