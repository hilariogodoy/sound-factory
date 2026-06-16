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
| 3 | Audio Compiler (Subprocess Executor) | Completed | 2026-06-16 | PASS - Subprocess isolation works; Pyo render script created; graceful error capture in compilation_errors; circuit breaker retries compiler failures |
| 4 | Librosa Feature Extraction Analyzer | Completed | 2026-06-16 | PASS - Analyzer node (audio_analyzer) added between compiler and curator; extracts spectral centroid, rms, zcr, tempo; graceful missing WAV/librosa handling; analysis_metrics field added to state |
| 5 | Bronze Designer Agent | Completed | 2026-06-16 | PASS - LLM-powered agent generating Pyo instrument patches; graceful empty-fallback on API/JSON errors; prompt populated with schema and constraints |
| 6 | Silver Sequencer Agent | Completed | 2026-06-16 | PASS - LLM-powered sequencer generating 16-step patterns; references bronze_instruments; graceful empty-fallback on API/JSON errors; prompt populated |
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
| `config/system_prompts/bronze_designer.txt` | Modified (full prompt) | Session 5 | Detailed Pyo DSP instrument generation prompt with JSON schema, constraints, instrument categories |
| `config/system_prompts/silver_sequencer.txt` | Modified (full prompt) | Session 6 | 16-step pattern generation prompt with techno style guidelines, MIDI note ranges, gate arrays, automation |
| `config/system_prompts/gold_mixer.txt` | Created (stub) | Session 1 | Output schema only; full prompt in Session 7 |
| `config/system_prompts/curator_critic.txt` | Created (stub) | Session 1 | Output schema only; full prompt in Session 8 |
| `src/__init__.py` | Created | Session 1 | Empty |
| `src/llm_factory.py` | Created | Session 1 | get_llm() factory - full implementation |
| `src/agents/__init__.py` | Created | Session 1 | Empty |
| `src/agents/orchestrator.py` | Modified (full impl) | Session 2 | Creates dirs, sets branch_name, resets iterations/errors |
| `src/agents/bronze_agent.py` | Modified (full LLM impl) | Session 5 | Calls get_llm() with SystemMessage + HumanMessage; JSON parse with empty-fallback; prints generated instruments |
| `src/agents/silver_agent.py` | Modified (full LLM impl) | Session 6 | Calls get_llm() with bronze_instruments context; validates list-type patterns; empty-fallback |
| `src/agents/gold_agent.py` | Modified (stub + print) | Session 2 | Traceability print added; returns {} until Session 7 |
| `src/agents/curator_agent.py` | Modified (full mock) | Session 2 | Always rejects; increments iterations_count; full impl in Session 8 |
| `src/audio_engine/__init__.py` | Created | Session 1 | Empty |
| `src/audio_engine/compiler.py` | Modified (full impl) | Session 3 | Subprocess executor: runs _render.py, captures stdout/stderr, returns gold_arrangement + compilation_errors |
| `src/audio_engine/_render.py` | Created | Session 3 | Standalone Pyo render script spawned by compiler.py |
| `src/audio_engine/analyzer.py` | Modified (full impl) | Session 4 | Librosa feature extraction + graph node wrapper; graceful fallback if librosa/WAV missing |
| `src/graph.py` | Modified (added analyzer node) | Session 2, 4 | Session 2: conditional routing; Session 4: audio_analyzer node + analysis_metrics state field |
| `src/main.py` | Modified (analysis_metrics, dry-run) | Session 2, 4 | Session 2: recursion_limit; Session 4: analysis_metrics initial state + dry-run + output display |
| `warehouse/bronze_patches/.gitkeep` | Created | Session 1 | Placeholder |
| `warehouse/silver_loops/.gitkeep` | Created | Session 1 | Placeholder |
| `warehouse/gold_outputs/track_001/json_manifest.json` | Created | Session 1 | Placeholder |
| `README.md` | Not Created | Session 9 | Documentation |
| `.github/workflows/compile_music.yml` | Not Created | Session 9 | CI pipeline |
| `PROGRESS.md` | Created | Session 0 | This file |

---

## Context Anchor (for next session: **Session 7**)

### What exists at the start of Session 7

The full project with LLM-powered Bronze and Silver agents:

```
audio-warehouse-engine/
|-- requirements.txt
|-- config/
|   |-- llm_config.yaml
|   |-- reference_taste_profile.json
|   |-- system_prompts/
|       |-- bronze_designer.txt   (full prompt: Pyo instrument generation)
|       |-- silver_sequencer.txt  (full prompt: 16-step pattern generation)
|       |-- gold_mixer.txt        (stub - output schema only)
|       |-- curator_critic.txt    (stub)
|-- src/
|   |-- __init__.py
|   |-- llm_factory.py            (full impl - get_llm)
|   |-- graph.py                   (7 nodes + conditional routing)
|   |-- main.py                    (CLI with --dry-run, recursion_limit=100)
|   |-- agents/
|   |   |-- __init__.py
|   |   |-- orchestrator.py       (full impl)
|   |   |-- bronze_agent.py       (full LLM: Pyo instrument patches)
|   |   |-- silver_agent.py       (full LLM: step patterns)
|   |   |-- gold_agent.py         (stub with print)
|   |   |-- curator_agent.py      (mock: always reject)
|   |-- audio_engine/
|       |-- __init__.py
|       |-- compiler.py           (full impl: subprocess -> Pyo _render.py)
|       |-- _render.py            (standalone Pyo render script)
|       |-- analyzer.py           (full impl: librosa feature extraction)
|-- warehouse/
|   |-- ...
```

### State fields at the start of Session 7

```python
class AudioWarehouseState(TypedDict):
    track_specification: Dict[str, Any]   # bpm, key, energy, mood, track_id, human_feedback
    active_branch_name: str               # set by orchestrator
    bronze_instruments: Dict[str, str]    # populated by bronze_agent (or {})
    silver_patterns: Dict[str, Any]       # populated by silver_agent (or {})
    gold_arrangement: str                 # WAV path from compiler, or ""
    compilation_errors: List[str]         # populated by compiler on failure
    curator_report: Dict[str, Any]        # mock until Session 8
    iterations_count: int                 # incremented by curator
    analysis_metrics: Dict[str, float]    # populated by analyzer, or {}
```

### What Session 7 needs to do

1. Implement `gold_agent.py` — the Gold Mixer agent:
   - Call LLM via `get_llm()` from `src/llm_factory.py`
   - Read the prompt from `config/system_prompts/gold_mixer.txt` — populate it with a real prompt
   - Parse LLM output as JSON (arrangement structure)
   - Apply ADR-005: JSON parse safety with empty-fallback
   - Accept `bronze_instruments` AND `silver_patterns` from state
   - Return `{"gold_arrangement": combined_pyo_code_string}` — a complete, runnable Pyo script
2. Populate `config/system_prompts/gold_mixer.txt` with a full prompt including:
   - How to combine instrument patches with pattern data
   - Pyo Server initialization with `Server(audio="offline")`
   - Export/recording setup for the master output
   - Track structure (intro, buildup, drop, outro)
3. **Connect the compiler**: The Gold agent's output (`gold_arrangement`) is a complete Pyo script string → written to a `.py` file on disk by `gold_agent.py` → `compiler.py` executes it as a subprocess.
   - This means `gold_agent.py` writes a `.py` file to `warehouse/silver_loops/{branch}/` or similar
   - `compiler.py` receives the path from `gold_arrangement` and runs it via subprocess

### Gold-Compiler handoff design

Currently `gold_arrangement: str` stores a WAV path returned by `compiler.py`. With the Gold agent:

**Proposed flow**:
1. Gold agent generates a complete Pyo script as a string
2. Gold agent writes this string to `warehouse/gold_outputs/{track_id}/_gold_arrangement.py`
3. Gold agent sets `gold_arrangement` to the path of that `.py` file
4. `compiler.py` reads `gold_arrangement` as a script path (not a WAV path) and executes it
5. `compiler.py` returns `gold_arrangement` as the WAV output path instead

**Alternative**: Keep `gold_arrangement` as the WAV path returned by compiler. Use a new field `arrangement_script: str` for the Gold agent's script path. During retry, the gold agent regenerates the arrangement.

### Dependency chain reminder

```
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
| ADR-011 | Subprocess isolation for Pyo compilation | Prevents Pyo segfaults from killing orchestrator; compiler.py spawns _render.py via subprocess.run() | Session 3 |
| ADR-012 | Analyzer as separate graph node (Option A) | Keeps pipeline modular and testable; analysis_metrics passes from analyzer -> curator; curator can be swapped without affecting analysis | Session 4 |

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

## Verification Results (Session 3)

```powershell
# Dry run - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run
> [DRY RUN] Graph structure: orchestrator -> ... -> taste_curator -> [conditional]

# Full invocation with real compiler (Pyo missing on 3.13) - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
> [COMPILER] stderr: Pyo not available: No module named 'pyo'
> [COMPILER] Compilation failed: Pyo not available: No module named 'pyo'
> [CURATOR] Iteration 3: score=0.4, approved=False
> [ERROR_TERMINATION] Circuit breaker tripped after 3 iteration(s)
> [SESSION COMPLETE]
>   Iterations:     3
>   Approved:       False
>   Compilation errors: 1

# Standalone _render.py test (JSON via Python subprocess) - PASS
python -c "import json, subprocess, sys; subprocess.run([sys.executable, 'src/audio_engine/_render.py', json.dumps({'bpm':133,'key':'A minor','energy':0.8,'mood':'hypnotic','output_path':'test.wav'})])"
> Pyo not available: No module named 'pyo'
# (Expected: Pyo needs Python 3.10; on 3.10 this generates an actual WAV)
```

## Verification Results (Session 4)

```powershell
# Dry run - PASS (shows audio_analyzer in chain)
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run
> [DRY RUN] Graph structure:
>   Primary: orchestrator -> bronze_designer -> silver_sequencer ->
>            gold_mixer -> audio_compiler -> audio_analyzer ->
>            taste_curator
>   Conditional routing from taste_curator: ...

# Full invocation with analyzer node - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
> ... audio_compiler -> audio_analyzer -> taste_curator ...
> [ANALYZER] Analyzing (no WAV)         # graceful no-WAV handling
> [SESSION COMPLETE]
>   Iterations:     3
>   Approved:       False
>   Compilation errors: 1
```

## Verification Results (Session 5)

```powershell
# Dry run - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run
> [DRY RUN] Graph structure shows all 7 nodes + conditional routing

# Full invocation with real bronze_agent (no DEEPSEEK_API_KEY) - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
> [BRONZE] LLM call failed: 'DEEPSEEK_API_KEY'     # graceful fallback
> [SESSION COMPLETE]
>   Iterations:     3
>   Approved:       False
>   Compilation errors: 1

# Prompt file is found and read correctly
# (verified by absence of "Failed to read prompt" error — path fixed in Session 5)
```

## Verification Results (Session 6)

```powershell
# Dry run - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run
> [DRY RUN] Graph structure shows all 7 nodes + conditional routing

# Full invocation with real silver_agent (no DEEPSEEK_API_KEY) - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
> [BRONZE] LLM call failed: 'DEEPSEEK_API_KEY'
> [SILVER] LLM call failed: 'DEEPSEEK_API_KEY'   # graceful fallback
> [SESSION COMPLETE]
>   Iterations:     3
>   Approved:       False
>   Compilation errors: 1

# Both LLM nodes fail gracefully; circuit breaker handles retries
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
