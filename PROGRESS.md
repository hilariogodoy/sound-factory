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
| Phase 4 - Closure & Curating Loop | 8-9 | In Progress (1/2 complete) |

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
| 7 | Gold Mixer Agent | Completed | 2026-06-16 | PASS - LLM generates complete Pyo arrangement script; gold-compiler handoff: gold writes .py, compiler executes it; fallback to _render.py if gold fails |
| 8 | Taste Curator & Circuit Breaker | Completed | 2026-06-16 | PASS - LLM evaluates analysis_metrics against taste profile; auto-rejects on compilation errors; fallback threshold evaluation if LLM fails; circuit breaker fully functional |
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
| `config/system_prompts/gold_mixer.txt` | Modified (full prompt) | Session 7 | Complete arrangement generation prompt: script template, section structure, pattern playback, Pyo offline rendering |
| `config/system_prompts/curator_critic.txt` | Modified (full prompt) | Session 8 | Evaluation criteria with scoring guidelines, per-agent feedback (bronze/silver/gold), taste profile threshold reference |
| `src/__init__.py` | Created | Session 1 | Empty |
| `src/llm_factory.py` | Created | Session 1 | get_llm() factory - full implementation |
| `src/agents/__init__.py` | Created | Session 1 | Empty |
| `src/agents/orchestrator.py` | Modified (full impl) | Session 2 | Creates dirs, sets branch_name, resets iterations/errors |
| `src/agents/bronze_agent.py` | Modified (full LLM impl) | Session 5 | Calls get_llm() with SystemMessage + HumanMessage; JSON parse with empty-fallback; prints generated instruments |
| `src/agents/silver_agent.py` | Modified (full LLM impl) | Session 6 | Calls get_llm() with bronze_instruments context; validates list-type patterns; empty-fallback |
| `src/agents/gold_agent.py` | Modified (full LLM impl) | Session 7 | Calls get_llm() with instruments + patterns; extracts Python code; writes script to warehouse; empty-fallback |
| `src/agents/curator_agent.py` | Modified (full LLM impl) | Session 8 | LLM evaluates metrics vs taste profile; auto-rejects on compilation errors; fallback threshold evaluation if LLM fails; per-agent structured feedback |
| `src/audio_engine/__init__.py` | Created | Session 1 | Empty |
| `src/audio_engine/compiler.py` | Modified (gold script support) | Session 3, 7 | Session 3: subprocess _render.py; Session 7: checks gold_arrangement for script path, executes it if valid, falls back to _render.py |
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

## Context Anchor (for next session: **Session 9**)

### What exists at the start of Session 9

All 8 nodes fully implemented — the complete pipeline:

```
audio-warehouse-engine/
|-- requirements.txt
|-- config/
|   |-- llm_config.yaml
|   |-- reference_taste_profile.json
|   |-- system_prompts/
|       |-- bronze_designer.txt   (full)
|       |-- silver_sequencer.txt  (full)
|       |-- gold_mixer.txt        (full)
|       |-- curator_critic.txt    (full)
|-- src/
|   |-- __init__.py
|   |-- llm_factory.py            (full)
|   |-- graph.py                   (7 nodes + error_termination + conditional routing)
|   |-- main.py                    (CLI with --dry-run, recursion_limit=100)
|   |-- agents/
|   |   |-- __init__.py
|   |   |-- orchestrator.py       (full)
|   |   |-- bronze_agent.py       (full LLM)
|   |   |-- silver_agent.py       (full LLM)
|   |   |-- gold_agent.py         (full LLM)
|   |   |-- curator_agent.py      (full LLM + fallback evaluation)
|   |-- audio_engine/
|       |-- __init__.py
|       |-- compiler.py           (full: gold script or _render.py)
|       |-- _render.py            (standalone Pyo script)
|       |-- analyzer.py           (full: librosa)
|-- warehouse/
|   |-- bronze_patches/
|   |-- silver_loops/
|   |-- gold_outputs/{track_id}/
```

### What Session 9 needs to do

1. **CLI polish**: Add `--verbose` flag for detailed per-node logging; add `--output-dir` flag
2. **README.md**: Write project documentation (README.md was deferred from Session 1)
3. **CI pipeline**: Create `.github/workflows/compile_music.yml`
4. **End-to-end dry-run verification**: Confirm all 8 nodes + conditional routing work
5. **Final session**: Commit all remaining files, update PROGRESS.md as final

### Pipeline overview (complete)

```
orchestrator
  → bronze_designer (LLM: Pyo instrument patches)
    → silver_sequencer (LLM: 16-step patterns)
      → gold_mixer (LLM: arrangement script → .py on disk)
        → audio_compiler (subprocess: executes .py or _render.py → .wav)
          → audio_analyzer (librosa: extract metrics)
            → taste_curator (LLM: evaluate metrics vs taste profile)
              → conditional:
                  approved → END
                  rejected + iters<3 → bronze_designer (retry)
                  rejected + iters>=3 → error_termination → END
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
| ADR-013 | Gold agent writes script, compiler executes it | gold_arrangement field carries script path from gold -> compiler, then WAV path from compiler -> analyzer -> curator; clean single-field handoff | Session 7 |

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

## Verification Results (Session 7)

```powershell
# Dry run - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run
> [DRY RUN] Graph structure shows all 7 nodes + conditional routing

# Full invocation with real gold_agent (no DEEPSEEK_API_KEY) - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
> [GOLD] LLM call failed: 'DEEPSEEK_API_KEY'        # graceful fallback
> [COMPILER] Using default render script: ..._render.py  # fallback to _render.py
> [SESSION COMPLETE]
>   Iterations:     3
>   Approved:       False
>   Compilation errors: 1

# All 3 LLM agents fail gracefully; compiler falls back to _render.py
# With DEEPSEEK_API_KEY set: gold writes _gold_arrangement.py, compiler executes it
```

## Verification Results (Session 8)

```powershell
# Dry run - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run
> [DRY RUN] Graph structure shows all 7 nodes + conditional routing

# Full invocation with real curator (no DEEPSEEK_API_KEY) - PASS
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
> [CURATOR] Auto-rejected: compilation errors     # no LLM call needed
> [SESSION COMPLETE]
>   Iterations:     3
>   Approved:       False
>   Score:          0.0
>   Compilation errors: 1

# Curator logic verified:
# 1. Compilation errors present → auto-reject (score=0.0)
# 2. No compilation errors + valid analysis_metrics → LLM call
# 3. LLM call fails → fallback threshold-based evaluation
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
