# Deep Product & Technical Teardown: Arize Phoenix

**Product:** Arize Phoenix (and Arize AX)  
**Vendor:** Arize AI  
**License:** Apache 2.0 (Open Source)  
**Primary Focus:** Open-source AI observability, OpenTelemetry tracing, evaluations, datasets, and experiment comparison  
**Research Date:** November 2026  
**Sources:** [Arize Phoenix GitHub Repository](https://github.com/Arize-ai/phoenix), [Arize Phoenix Official Docs](https://docs.arize.com/phoenix), [OpenInference Semantic Conventions](https://github.com/Arize-ai/openinference)

---

## 1. Executive Summary & Market Positioning

Arize Phoenix is a widely adopted open-source AI observability and evaluation platform. Originally developed by Arize AI (a machine learning observability vendor), Phoenix was designed to bring OpenTelemetry-native tracing, evaluation benchmarks, and prompt experimentation to LLM and agentic workflows.

### Core Value Proposition
- **Open-source, self-hostable core:** Developers can run Phoenix locally inside a Jupyter notebook or as a standalone Docker/FastAPI container without sending application traces to a third-party cloud.
- **OpenTelemetry & OpenInference Standard:** Phoenix relies on OpenTelemetry standards and pioneered the **OpenInference** semantic conventions (standardizing span attributes for LLMs, chains, embeddings, retrievers, tools, and agents).
- **All-in-one Observability:** Combines live trace collection, dataset curation, offline evaluator execution, and side-by-side experiment comparisons in a single UI.

### Ideal Customer Profile (ICP)
- **Primary:** AI Engineers and ML Platform Engineers building LLM-powered applications (RAG and agents) who require OpenTelemetry-compliant tracing and want to self-host to comply with data privacy policies.
- **Secondary:** Applied AI Teams migrating from ad-hoc notebook evaluation to a centralized experimentation and tracing dashboard.

---

## 2. Onboarding & Developer Experience

### Getting Started (Time to "Hello World")
Phoenix excels at low-friction developer onboarding:
```bash
pip install arize-phoenix openinference-instrumentation-openai openai
```

Starting the local Phoenix server in Python:
```python
import phoenix as px
session = px.launch_app() # Launches local UI on http://localhost:6006
```

Auto-instrumenting an agent or LLM call via OpenInference:
```python
from openinference.instrumentation.openai import OpenAIInstrumentor
from opentelemetry import trace as trace_api

# Automatically captures all OpenAI completions and tool calls as OTel spans
OpenAIInstrumentor().instrument()
```

### Usability Assessment
- **Frictionless local launch:** Launching within a notebook (`px.launch_app()` renders an inline iframe) is intuitive for data scientists and ML researchers.
- **Setup Complexity:** Getting basic traces running takes under 5 minutes. However, configuring full agent trajectory tracing across custom multi-step tools (beyond standard LangChain or LlamaIndex wrappers) requires manual OpenTelemetry tracer instrumentation, which has a steeper learning curve for product managers and junior developers.

---

## 3. Open-Source Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Application / Agent Code                    │
│      (LangChain, LlamaIndex, CrewAI, Custom Agent SDK)      │
└──────────────────────────────┬──────────────────────────────┘
                               │ OpenInference Instrumentation
                               ▼ (OTel Spans: LLM, Tool, Agent)
┌─────────────────────────────────────────────────────────────┐
│             OpenTelemetry Collector / Phoenix Client        │
│                (gRPC / HTTP: http://localhost:6006/v1/traces)│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Arize Phoenix Server                     │
│  ┌──────────────────────────┐    ┌───────────────────────┐  │
│  │   FastAPI Ingestion API  │    │ GraphQL / REST API    │  │
│  └─────────────┬────────────┘    └───────────┬───────────┘  │
│                │                             │              │
│                ▼                             ▼              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ Storage Layer: DuckDB (in-memory/file) / PostgreSQL   │  │
│  │ Traces, Spans, Datasets, Experiments, Annotations    │  │
│  └───────────────────────────────────────────────────────┘  │
│                              ▲                              │
│                              │                              │
│  ┌───────────────────────────┴───────────────────────────┐  │
│  │        React + TypeScript Single Page App (UI)        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Datasets & Experiment Workflow

### Dataset Management
Phoenix provides a dataset entity composed of:
- `id`, `name`, `description`
- `examples`: List of rows containing `input` (dictionary), `expected_output` (optional ground truth), and `metadata`.
- Datasets can be created:
  1. Manually via UI or Python SDK (`px.Client().upload_dataset(...)`).
  2. Extracted directly from production traces ("golden dataset" creation from filtered traces).

### Experiment Execution (`run_experiment`)
Experiments in Phoenix are executed programmatically via the Python SDK:
```python
from phoenix.experiments import run_experiment
from phoenix.experiments.evaluators import Contains

def agent_task(input_data):
    return my_agent.run(input_data["query"])

experiment = run_experiment(
    dataset=dataset,
    task=agent_task,
    evaluators=[Contains(target="expected_output")]
)
```

---

## 5. Shortcomings & The Authoring Gap in Phoenix

Recent GitHub issues from Phoenix practitioners expose the real friction points in evaluation authoring:
- **Issue #17733:** Users request formal holdout example splits to prevent prompt overfitting.
- **Issue #17715 & #17723:** Users struggle with inconsistent evaluator authoring and demand simplified creation workflows.
- **Issue #17721:** Users demand spend limits on evaluator runs to prevent token drain.
- **RAG Bias:** Built-in evaluators are heavily weighted toward QA and RAG; authoring multi-step tool-calling agent evaluators requires significant custom code.
- **No Evaluation Linter:** Phoenix will run whatever dataset you feed it, even if the dataset has ambiguous expectations, zero negative test cases, or missing parameter definitions.
