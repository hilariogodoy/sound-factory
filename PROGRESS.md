# Audio Warehouse Engine - Progress Tracker

> **State Preservation Protocol**: This file is the single source of truth for cross-session context.
> Always read before starting work.
> Always append the updated version at the end of every session.

---

## Project Status Summary

| Phase | Sessions | Status |
|---|---|---|
| Phase 1 - Functional Skeleton | 1-2 | In Progress (1/2 complete) |
| Phase 2 - Core Engines | 3-4 | Not Started |
| Phase 3 - Medallion Agents | 5-7 | Not Started |
| Phase 4 - Closure & Curating Loop | 8-9 | Not Started |

---

## Session Log

| # | Session Name | Status | Date Completed | Verdict |
|---|---|---|---|---|
| 1 | Project Scaffold, State Types & LLM Factory | Completed | 2026-06-15 | PASS - All 6 nodes execute sequentially, graph terminates at END, dry-run works |
| 2 | LangGraph State Machine with Mock Nodes | Not Started | - | - |
| 3 | Audio Compiler (Subprocess Executor) | Not Started | - | - |
| 4 | Librosa Feature Extraction Analyzer | Not Started | - | - |
| 5 | Bronze Designer Agent | Not Started | - | - |
| 6 | Silver Sequencer Agent | Not Started | - | - |
| 7 | Gold Mixer Agent | Not Started | - | - |
| 8 | Taste Curator & Circuit Breaker | Not Started | - | - |
| 9 | Orchestrator, CLI & Full Integration | Not Started | - | - |

---

## File Manifest (Truth of Record)

Each session MUST update this table with any new or modified files.

| File Path | Status | Created In | Notes |
|---|---|---|---|
| `requirements.txt` | Created | Session 1 | Pinned deps; numpy/pyo need Python<3.13 |
| `config/llm_config.yaml` | Created | Session 1 | Provider selection (default: openai_compatible) |
| `config/reference_taste_profile.json` | Created | Session 1 | 4 Librosa thresholds from PRD |
| `config/system_prompts/bronze_designer.txt` | Created (stub) | Session 1 | Output schema only; full prompt in Session 5 |
| `config/system_prompts/silver_sequencer.txt` | Created (stub) | Session 1 | Output schema only; full prompt in Session 6 |
| `config/system_prompts/gold_mixer.txt` | Created (stub) | Session 1 | Output schema only; full prompt in Session 7 |
| `config/system_prompts/curator_critic.txt` | Created (stub) | Session 1 | Output schema only; full prompt in Session 8 |
| `src/__init__.py` | Created | Session 1 | Empty |
| `src/llm_factory.py` | Created | Session 1 | get_llm() factory - full implementation |
| `src/agents/__init__.py` | Created | Session 1 | Empty |
| `src/agents/orchestrator.py` | Created (stub) | Session 1 | Returns {}; full impl in Session 2 |
| `src/agents/bronze_agent.py` | Created (stub) | Session 1 | Returns {}; full impl in Session 5 |
| `src/agents/silver_agent.py` | Created (stub) | Session 1 | Returns {}; full impl in Session 6 |
| `src/agents/gold_agent.py` | Created (stub) | Session 1 | Returns {}; full impl in Session 7 |
| `src/agents/curator_agent.py` | Created (stub) | Session 1 | Returns {}; full impl in Session 8 |
| `src/audio_engine/__init__.py` | Created | Session 1 | Empty |
| `src/audio_engine/compiler.py` | Created (stub) | Session 1 | Returns {}; full impl in Session 3 |
| `src/audio_engine/analyzer.py` | Created (stub) | Session 1 | Returns {}; full impl in Session 4 |
| `src/graph.py` | Created (linear chain) | Session 1 | StateGraph with 6 nodes -> linear edges to END |
| `src/main.py` | Created (basic) | Session 1 | argparse + invoke + print; finalize in Session 9 |
| `warehouse/bronze_patches/.gitkeep` | Created | Session 1 | Placeholder |
| `warehouse/silver_loops/.gitkeep` | Created | Session 1 | Placeholder |
| `warehouse/gold_outputs/track_001/json_manifest.json` | Created | Session 1 | Placeholder |
| `README.md` | Not Created | Session 9 | Documentation |
| `.github/workflows/compile_music.yml` | Not Created | Session 9 | CI pipeline |
| `PROGRESS.md` | Created | Session 0 | This file |

---

## Context Anchor (for next session: **Session 2**)

### What exists at the start of Session 2

The full project skeleton at `audio-warehouse-engine/`:

```
audio-warehouse-engine/
|-- requirements.txt
|-- config/
|   |-- llm_config.yaml
|   |-- reference_taste_profile.json
|   |-- system_prompts/
|       |-- bronze_designer.txt   (stub - output schema only)
|       |-- silver_sequencer.txt  (stub)
|       |-- gold_mixer.txt        (stub)
|       |-- curator_critic.txt    (stub)
|-- src/
|   |-- __init__.py
|   |-- llm_factory.py            (full impl - get_llm)
|   |-- graph.py                   (linear chain - no conditional routing)
|   |-- main.py                    (basic CLI with --dry-run)
|   |-- agents/
|   |   |-- __init__.py
|   |   |-- orchestrator.py       (stub: returns {})
|   |   |-- bronze_agent.py       (stub: returns {})
|   |   |-- silver_agent.py       (stub: returns {})
|   |   |-- gold_agent.py         (stub: returns {})
|   |   |-- curator_agent.py      (stub: returns {})
|   |-- audio_engine/
|       |-- __init__.py
|       |-- compiler.py           (stub: returns {})
|       |-- analyzer.py           (stub: returns {})
|-- warehouse/
|   |-- bronze_patches/.gitkeep
|   |-- silver_loops/.gitkeep
|   |-- gold_outputs/track_001/json_manifest.json
```

### Key architectural notes from Session 1

1. **LangGraph 0.0.15 does NOT accept `recursion_limit` as a compile() kwarg** - must be avoided
2. **LangGraph 0.0.15 validates all registered nodes are reachable** - no orphan nodes allowed
3. **Session 1 graph uses linear edges only** (no conditional routing) to satisfy validation with stubs
4. **Python 3.13 detected** - numpy 1.24.3 and pyo 1.0.5 are incompatible; alternative versioning needed for Sessions 3, 4, 5+

### Exact signatures Session 2 must work with

```python
# graph.py imports:
from src.agents.orchestrator import orchestrator_node
from src.agents.bronze_agent import bronze_designer_node
from src.agents.silver_agent import silver_sequencer_node
from src.agents.gold_agent import gold_mixer_node
from src.agents.curator_agent import curator_node
from src.audio_engine.compiler import execute_audio_compilation

# All agent/engine stubs currently return {} - Session 2 replaces
# orchestrator.py, curator_agent.py with real implementations

# main.py builds initial AudioWarehouseState with:
initial_state = {
    "track_specification": {"bpm", "key", "energy", "mood", "track_id", "human_feedback"},
    "active_branch_name": "",
    "bronze_instruments": {},
    "silver_patterns": {},
    "gold_arrangement": "",
    "compilation_errors": [],
    "curator_report": {},
    "iterations_count": 0,
}
```

### What Session 2 needs to do

1. Implement `orchestrator.py` - set `active_branch_name`, `iterations_count=0`, `compilation_errors=[]`, create dirs
2. Implement `curator_agent.py` with mock approval/rejection + iteration counter increment
3. Replace linear edges with `add_conditional_edges` routing (curator -> approve/retry/error_termination)
4. Implement `error_termination_node` that writes failure manifest
5. Add `print()` traceability in all 6 agent stubs so the console shows the execution path
6. Verify graph loops correctly (mock reject -> 3 iterations -> error_termination)
7. Verify graph terminates on approval

### Dependency chain reminder

```
Session 2 (conditional routing) <- Session 3 (needs graph to handle loop/end)
Session 3 (compiler) <- Session 4 (needs WAV output to analyze)
Session 4 (analyzer) <- Session 5 (analyzer feeds curator which drives bronze)
Session 5 (bronze) <- Session 6 (needs bronze_instruments)
Session 6 (silver) <- Session 7 (needs silver_patterns)
Session 7 (gold) <- Session 8 (needs gold_arrangement)
Session 8 (curator) <- Session 9 (needs all nodes complete)
```

---

## Architectural Decision Log

| ID | Decision | Rationale | Session |
|---|---|---|---|
| ADR-001 | LLM calls route through src/llm_factory.py only | Zero vendor coupling; provider swap via env var or YAML | Session 1 |
| ADR-002 | LangGraph 0.0.15 API with StateGraph + string keys | Explicit version pin; no Command objects | Session 1 |
| ADR-003 | Server(audio="offline") for Pyo | Headless/CI-compatible rendering, no sound card needed | Session 7 |
| ADR-004 | Subprocess isolation for audio compilation | Prevents Pyo segfaults from killing orchestrator | Session 3 |
| ADR-005 | JSON parse safety with empty-fallback in all agents | Prevents graph crash on malformed LLM output | Sessions 5-8 |
| ADR-006 | Circuit breaker at 3 iterations | Prevents runaway token burn on unrecoverable tracks | Session 8 |
| ADR-007 | sys.path insertion in main.py | Allows direct execution without editable pip installs | Session 1 |
| ADR-008 | Linear edge graph in Session 1 (no conditional) | LangGraph 0.0.15 validates reachability; orphan error_termination blocked compile | Session 1 |
| ADR-009 | requirements.txt pinned for Python<3.13; runtime is Python 3.13 | numpy 1.24.3 and pyo 1.0.5 need older Python; use relaxed pinning for development | Session 1 |

---

## Known Issues & Pitfalls

| Issue | Affects | Workaround |
|---|---|---|
| Pyo requires python>=3.9,<3.13 on Windows; runtime=3.13 | Sessions 3, 7, 9 | Use Python 3.10 virtualenv; or find pyo wheels for 3.13 |
| numpy 1.24.3 does not build on Python 3.13 | Session 4 | Pin numpy>=2.0 for 3.13; or use Python 3.10 |
| LangGraph 0.0.15 compile() does NOT support recursion_limit kwarg | All sessions | Use default recursion; add explicit stop conditions in routing logic |
| LangGraph 0.0.15 validates all nodes reachable at compile() time | Session 1, 2 | Dangling nodes (error_termination without incoming edge) break compile |
| Stubs returning {} mean state never mutates | Sessions 1 | Graph cannot use conditional routing until at least curator increments iterations_count |

---

## Verification Results (Session 1)

```powershell
# Dry run - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run
> [DRY RUN] Node sequence that would execute:
>   1. orchestrator
>   2. bronze_designer
>   3. silver_sequencer
>   4. gold_mixer
>   5. audio_compiler
>   6. taste_curator
>   7. conditional_edge

# Full invocation with stubs - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
> [SESSION COMPLETE]
>   Track ID:       track_001
>   BPM:            133
>   Key:            A minor
>   Iterations:     0
>   Approved:       N/A
>   Compilation errors: 0
```

---

## Verification Checklist (Global)

Run this at the end of every session:

```powershell
# 1. No import errors
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run

# 2. requirements.txt is installable
pip install -r requirements.txt --dry-run

# 3. Full invocation completes
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
```
