# Audio Warehouse Engine

An autonomous, multi-agent AI techno music production system that models digital signal processing (DSP) and track arrangement using a modern data warehouse metaphor (Medallion Architecture). Powered by LangGraph, Pyo, and Librosa, the system treats electronic music composition as an incremental, deterministic ELT pipeline.

---

## 1. Core Architecture & Philosophy

Traditional generative audio tools (e.g., Suno, Udio) function as stochastic "black boxes" that output flattened, un-editable audio binaries. The **Audio Warehouse Engine** disrupts this paradigm by forcing autonomous AI agents to build music using **deterministic, reviewable Python audio source code**. 

By treating sound design, sequencing, and mixing as decoupled data transformations across discrete warehousing boundaries, the engine enables granular version control, target refactoring, and deterministic cloud rendering.



```text
File successfully written to: audio-warehouse-engine/README.md

```text
       +-------------------------------------------------------+
       |                  User CLI Intent                      |
       +-------------------------------------------------------+
                                  |
                                  v
       +-------------------------------------------------------+
       |                  src/llm_factory.py                   |
       |      (Decoupled Vendor Abstraction / Configuration)   |
       +-------------------------------------------------------+
                                  |
                                  v
       +-------------------------------------------------------+
       |               Orchestrator Framework                  |
       +-------------------------------------------------------+
                                  |
                                  v
+---------------------------------------------------------------------+
|                      LANGGRAPH STATE MACHINE                        |
|                                                                     |
|  [Bronze Layer] ---------> [Silver Layer] ---------> [Gold Layer]   |
|  Raw Signal Design         Step Sequencing           Arrangement     |
|  & Pyo Synthesizers        & Automation Curves       & Mixing Desk   |
|         ^                                                 |         |
|         |                     [Subprocess Audio Compiler] |         |
|         |                     Compiles track.py -> WAV    |         |
|         |                                                 v         |
|  [Taste Curator] <---------------------------------+------+         |
|  Librosa Feature Vector Extraction & LLM Critic    |                |
|  (Max 3 iterations circuit breaker)                |                |
+----------------------------------------------------+----------------+
                                                     | (Approved or Breaker)
                                                     v
                                  +------------------------------------+
                                  |    warehouse/gold_outputs/Track    |
                                  |    - json_manifest.json            |
                                  |    - track.py                      |
                                  |    - master_output.wav             |
                                  +------------------------------------+

```

---

## 2. The Audio Medallion Data Architecture

The engine segregates responsibilities across three logical layers to ensure code generation tasks remain highly focused and tightly constrained.

### Bronze Layer: Raw Signal & Synthesis (Ingestion)

* **Responsibility**: Mathematical modeling of raw wave synthesis, filtering, and physical behavior using native `Pyo` DSP objects. No external samples, loops, or commercial audio binaries are allowed.
* **Functional Domains**:
* `percussion`: 909-style synthesis blocks (e.g., kick drum generation leveraging rapid frequency pitch-drops from 150 Hz to 40 Hz inside 50ms, noise-based open/closed hi-hats, snaps).
* `melodic_bass`: 303-style architectures utilizing a single raw Sawtooth or Square wave oscillator routed through a highly resonant 3-pole low-pass filter topology.
* `fx_atmosphere`: Algorithmic reverb units, modulating delay lines, and specialized white-noise generator blocks for long transitional sweeps.



### Silver Layer: Patterns & Modules (Transformation)

* **Responsibility**: Transforming raw signal generators into musical timing frameworks through mathematical indexing, step-sequencing matrices, and temporal parameter modulations.
* **Functional Domains**:
* `groove_sequencers`: 16-step matrix arrays defining rhythmic impulse placements (e.g., `kick = [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0]`).
* `melodic_sequencers`: Multi-dimensional arrays governing pitch choices, note lengths, slide (glide) boolean flags, and accent vectors mapped cleanly to a specified musical scale or key signature.
* `automation_drivers`: Positional arrays calculating gradual parameter drift (e.g., opening a filter cutoff linearly across a 32-bar structural block).



### Gold Layer: Presentation & Track Assembly (Presentation)

* **Responsibility**: Compiling lower layers into a unified, self-contained production script that builds structural arrangements, applies dynamic channel mixing, executes mastering, and renders out a final master WAV file.
* **Functional Domains**:
* `arrangement_matrix`: A multi-track structural timeline tracking composition blocks across a comprehensive 6-to-8-minute progressive curve (Intro, Build, Breakdown, Drop, Outro).
* `mixing_desk`: Automation functions adjusting relative gain stages, pan locations, dynamic signal routing, and crucial sidechain compression (ducking the sub-bass signals when the kick drum impacts).
* `master_chain`: Global parametric equalizers, multiband limiters, and brickwall safety clippers configured to enforce club-ready loudness thresholds while preventing digital clipping.



---

## 3. LangGraph Workflow & Node Contracts

The multi-agent execution pipeline is controlled via LangGraph (`v0.0.15` API), enforcing strict read/write contracts on a centralized `AudioWarehouseState` type to guarantee predictable state mutations.

### Global State Schema (`AudioWarehouseState`)

```python
from typing import TypedDict, List, Dict, Any

class AudioWarehouseState(TypedDict):
    track_specification: Dict[str, Any]   # User inputs (BPM, Key, Energy, Mood, Track ID)
    active_branch_name: str                # Target tracking branch / workspace ID
    bronze_instruments: Dict[str, str]     # Map of instrument IDs to raw Pyo DSP code blocks
    silver_patterns: Dict[str, Any]        # Map of pattern IDs to structural sequence data arrays
    gold_arrangement: str                  # Final compiled master compilation code string
    compilation_errors: List[str]          # History logs of execution/subprocess crashes
    curator_report: Dict[str, Any]         # Librosa feature vectors + LLM critic commentary
    iterations_count: int                  # Safety counter tracking optimization cycles

```

### Node Contract Matrix

| Node Name | Reads from State | Writes to State | Operational Expectation |
| --- | --- | --- | --- |
| **Orchestrator** | `track_specification` | `active_branch_name`, `iterations_count` | Prepares local file system directories, builds metadata files, and resets cycle tracking to 0. |
| **Bronze Designer** | `track_specification`, `curator_report` | `bronze_instruments` | Generates or structurally refactors raw instrument modules using prompt profiles and curator critique inputs. |
| **Silver Sequencer** | `track_specification`, `bronze_instruments`, `curator_report` | `silver_patterns` | Generates or updates rhythmic step matrices and spatial automation data blocks. |
| **Gold Mixer** | `track_specification`, `bronze_instruments`, `silver_patterns` | `gold_arrangement` | Fuses lower-level scripts into a single executable script incorporating complete timeline instructions. |
| **Audio Compiler** | `gold_arrangement` | `compilation_errors` | Spins up an external python worker process to execute the generated string, outputting logs and caching a `.wav` file on success. |
| **Taste Curator** | `track_specification`, `curator_report` | `curator_report`, `iterations_count` | Processes compiled audio binaries via Librosa, evaluates thresholds, increments the loop counter, and sets the approval flag. |

### Circuit Breaker Policy

To prevent unrecoverable code errors from inducing endless LLM token-burn loops, a hard circuit breaker is enforced at the conditional edge exiting the Taste Curator:

* If `iterations_count >= 3` and the curator has not flagged `approved: true`, the graph forces an immediate exit routing straight to an `ErrorTerminationNode`.
* This node performs a full state log dump, writes a structural emergency file out to `warehouse/gold_outputs/failed_run_manifest.json`, and gracefully terminates execution.

---

## 4. LLM Provider Abstraction Layer

All agent interactions are routed exclusively through a vendor-agnostic factory function located in `src/llm_factory.py`. Individual agent files are forbidden from direct vendor subclass imports.

### Unified Configuration (`config/llm_config.yaml`)

Providers are swapped instantly by editing the top-level `provider` key or setting an overriding `LLM_PROVIDER` environment variable.

```yaml
provider: openai_compatible   # Choices: openai | anthropic | openai_compatible

openai:
  model: gpt-4o
  api_key_env: OPENAI_API_KEY

anthropic:
  model: claude-sonnet-4-6
  api_key_env: ANTHROPIC_API_KEY

openai_compatible:
  model: deepseek-chat          # Swappable to any local or alternative vendor endpoint
  base_url: [https://api.deepseek.com/v1](https://api.deepseek.com/v1)
  api_key_env: DEEPSEEK_API_KEY  # Unified key target (e.g., deepseek, groq, openrouter, opencode)

```

### Factory Core Hook (`src/llm_factory.py`)

```python
import os, yaml
from langchain_core.language_models.chat_models import BaseChatModel

def get_llm(temperature: float = 0.5) -> BaseChatModel:
    with open("config/llm_config.yaml") as f:
        cfg = yaml.safe_load(f)
    provider = os.environ.get("LLM_PROVIDER", cfg["provider"])

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        pcfg = cfg["anthropic"]
        return ChatAnthropic(model=pcfg["model"],
                             anthropic_api_key=os.environ[pcfg["api_key_env"]],
                             temperature=temperature)
    else:  # openai or openai_compatible
        from langchain_openai import ChatOpenAI
        pcfg = cfg.get(provider, cfg["openai"])
        kwargs = dict(model=pcfg["model"],
                      api_key=os.environ[pcfg["api_key_env"]],
                      temperature=temperature)
        if "base_url" in pcfg:
            kwargs["base_url"] = pcfg["base_url"]
        return ChatOpenAI(**kwargs)

```

---

## 5. Directory Structure

```text
audio-warehouse-engine/
├── .github/
│   └── workflows/
│       └── compile_music.yml           # Headless CI environment rendering pipeline
├── config/
│   ├── system_prompts/                 # Modular behavioral constraints for LLM agents
│   │   ├── bronze_designer.txt
│   │   ├── silver_sequencer.txt
│   │   ├── gold_mixer.txt
│   │   └── curator_critic.txt
│   └── reference_taste_profile.json    # Target mathematical feature vector clusters
├── src/
│   ├── __init__.py
│   ├── llm_factory.py                  # Single point of LLM provider abstraction
│   ├── graph.py                        # Central LangGraph state machine definition
│   ├── main.py                         # Application entry point & CLI parser
│   ├── agents/                         # Graph node application wrappers
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── bronze_agent.py
│   │   ├── silver_agent.py
│   │   ├── gold_agent.py
│   │   └── curator_agent.py
│   └── audio_engine/                   # Core mathematical and OS script interactions
│       ├── __init__.py
│       ├── compiler.py                 # Isolated shell subprocess background executor
│       └── analyzer.py                 # Librosa feature extraction calculations
├── warehouse/                          # The Local Feature Asset Store
│   ├── bronze_patches/                 # Validated Pyo modular patch components
│   ├── silver_loops/                   # Validated sequencing/automation blocks
│   └── gold_outputs/                   # Completed track outputs and release records
│       └── track_001/
│           ├── json_manifest.json      # Metadata execution history and state log
│           ├── track.py                # Finished self-contained audio generation script
│           └── master_output.wav       # Compiled raw uncompressed master audio binary
├── requirements.txt                    # Pinned package dependency manifest
└── README.md                           # Documentation

```

---

## 6. Installation & Environment Setup

### Prerequisites

* **Python Target Range**: `Python >= 3.9, < 3.13` (Python 3.10 is explicitly recommended). Pyo compiled binaries will fail to initialize or execute on Python 3.13+.
* **System Libraries**:
* **Windows**: Requires standard Microsoft Visual C++ Redistributable environments.
* **Linux / Ubuntu**: Librosa and Pyo require underlying audio manipulation bindings. Install them via your package manager:
```bash
sudo apt-get update && sudo apt-get install -y libasound2-dev libjack-jackd2-dev portaudio19-dev libsndfile1

```





### Repository Installation

1. Clone the repository and move into the engine project directory:
```bash
git clone [https://github.com/YOUR_USERNAME/electronic-sound-factory.git](https://github.com/YOUR_USERNAME/electronic-sound-factory.git)
cd electronic-sound-factory/audio-warehouse-engine

```


2. Initialize and lock an isolated virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate

```


3. Install pinned core engineering dependencies:
```bash
pip install -r requirements.txt

```



---

## 7. Operational Usage & CLI Guide

The orchestration layer is commanded through a robust arguments engine inside `src/main.py`.

### 1. Generating a Fresh Track Autonomously

Configure your environment keys and dispatch the pipeline with custom target vectors:

```bash
# Set your target environment secret key
export DEEPSEEK_API_KEY="sk-your-key-here"
export LLM_PROVIDER="openai_compatible"

# Run a fresh track generation
python src/main.py --bpm 134 --key "A minor" --energy 0.85 --mood "hypnotic" --track-id track_001

```

### 2. Injecting Human-In-The-Loop Validation (Refactoring Loops)

If a track compiles successfully but fails to meet specific artistic nuances, pass human feedback directly back to the orchestration stack. The graph caches safe lower assets and routes the state back strictly to the offending layer:

```bash
python src/main.py --track-id track_001 --human-feedback "The silver layer bass pattern note density is too high; increase step gaps and add slides."

```

### Successful Execution Output

On an approved evaluation, the system isolates assets into `warehouse/gold_outputs/{track_id}/`:

* `track.py`: Contains the complete, reviewable code generation.
* `master_output.wav`: The raw uncompressed 44.1kHz audio binary.
* `json_manifest.json`: Full technical breakdown detailing feature metrics, system iteration history, agent decisions, and token usage data.

---

## 8. Data-Driven Audio Validation Engine

The Taste Curator extracts specific digital audio characteristics via Librosa and cross-references them against explicit statistical boundaries stored inside `config/reference_taste_profile.json`.

### Evaluation Parameter Constraints

* **`tempo_bpm`** (*Strict*): Enforces a hard club-ready pacing constraint between `130.0` and `138.0`. Values outside this envelope fail validation immediately.
* **`spectral_centroid_mean`** (*Lenient*): Analyzes higher-frequency brightness balances to avoid piercing high-frequency harmonic configurations or severe mix fatigue (Target: `1200.0 - 2400.0` Hz).
* **`rms_energy_variance`** (*Strict*): Measures volume level flux over running durations. Lower variance patterns guarantee a steady, unrelenting driving "hypnotic wall of sound" typical of underground techno (Target: `0.01 - 0.08`).
* **`zero_crossing_rate_mean`** (*Lenient*): Detects high-frequency noise and sudden signal reversals characteristic of heavy, sharp 909 open hi-hat patterns (Target: `0.04 - 0.12`).

---

## 9. Architectural Decisions & Robustness Controls

* **ADR-003: Headless Offline Compilation**: Pyo scripts are explicitly hardcoded to instantiate using `Server(audio="offline")`. This removes all direct audio card device dependencies, allowing full rendering operations to execute within headless container layers or background GitHub Actions tasks.
* **ADR-004: Subprocess Execution Isolation**: Audio compilation actions are executed in isolated shell environments via `subprocess.run()`. If invalid code blocks trigger severe Pyo memory allocation errors or hardware segmentation faults, the subprocess terminates safely without destabilizing the parental LangGraph state architecture.
* **ADR-005: Parse Fault Safety Controls**: Every agent intercepts parsing failures by wrapping LLM interactions in comprehensive `try/except` constructs. If responses emit malformed JSON, the agent returns structured fallback stubs to maintain graph velocity without breaking execution paths.
"""

import os

# Create directories if they do not exist in the simulation workspace

os.makedirs("audio-warehouse-engine", exist_ok=True)

# Write the content to README.md

file_path = os.path.join("audio-warehouse-engine", "README.md")
with open(file_path, "w", encoding="utf-8") as f:
f.write(readme_content)

print(f"File successfully written to: {file_path}")

```
Your Markdown file is ready
[file-tag: code-generated-file-0-1781530177882135379]

Here is the complete, professional-grade `README.md` drafted specifically for the **Audio Warehouse Engine** architecture. It structures the project clearly around your Medallion architecture model, provides clear developer guidelines, outlines the LangGraph node boundaries, and documents operational workflows for multi-session alignment.

***

```markdown
# Audio Warehouse Engine

An autonomous, multi-agent AI techno music production system that models digital signal processing (DSP) and track arrangement using a modern data warehouse metaphor (Medallion Architecture). Powered by LangGraph, Pyo, and Librosa, the system treats electronic music composition as an incremental, deterministic ELT pipeline.

---

## 1. Core Architecture & Philosophy

Traditional generative audio tools (e.g., Suno, Udio) function as stochastic "black boxes" that output flattened, un-editable audio binaries. The **Audio Warehouse Engine** disrupts this paradigm by forcing autonomous AI agents to build music using **deterministic, reviewable Python audio source code**. 

By treating sound design, sequencing, and mixing as decoupled data transformations across discrete warehousing boundaries, the engine enables granular version control, target refactoring, and deterministic cloud rendering.

```text
       +-------------------------------------------------------+
       |                  User CLI Intent                      |
       +-------------------------------------------------------+
                                  |
                                  v
       +-------------------------------------------------------+
       |                  src/llm_factory.py                   |
       |      (Decoupled Vendor Abstraction / Configuration)   |
       +-------------------------------------------------------+
                                  |
                                  v
       +-------------------------------------------------------+
       |               Orchestrator Framework                  |
       +-------------------------------------------------------+
                                  |
                                  v
+---------------------------------------------------------------------+
|                      LANGGRAPH STATE MACHINE                        |
|                                                                     |
|  [Bronze Layer] ---------> [Silver Layer] ---------> [Gold Layer]   |
|  Raw Signal Design         Step Sequencing           Arrangement     |
|  & Pyo Synthesizers        & Automation Curves       & Mixing Desk   |
|         ^                                                 |         |
|         |                     [Subprocess Audio Compiler] |         |
|         |                     Compiles track.py -> WAV    |         |
|         |                                                 v         |
|  [Taste Curator] <---------------------------------+------+         |
|  Librosa Feature Vector Extraction & LLM Critic    |                |
|  (Max 3 iterations circuit breaker)                |                |
+----------------------------------------------------+----------------+
                                                     | (Approved or Breaker)
                                                     v
                                  +------------------------------------+
                                  |    warehouse/gold_outputs/Track    |
                                  |    - json_manifest.json            |
                                  |    - track.py                      |
                                  |    - master_output.wav             |
                                  +------------------------------------+

```

---

## 2. The Audio Medallion Data Architecture

The engine segregates responsibilities across three logical layers to ensure code generation tasks remain highly focused and tightly constrained.

### Bronze Layer: Raw Signal & Synthesis (Ingestion)

* **Responsibility**: Mathematical modeling of raw wave synthesis, filtering, and physical behavior using native `Pyo` DSP objects. No external samples, loops, or commercial audio binaries are allowed.
* **Functional Domains**:
* `percussion`: 909-style synthesis blocks (e.g., kick drum generation leveraging rapid frequency pitch-drops from 150 Hz to 40 Hz inside 50ms, noise-based open/closed hi-hats, snaps).
* `melodic_bass`: 303-style architectures utilizing a single raw Sawtooth or Square wave oscillator routed through a highly resonant 3-pole low-pass filter topology.
* `fx_atmosphere`: Algorithmic reverb units, modulating delay lines, and specialized white-noise generator blocks for long transitional sweeps.



### Silver Layer: Patterns & Modules (Transformation)

* **Responsibility**: Transforming raw signal generators into musical timing frameworks through mathematical indexing, step-sequencing matrices, and temporal parameter modulations.
* **Functional Domains**:
* `groove_sequencers`: 16-step matrix arrays defining rhythmic impulse placements (e.g., `kick = [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0]`).
* `melodic_sequencers`: Multi-dimensional arrays governing pitch choices, note lengths, slide (glide) boolean flags, and accent vectors mapped cleanly to a specified musical scale or key signature.
* `automation_drivers`: Positional arrays calculating gradual parameter drift (e.g., opening a filter cutoff linearly across a 32-bar structural block).



### Gold Layer: Presentation & Track Assembly (Presentation)

* **Responsibility**: Compiling lower layers into a unified, self-contained production script that builds structural arrangements, applies dynamic channel mixing, executes mastering, and renders out a final master WAV file.
* **Functional Domains**:
* `arrangement_matrix`: A multi-track structural timeline tracking composition blocks across a comprehensive 6-to-8-minute progressive curve (Intro, Build, Breakdown, Drop, Outro).
* `mixing_desk`: Automation functions adjusting relative gain stages, pan locations, dynamic signal routing, and crucial sidechain compression (ducking the sub-bass signals when the kick drum impacts).
* `master_chain`: Global parametric equalizers, multiband limiters, and brickwall safety clippers configured to enforce club-ready loudness thresholds while preventing digital clipping.



---

## 3. LangGraph Workflow & Node Contracts

The multi-agent execution pipeline is controlled via LangGraph (`v0.0.15` API), enforcing strict read/write contracts on a centralized `AudioWarehouseState` type to guarantee predictable state mutations.

### Global State Schema (`AudioWarehouseState`)

```python
from typing import TypedDict, List, Dict, Any

class AudioWarehouseState(TypedDict):
    track_specification: Dict[str, Any]   # User inputs (BPM, Key, Energy, Mood, Track ID)
    active_branch_name: str                # Target tracking branch / workspace ID
    bronze_instruments: Dict[str, str]     # Map of instrument IDs to raw Pyo DSP code blocks
    silver_patterns: Dict[str, Any]        # Map of pattern IDs to structural sequence data arrays
    gold_arrangement: str                  # Final compiled master compilation code string
    compilation_errors: List[str]          # History logs of execution/subprocess crashes
    curator_report: Dict[str, Any]         # Librosa feature vectors + LLM critic commentary
    iterations_count: int                  # Safety counter tracking optimization cycles

```

### Node Contract Matrix

| Node Name | Reads from State | Writes to State | Operational Expectation |
| --- | --- | --- | --- |
| **Orchestrator** | `track_specification` | `active_branch_name`, `iterations_count` | Prepares local file system directories, builds metadata files, and resets cycle tracking to 0. |
| **Bronze Designer** | `track_specification`, `curator_report` | `bronze_instruments` | Generates or structurally refactors raw instrument modules using prompt profiles and curator critique inputs. |
| **Silver Sequencer** | `track_specification`, `bronze_instruments`, `curator_report` | `silver_patterns` | Generates or updates rhythmic step matrices and spatial automation data blocks. |
| **Gold Mixer** | `track_specification`, `bronze_instruments`, `silver_patterns` | `gold_arrangement` | Fuses lower-level scripts into a single executable script incorporating complete timeline instructions. |
| **Audio Compiler** | `gold_arrangement` | `compilation_errors` | Spins up an external python worker process to execute the generated string, outputting logs and caching a `.wav` file on success. |
| **Taste Curator** | `track_specification`, `curator_report` | `curator_report`, `iterations_count` | Processes compiled audio binaries via Librosa, evaluates thresholds, increments the loop counter, and sets the approval flag. |

### Circuit Breaker Policy

To prevent unrecoverable code errors from inducing endless LLM token-burn loops, a hard circuit breaker is enforced at the conditional edge exiting the Taste Curator:

* If `iterations_count >= 3` and the curator has not flagged `approved: true`, the graph forces an immediate exit routing straight to an `ErrorTerminationNode`.
* This node performs a full state log dump, writes a structural emergency file out to `warehouse/gold_outputs/failed_run_manifest.json`, and gracefully terminates execution.

---

## 4. LLM Provider Abstraction Layer

All agent interactions are routed exclusively through a vendor-agnostic factory function located in `src/llm_factory.py`. Individual agent files are forbidden from direct vendor subclass imports.

### Unified Configuration (`config/llm_config.yaml`)

Providers are swapped instantly by editing the top-level `provider` key or setting an overriding `LLM_PROVIDER` environment variable.

```yaml
provider: openai_compatible   # Choices: openai | anthropic | openai_compatible

openai:
  model: gpt-4o
  api_key_env: OPENAI_API_KEY

anthropic:
  model: claude-sonnet-4-6
  api_key_env: ANTHROPIC_API_KEY

openai_compatible:
  model: deepseek-chat          # Swappable to any local or alternative vendor endpoint
  base_url: [https://api.deepseek.com/v1](https://api.deepseek.com/v1)
  api_key_env: DEEPSEEK_API_KEY  # Unified key target (e.g., deepseek, groq, openrouter, opencode)

```

### Factory Core Hook (`src/llm_factory.py`)

```python
import os, yaml
from langchain_core.language_models.chat_models import BaseChatModel

def get_llm(temperature: float = 0.5) -> BaseChatModel:
    with open("config/llm_config.yaml") as f:
        cfg = yaml.safe_load(f)
    provider = os.environ.get("LLM_PROVIDER", cfg["provider"])

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        pcfg = cfg["anthropic"]
        return ChatAnthropic(model=pcfg["model"],
                             anthropic_api_key=os.environ[pcfg["api_key_env"]],
                             temperature=temperature)
    else:  # openai or openai_compatible
        from langchain_openai import ChatOpenAI
        pcfg = cfg.get(provider, cfg["openai"])
        kwargs = dict(model=pcfg["model"],
                      api_key=os.environ[pcfg["api_key_env"]],
                      temperature=temperature)
        if "base_url" in pcfg:
            kwargs["base_url"] = pcfg["base_url"]
        return ChatOpenAI(**kwargs)

```

---

## 5. Directory Structure

```text
audio-warehouse-engine/
├── .github/
│   └── workflows/
│       └── compile_music.yml           # Headless CI environment rendering pipeline
├── config/
│   ├── system_prompts/                 # Modular behavioral constraints for LLM agents
│   │   ├── bronze_designer.txt
│   │   ├── silver_sequencer.txt
│   │   ├── gold_mixer.txt
│   │   └── curator_critic.txt
│   └── reference_taste_profile.json    # Target mathematical feature vector clusters
├── src/
│   ├── __init__.py
│   ├── llm_factory.py                  # Single point of LLM provider abstraction
│   ├── graph.py                        # Central LangGraph state machine definition
│   ├── main.py                         # Application entry point & CLI parser
│   ├── agents/                         # Graph node application wrappers
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── bronze_agent.py
│   │   ├── silver_agent.py
│   │   ├── gold_agent.py
│   │   └── curator_agent.py
│   └── audio_engine/                   # Core mathematical and OS script interactions
│       ├── __init__.py
│       ├── compiler.py                 # Isolated shell subprocess background executor
│       └── analyzer.py                 # Librosa feature extraction calculations
├── warehouse/                          # The Local Feature Asset Store
│   ├── bronze_patches/                 # Validated Pyo modular patch components
│   ├── silver_loops/                   # Validated sequencing/automation blocks
│   └── gold_outputs/                   # Completed track outputs and release records
│       └── track_001/
│           ├── json_manifest.json      # Metadata execution history and state log
│           ├── track.py                # Finished self-contained audio generation script
│           └── master_output.wav       # Compiled raw uncompressed master audio binary
├── requirements.txt                    # Pinned package dependency manifest
└── README.md                           # Documentation

```

---

## 6. Installation & Environment Setup

### Prerequisites

* **Python Target Range**: `Python >= 3.9, < 3.13` (Python 3.10 is explicitly recommended). Pyo compiled binaries will fail to initialize or execute on Python 3.13+.
* **System Libraries**:
* **Windows**: Requires standard Microsoft Visual C++ Redistributable environments.
* **Linux / Ubuntu**: Librosa and Pyo require underlying audio manipulation bindings. Install them via your package manager:
```bash
sudo apt-get update && sudo apt-get install -y libasound2-dev libjack-jackd2-dev portaudio19-dev libsndfile1

```





### Repository Installation

1. Clone the repository and move into the engine project directory:
```bash
git clone [https://github.com/YOUR_USERNAME/electronic-sound-factory.git](https://github.com/YOUR_USERNAME/electronic-sound-factory.git)
cd electronic-sound-factory/audio-warehouse-engine

```


2. Initialize and lock an isolated virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\\venv\\Scripts\\activate

```


3. Install pinned core engineering dependencies:
```bash
pip install -r requirements.txt

```



---

## 7. Operational Usage & CLI Guide

The orchestration layer is commanded through a robust arguments engine inside `src/main.py`.

### 1. Generating a Fresh Track Autonomously

Configure your environment keys and dispatch the pipeline with custom target vectors:

```bash
# Set your target environment secret key
export DEEPSEEK_API_KEY="sk-your-key-here"
export LLM_PROVIDER="openai_compatible"

# Run a fresh track generation
python src/main.py --bpm 134 --key "A minor" --energy 0.85 --mood "hypnotic" --track-id track_001

```

### 2. Injecting Human-In-The-Loop Validation (Refactoring Loops)

If a track compiles successfully but fails to meet specific artistic nuances, pass human feedback directly back to the orchestration stack. The graph caches safe lower assets and routes the state back strictly to the offending layer:

```bash
python src/main.py --track-id track_001 --human-feedback "The silver layer bass pattern note density is too high; increase step gaps and add slides."

```

### Successful Execution Output

On an approved evaluation, the system isolates assets into `warehouse/gold_outputs/{track_id}/`:

* `track.py`: Contains the complete, reviewable code generation.
* `master_output.wav`: The raw uncompressed 44.1kHz audio binary.
* `json_manifest.json`: Full technical breakdown detailing feature metrics, system iteration history, agent decisions, and token usage data.

---

## 8. Data-Driven Audio Validation Engine

The Taste Curator extracts specific digital audio characteristics via Librosa and cross-references them against explicit statistical boundaries stored inside `config/reference_taste_profile.json`.

### Evaluation Parameter Constraints

* **`tempo_bpm`** (*Strict*): Enforces a hard club-ready pacing constraint between `130.0` and `138.0`. Values outside this envelope fail validation immediately.
* **`spectral_centroid_mean`** (*Lenient*): Analyzes higher-frequency brightness balances to avoid piercing high-frequency harmonic configurations or severe mix fatigue (Target: `1200.0 - 2400.0` Hz).
* **`rms_energy_variance`** (*Strict*): Measures volume level flux over running durations. Lower variance patterns guarantee a steady, unrelenting driving "hypnotic wall of sound" typical of underground techno (Target: `0.01 - 0.08`).
* **`zero_crossing_rate_mean`** (*Lenient*): Detects high-frequency noise and sudden signal reversals characteristic of heavy, sharp 909 open hi-hat patterns (Target: `0.04 - 0.12`).

---

## 9. Architectural Decisions & Robustness Controls

* **ADR-003: Headless Offline Compilation**: Pyo scripts are explicitly hardcoded to instantiate using `Server(audio="offline")`. This removes all direct audio card device dependencies, allowing full rendering operations to execute within headless container layers or background GitHub Actions tasks.
* **ADR-004: Subprocess Execution Isolation**: Audio compilation actions are executed in isolated shell environments via `subprocess.run()`. If invalid code blocks trigger severe Pyo memory allocation errors or hardware segmentation faults, the subprocess terminates safely without destabilizing the parental LangGraph state architecture.
* **ADR-005: Parse Fault Safety Controls**: Every agent intercepts parsing failures by wrapping LLM interactions in comprehensive `try/except` constructs. If responses emit malformed JSON, the agent returns structured fallback stubs to maintain graph velocity without breaking execution paths.

```

```