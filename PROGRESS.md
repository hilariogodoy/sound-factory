# Audio Warehouse Engine - Progress Tracker

> **State Preservation Protocol**: This file is the single source of truth for cross-session context.
> Always read before starting work.
> Always append the updated version at the end of every session.

---

## Project Status Summary

| Phase | Sessions | Status |
|---|---|---|
| Phase 1 - Functional Skeleton | 1-2 | Completed |
| Phase 2 - Core Engines | 3-4 | Not Started |
| Phase 3 - Medallion Agents | 5-7 | Not Started |
| Phase 4 - Closure & Curating Loop | 8-9 | Not Started |

---

## Session Log

| # | Session Name | Status | Date Completed | Verdict |
|---|---|---|---|---|
| 1 | Project Scaffold, State Types & LLM Factory | Completed | 2026-06-15 | PASS - All 6 nodes execute sequentially, graph terminates at END, dry-run works |
| 2 | LangGraph State Machine with Mock Nodes | Completed | 2026-06-16 | PASS - Conditional routing with circuit breaker (3 iterations -> error_termination); approval path verified; orchestrator creates dirs and sets branch name |
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
|---|---|---|---|---|
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
| `src/agents/orchestrator.py` | Modified (full impl) | Session 2 | Creates dirs, sets branch_name, resets iterations/errors |
| `src/agents/bronze_agent.py` | Modified (stub + print) | Session 2 | Traceability print added; returns {} until Session 5 |
| `src/agents/silver_agent.py` | Modified (stub + print) | Session 2 | Traceability print added; returns {} until Session 6 |
| `src/agents/gold_agent.py` | Modified (stub + print) | Session 2 | Traceability print added; returns {} until Session 7 |
| `src/agents/curator_agent.py` | Modified (full mock) | Session 2 | Always rejects; increments iterations_count; full impl in Session 8 |
| `src/audio_engine/__init__.py` | Created | Session 1 | Empty |
| `src/audio_engine/compiler.py` | Modified (stub + print) | Session 2 | Traceability print added; returns {} until Session 3 |
| `src/audio_engine/analyzer.py` | Created (stub) | Session 1 | Returns {}; full impl in Session 4 |
| `src/graph.py` | Modified (conditional routing) | Session 2 | add_conditional_edges + error_termination_node; circuit breaker at 3 iterations |
| `src/main.py` | Modified (recursion_limit, dry-run text) | Session 2 | Passes recursion_limit=100 to invoke(); updated dry-run display |
| `warehouse/bronze_patches/.gitkeep` | Created | Session 1 | Placeholder |
| `warehouse/silver_loops/.gitkeep` | Created | Session 1 | Placeholder |
| `warehouse/gold_outputs/track_001/json_manifest.json` | Created | Session 1 | Placeholder |
| `README.md` | Not Created | Session 9 | Documentation |
| `.github/workflows/compile_music.yml` | Not Created | Session 9 | CI pipeline |
| `PROGRESS.md` | Created | Session 0 | This file |

---

## Context Anchor (for next session: **Session 3**)

### What exists at the start of Session 3

The full project skeleton with conditional routing and circuit breaker:

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
|   |-- graph.py                   (conditional routing + error_termination node)
|   |-- main.py                    (CLI with --dry-run, recursion_limit=100)
|   |-- agents/
|   |   |-- __init__.py
|   |   |-- orchestrator.py       (full impl: creates dirs, sets branch)
|   |   |-- bronze_agent.py       (stub with print)
|   |   |-- silver_agent.py       (stub with print)
|   |   |-- gold_agent.py         (stub with print)
|   |   |-- curator_agent.py      (mock: always reject, increments iterations)
|   |-- audio_engine/
|       |-- __init__.py
|       |-- compiler.py           (stub with print)
|       |-- analyzer.py           (stub: returns {})
|-- warehouse/
|   |-- bronze_patches/.gitkeep
|   |-- silver_loops/.gitkeep
|   |-- gold_outputs/track_001/json_manifest.json
```

### Key architectural notes from Session 2

1. **`recursion_limit` must be passed to `invoke()`, not `compile()`** — `invoke(initial_state, {"recursion_limit": 100})` works; `compile(recursion_limit=100)` crashes.
2. **`add_conditional_edges` maps return values to node strings** — the router function returns `"bronze_designer"`, `"error_termination"`, or `"__end__"` (END).
3. **Circuit breaker at 3 iterations** — `iterations_count >= 3` routes to `error_termination` before checking approval.
4. **Orchestrator creates per-branch subdirs** — `warehouse/bronze_patches/{branch}/`, `warehouse/silver_loops/{branch}/`, `warehouse/gold_outputs/{track_id}/`.
5. **Python 3.13 issue persists** — numpy 1.24.3 and pyo 1.0.5 still incompatible; use Python 3.10 venv for Sessions 3+.

### Exact signatures Session 3 must work with

```python
# graph.py imports:
from src.agents.orchestrator import orchestrator_node
from src.agents.bronze_agent import bronze_designer_node
from src.agents.silver_agent import silver_sequencer_node
from src.agents.gold_agent import gold_mixer_node
from src.agents.curator_agent import curator_node
from src.audio_engine.compiler import execute_audio_compilation  # <-- Session 3 replaces this

# All agent stubs return {} except orchestrator and curator.
# compiler.py stub currently prints and returns {}.
# graph.py has conditional routing with retry loop.
```

### What Session 3 needs to do

1. Implement `compiler.py` — subprocess execution of a Pyo Python script → `.wav` output
2. Write a minimal Pyo test script that generates a simple tone/sound and verify subprocess isolation
3. Store WAV output in `warehouse/silver_loops/{branch}/` or `warehouse/gold_outputs/{track_id}/`
4. Capture compilation stdout/stderr; populate `compilation_errors` on failure
5. Update `execute_audio_compilation` signature: write WAV, return `{"gold_arrangement": wav_path}` on success
6. Verify the graph compiles and runs with the real compiler (mock reject still can test)
7. Add ADR for subprocess isolation strategy and chosen Python/pyo invocation pattern

### Dependency chain reminder

```
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
| ADR-010 | recursion_limit passed as config to invoke(), not compile() | LangGraph 0.0.15 compile() silently ignores recursion_limit kwarg; invoke() config dict works | Session 2 |

---

## Known Issues & Pitfalls

| Issue | Affects | Workaround |
|---|---|---|
| Pyo requires python>=3.9,<3.13 on Windows; runtime=3.13 | Sessions 3, 7, 9 | Use Python 3.10 virtualenv; or find pyo wheels for 3.13 |
| numpy 1.24.3 does not build on Python 3.13 | Session 4 | Pin numpy>=2.0 for 3.13; or use Python 3.10 |
| LangGraph 0.0.15 compile() does NOT support recursion_limit kwarg | All sessions | Pass recursion_limit in invoke() config dict instead |
| LangGraph 0.0.15 validates all nodes reachable at compile() time | Session 1, 2 | Dangling nodes (error_termination without incoming edge) break compile |
| Stubs returning {} mean state never mutates | Sessions 1 | Graph cannot use conditional routing until at least curator increments iterations_count |
| Default recursion_limit (25) too low for 3-iteration retry loop | Sessions 2, 3+ | Pass `{"recursion_limit": 100}` to invoke(); adjust if more loops needed |

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

## Verification Results (Session 2)

```powershell
# Dry run - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run
> [DRY RUN] Graph structure:
>   Primary: orchestrator -> bronze_designer -> silver_sequencer ->
>            gold_mixer -> audio_compiler -> taste_curator
>   Conditional routing from taste_curator:
>     - approved (score >= 0.7):         -> END
>     - rejected (score < 0.7, iters<3): -> bronze_designer (retry)
>     - rejected (iters >= 3):           -> error_termination -> END

# Circuit breaker test (mock reject -> 3 iterations -> error_termination) - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
> [Output truncated]
> [CURATOR] Iteration 3: score=0.4, approved=False
> [ROUTER] iterations_count=3 >= 3 -> error_termination
> [ERROR_TERMINATION] Circuit breaker tripped after 3 iteration(s)
> [ERROR_TERMINATION] Failure manifest written to warehouse\gold_outputs\track_001\failure_manifest.json
> [SESSION COMPLETE]
>   Iterations:     3
>   Approved:       False
>   Score:          0.4
>   Compilation errors: 0

# Approval path test (curator returns approved=True) - PASS
python src/main.py --bpm 130 --key "C major" --energy 0.9 --mood "dark"  # (with curator modified to approve on iter 2)
> [CURATOR] Iteration 2: score=0.8, approved=True
> [ROUTER] Curator approved -> END
> [SESSION COMPLETE]
>   Iterations:     2
>   Approved:       True
>   Score:          0.8
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
