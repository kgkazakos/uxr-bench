# uxr-bench

**CPR Orbital · S3 Tool 3 · Tool 15**

A benchmark dataset and evaluation harness for measuring LLM performance on qualitative UX research tasks.

[![CI](https://github.com/kgkazakos/uxr-bench/actions/workflows/ci.yml/badge.svg)](https://github.com/kgkazakos/uxr-bench/actions)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)](https://pypi.org/project/uxr-bench/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## What it is

`uxr-bench` gives you a **curated dataset of 25 annotated UX research tasks** — each with a real-world input, a standardised prompt, and human-verified ground truth labels. You can run any LLM (or baseline heuristic) against the full suite and get back precision, recall, F1, and pass rates — by task, category, and difficulty.

The benchmark covers five research skills that matter most when evaluating LLMs for product research work:

| Category | Code | What it tests |
|----------|------|---------------|
| Thematic Coding | `TC` | Identifying themes from interview excerpts |
| Bias Detection | `BD` | Spotting leading questions, social desirability, anchoring |
| Insight Extraction | `IE` | Surfacing actionable insights from messy data |
| Guide Evaluation | `GE` | Scoring discussion guide quality (0–100) |
| Say–Do Gap | `SD` | Detecting inconsistencies between stated and revealed behaviour |

Each category has 5 tasks spanning easy → medium → hard.

---

## Installation

```bash
pip install uxr-bench
```

With LLM support (OpenAI / Anthropic / Gemini via LiteLLM):

```bash
pip install "uxr-bench[llm]"
```

---

## Quick start

### Baseline evaluation (no API key needed)

```bash
# Run all 25 tasks using the keyword-extraction baseline
uxr-bench run --all

# Filter by category or difficulty
uxr-bench run --category bias_detection
uxr-bench run --category thematic_coding --difficulty easy

# Get JSON output for CI integration
uxr-bench run --all --json
```

### LLM evaluation

```bash
export OPENAI_API_KEY=sk-...
uxr-bench run --all --llm-backend openai

export ANTHROPIC_API_KEY=sk-ant-...
uxr-bench run --category say_do_gap --llm-backend anthropic

export GEMINI_API_KEY=...
uxr-bench run --task TC-003 --llm-backend gemini
```

### Explore the dataset

```bash
# List tasks
uxr-bench list
uxr-bench list --category insight_extraction
uxr-bench list --difficulty hard
uxr-bench list --tag fintech

# Inspect a task
uxr-bench show TC-001

# Dataset statistics
uxr-bench stats

# Export for fine-tuning or downstream use
uxr-bench export --format jsonl -o benchmark.jsonl
uxr-bench export --category bias_detection --format json
```

---

## Dataset design

### A note on the built-in tasks

The 25 built-in tasks are **synthetic**. The inputs were constructed to reflect real qualitative research patterns — privacy paradox, notification fatigue, workaround behaviour, say–do inconsistency — but they are not drawn from actual research sessions. Ground truth labels were reasoned from first principles by the author, not validated through inter-rater reliability with human coders.

This means `uxr-bench` is best positioned as a **developer evaluation tool**: something you run to catch regressions, compare models head-to-head, and understand where a given LLM tends to fall apart before putting it in front of real research data. It is not a research artefact making claims about LLM capability in the wild.

A version grounded in real annotated corpora with measured inter-rater reliability would be a legitimate research contribution. If you are working on that, the harness below is designed to support it directly.

### Bring your own data

If you have a real annotated research corpus — actual transcripts, real labels, measured ground truth — you can wire it straight into the evaluation harness through a single `response_fn`. The scoring, reporting, and CLI infrastructure work on any data you provide:

```python
from uxr_bench.models import BenchmarkTask, Difficulty, GroundTruth, TaskCategory
from uxr_bench.evaluator import BenchmarkEvaluator

# Define tasks from your own corpus
my_tasks = [
    BenchmarkTask(
        task_id="MY-001",
        category=TaskCategory.THEMATIC_CODING,
        difficulty=Difficulty.MEDIUM,
        description="Real transcript from fintech study, wave 2",
        input_text="P: I never actually check my balance...",
        prompt_template="Identify themes:\n{input_text}\n\nThemes:",
        ground_truth=GroundTruth(
            labels=["financial_avoidance", "anxiety_driven_behaviour"],
            rationale="Coded by two researchers, Cohen's kappa=0.81",
        ),
    ),
]

evaluator = BenchmarkEvaluator(backend="anthropic")
results = evaluator.run_tasks(my_tasks, response_fn=lambda t: your_llm(t.render_prompt()))
report = evaluator.compile_report(results)
print(f"Pass rate: {report.pass_rate:.1%}")
```

### Task structure

Every task includes:
- **`input_text`** — a UX research excerpt (interview quote, discussion guide, or transcript segment)
- **`prompt_template`** — a standardised prompt with `{input_text}` placeholder
- **`ground_truth.labels`** — label set with annotation rationale
- **`ground_truth.score`** — numeric score (Guide Evaluation tasks only)
- **`ground_truth.rationale`** — explanation of the annotation decision

### Scoring

| Category | Scoring method | Pass threshold |
|----------|---------------|----------------|
| Thematic Coding | Exact set F1 | F1 ≥ 0.5 |
| Bias Detection | Exact set F1 | F1 ≥ 0.5 |
| Insight Extraction | Partial token-overlap F1 | F1 ≥ 0.5 |
| Guide Evaluation | Numeric proximity | Within 20 points of GT |
| Say–Do Gap | Exact set F1 | F1 ≥ 0.5 |

Insight Extraction uses a more lenient partial-match scorer (token overlap ≥ 0.4) because insights are expressed in natural language and exact label agreement is an unreasonably high bar.

### Baseline

The built-in baseline extracts the top-6 most frequent non-stopword words (≥5 characters) from the input text. It is intentionally a low floor — any capable LLM should beat it. The baseline requires no API key and runs offline.

---

## Python API

```python
from uxr_bench.dataset import list_tasks, get_task
from uxr_bench.evaluator import BenchmarkEvaluator
from uxr_bench.llm import baseline_response

# Explore the dataset
tasks = list_tasks(category="bias_detection", difficulty="easy")
task = get_task("TC-001")
prompt = task.render_prompt()

# Run evaluation
evaluator = BenchmarkEvaluator(backend="baseline")
results = evaluator.run_tasks(
    tasks,
    response_fn=baseline_response,
    on_result=lambda r: print(f"{r.task_id}: F1={r.score.f1:.2f}"),
)
report = evaluator.compile_report(results)
print(f"Pass rate: {report.pass_rate:.1%}")
print(f"Overall F1: {report.overall_f1:.3f}")

# BYO response function
def my_llm(task):
    # call your model here
    return "privacy_concern, trust_deficit, workaround_behaviour"

results = evaluator.run_tasks(tasks, response_fn=my_llm)
```

---

## Task catalogue

### Thematic Coding (TC)

| ID | Difficulty | Topic |
|----|-----------|-------|
| TC-001 | Easy | Onboarding friction |
| TC-002 | Medium | Data sharing attitudes |
| TC-003 | Medium | Multi-speaker collaboration |
| TC-004 | Hard | Financial app psychology |
| TC-005 | Hard | AI tool trust and adoption |

### Bias Detection (BD)

| ID | Difficulty | Topic |
|----|-----------|-------|
| BD-001 | Easy | Single leading question |
| BD-002 | Medium | Double-barreled question |
| BD-003 | Medium | Social desirability + loaded framing |
| BD-004 | Hard | Confirmation bias sequence |
| BD-005 | Hard | Subtle framing effects |

### Insight Extraction (IE)

| ID | Difficulty | Topic |
|----|-----------|-------|
| IE-001 | Easy | Converging themes |
| IE-002 | Medium | Privacy paradox |
| IE-003 | Medium | Design opportunity from workarounds |
| IE-004 | Hard | Hedged expert/novice insight |
| IE-005 | Hard | Longitudinal wave comparison |

### Guide Evaluation (GE)

| ID | Difficulty | GT Score |
|----|-----------|---------|
| GE-001 | Easy | 82 (high quality) |
| GE-002 | Easy | 28 (poor quality) |
| GE-003 | Medium | 61 (mixed) |
| GE-004 | Medium | 66 (time-unrealistic) |
| GE-005 | Hard | 71 (survivor bias) |

### Say–Do Gap (SD)

| ID | Difficulty | Topic |
|----|-----------|-------|
| SD-001 | Easy | Privacy paradox |
| SD-002 | Medium | Frequency misreport |
| SD-003 | Medium | Simplicity vs power-user |
| SD-004 | Hard | Competitor denial |
| SD-005 | Hard | Self-serving rationalisation |

---

## Development

```bash
git clone https://github.com/kgkazakos/uxr-bench
cd uxr-bench
pip install -e ".[dev]"
pytest
ruff check uxr_bench/ tests/
```

---

## Part of CPR Orbital

`uxr-bench` is Tool 15 in the [CPR Orbital](https://github.com/kgkazakos) series — 40 open-source Python tools for AI-native product research infrastructure, shipping every Friday.

**Computational Product Research (CPR)** is a discipline that combines qualitative research rigour with quantitative methods and LLM tooling to build a more systematic, reproducible approach to product understanding.

---

## License

MIT © Kostas Gkazakos
