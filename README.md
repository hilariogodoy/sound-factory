# Audio Warehouse Engine

Autonomous AI techno music production system using a Medallion architecture
(Bronze/Silver/Gold) over a LangGraph multi-agent pipeline.

## Architecture

```
orchestrator
  -> bronze_designer (LLM: generates Pyo instrument patches)
    -> silver_sequencer (LLM: generates 16-step patterns)
      -> gold_mixer (LLM: generates complete arrangement script)
        -> audio_compiler (subprocess: executes Pyo script -> WAV)
          -> audio_analyzer (librosa: extracts audio metrics)
            -> taste_curator (LLM: evaluates metrics vs taste profile)
              -> conditional:
                  approved -> END
                  rejected + iters<3 -> bronze_designer (retry)
                  rejected + iters>=3 -> error_termination -> END
```

- **Circuit breaker**: Caps retries at 3 iterations
- **Provider abstraction**: All LLMs route through `src/llm_factory.py`
- **Subprocess isolation**: Audio compilation runs in isolated subprocess

## Quick Start

### Prerequisites

- Python 3.10 (required for Pyo compatibility)
- API key for an LLM provider (default: DeepSeek via `DEEPSEEK_API_KEY`)

### Setup

```bash
pip install -r requirements.txt
```

### Run

```bash
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic
```

### Dry Run

```bash
python src/main.py --bpm 133 --key "A minor" --energy 0.8 --mood hypnotic --dry-run
```

### Options

| Flag | Default | Description |
|---|---|---|
| `--bpm` | 133 | Target BPM |
| `--key` | A minor | Musical key |
| `--energy` | 0.8 | Energy level 0.0-1.0 |
| `--mood` | hypnotic | Mood descriptor |
| `--track-id` | track_001 | Track identifier |
| `--human-feedback` | (empty) | Feedback for retry iteration |
| `--output-dir` | warehouse | Output directory root |
| `--verbose` | false | Detailed per-node logging |
| `--dry-run` | false | Print graph structure only |

## LLM Configuration

Edit `config/llm_config.yaml` or set `LLM_PROVIDER` env var. Supported providers:

- `openai` — uses `OPENAI_API_KEY`
- `anthropic` — uses `ANTHROPIC_API_KEY`
- `openai_compatible` (default) — uses `DEEPSEEK_API_KEY`

## Project Structure

```
config/
  llm_config.yaml               Provider selection
  reference_taste_profile.json  4 Librosa thresholds for curator
  system_prompts/               Agent prompts (bronze, silver, gold, curator)
src/
  main.py                       CLI entry point
  graph.py                      LangGraph state machine (8 nodes)
  llm_factory.py                Vendor-agnostic LLM provider
  agents/
    orchestrator.py             Dir setup, branch naming
    bronze_agent.py             Pyo instrument generation
    silver_agent.py             16-step pattern generation
    gold_agent.py               Full arrangement script
    curator_agent.py            Taste evaluation + fallback scoring
  audio_engine/
    compiler.py                 Subprocess executor
    _render.py                  Fallback Pyo render script
    analyzer.py                 Librosa feature extraction
warehouse/
  bronze_patches/               Instrument definitions
  silver_loops/                 Pattern data
  gold_outputs/                 Final WAV + manifests
```
