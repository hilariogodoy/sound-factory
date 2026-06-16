# AGENTS.md — Audio Warehouse Engine

## Project Overview

Autonomous AI techno music production system using a Medallion architecture (Bronze/Silver/Gold) over LangGraph multi-agent pipeline. Agents write Python/Pyo DSP code, compiled as a subprocess into `.wav`, analyzed by Librosa, critiqued by an LLM curator. Circuit breaker caps retries at 3 iterations.

**Provider abstraction**: All LLM calls route through `src/llm_factory.py` — vendor-agnostic, configured via `config/llm_config.yaml` or `LLM_PROVIDER` env var.

**Sessions are tracked in `PROGRESS.md`** — always read it first.

---

## Every Session Start

1. Read `PROGRESS.md` — understand current phase, completed sessions, and outstanding work.
2. Check the "Context Anchor" section for the exact state of the codebase and what the next session needs to do.
3. Read `AGENTS.md` (this file) for project context.
4. Optionally check `IMPLEMENTATION_PLAN.md`, `precious-meandering-whisper.md`, and `project-kickoff-prompt.md` in the parent directory for deeper architectural reference.
5. Run `git pull` (or `git status`/`git log`) to see the latest state.

---

## Every Session End

1. Run verification checklist from `PROGRESS.md`:
   - `python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run`
   - `pip install -r requirements.txt --dry-run`
   - `python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic`
2. Update `PROGRESS.md`:
   - Mark the completed session row with date and verdict.
   - Verify/update the File Manifest table with new/modified files.
   - Update the Context Anchor section for the next session.
   - Add any new ADRs or Known Issues.
3. Commit all changes with a descriptive message referencing the session number.
4. **Do not push** unless explicitly asked.

---

## Key Constraints

| Constraint | Detail |
|---|---|
| LangGraph | v0.0.15 — no `recursion_limit` kwarg in `compile()`; all nodes must be reachable at compile time |
| Python | 3.13 runtime; numpy/pyo/pyo require workarounds (use Python 3.10 venv for Sessions 3-7 if needed) |
| State | `AudioWarehouseState` TypedDict with 8 fields (see `project-kickoff-prompt.md` §4 or `src/graph.py`) |
| Graph flow | `orchestrator → bronze → silver → gold → compiler → curator → [conditional: approve\|retry\|error_termination]` |
| Circuit breaker | `iterations_count >= 3` → `error_termination` → END |
| Prompts | Stubs live in `config/system_prompts/*.txt` — populate fully when implementing each agent |
