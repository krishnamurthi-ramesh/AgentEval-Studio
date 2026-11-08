# Product Strategy, Opportunity Solution Tree (OST) & MVP Scoping

**Document Status:** Approved Strategy  
**Phase:** 3 — Product Strategy  
**Product:** AgentEval Studio  
**Date:** November 2026

---

## 1. Product Vision & Strategic Positioning

### Vision
**To become the standard open-source decision workbench for engineering teams shipping tool-using AI agents.**

### Strategic Positioning (2x2 Matrix)
To position AgentEval Studio in the competitive landscape, we map two primary axes:
- **X-Axis:** Scope of Evaluation (*General LLM / RAG vs. Tool-Calling & Agent Trajectory*)
- **Y-Axis:** Product Workflow Focus (*Passive Observability / Metrics vs. Prescriptive Release Decision-Making*)

```
                                Prescriptive Release Decision
                                              ▲
                                              │
                                              │   ★ AgentEval Studio
                                              │     (Tool-Agent Focus +
                                              │      Release Gate Engine)
                                              │
                      Braintrust              │
                   (CI/CD Assertions)         │
                                              │
    General LLM / RAG ────────────────────────┼──────────────────────── Agent / Tool Trajectory
                                              │
                 LangSmith                    │   Google Gen AI Eval
             (Prompt Playground)              │   (Trajectory Metrics Pre-GA)
                                              │
                 Arize Phoenix                │   OpenAI Agent Evals
             (OTel Span Waterfall)            │   (Trace Grading Guides)
                                              │
                                              ▼
                                 Passive Observability / Metrics
```

---

## 2. Opportunity Solution Tree (OST)

Following Teresa Torres' Opportunity Solution Tree framework, we anchor on a single measurable desired outcome:

### Desired Outcome
> **Enable applied AI teams to evaluate agent variants across multiple dimensions and reach a defensible, auditable release decision in under 5 minutes with zero undetected tool regressions.**

```
                                  [ Desired Outcome ]
                   Fast, defensible release decisions with zero regressions
                                           │
         ┌─────────────────────────────────┼─────────────────────────────────┐
         │                                 │                                 │
         ▼                                 ▼                                 ▼
   [Opportunity 1]                   [Opportunity 2]                   [Opportunity 3]
  Release Paralysis &             High Friction in Tool             Infrastructure & Setup
  Metric Interpretation           Failure Diagnostics               Friction (Cloud lock-in)
         │                                 │                                 │
  ┌──────┴──────┐                   ┌──────┴──────┐                   ┌──────┴──────┐
  │             │                   │             │                   │             │
  ▼             ▼                   ▼             ▼                   ▼             ▼
[Sol 1.1]     [Sol 1.2]           [Sol 2.1]     [Sol 2.2]           [Sol 3.1]     [Sol 3.2]
Policy Gate   Automated           Deterministic Trajectory          Local-First   File-Backed
Engine        Decision Brief      Tool Suite    Matcher             Workbench UI  Dataset Core
(Pass/Fail)   (Markdown/PDF)      (JSON Schema) (Exact, In-Order)   (Streamlit)   (JSONL/Parquet)
```

### Opportunities & Solutions Breakdown

#### Opportunity 1: Teams experience "Release Paralysis" trying to reconcile competing metrics
- **Pain:** When accuracy increases 3% but latency increases 25% and cost increases 15%, teams lack clear rules for deciding whether to ship.
- **Solution 1.1 (Release Gate Engine):** A configurable policy engine with explicit thresholds:
  - Minimum Tool Selection Accuracy (e.g., `>= 92%`)
  - Maximum Permissible Latency Delta (e.g., `< +15%`)
  - Zero-Tolerance Tool Blockers (e.g., `execute_refund` regression = `FAIL`)
- **Solution 1.2 (Automated Release Decision Brief):** One-click exportable Markdown/PDF summary synthesizing the decision (`SHIP`, `HOLD`, `INVESTIGATE`), linking every violated gate to the exact failing row.

#### Opportunity 2: High friction diagnosing tool-agent failure modes
- **Pain:** Existing tools treat tool calls as generic spans or rely on expensive, non-deterministic LLM-as-judge prompts to evaluate outputs.
- **Solution 2.1 (Deterministic Tool Evaluator Suite):** Native Python evaluators for:
  - Tool Selection Precision, Recall, and Accuracy.
  - JSON Schema Argument Conformance.
  - Entity Parameter Matching (ground truth value equality).
- **Solution 2.2 (Trajectory Path Evaluators):** Formal mathematical trajectory metrics (Exact Match, In-Order Match, Any-Order Match, Redundant Loop Detection).

#### Opportunity 3: Heavy infrastructure overhead and vendor lock-in
- **Pain:** LangSmith and Braintrust require SaaS accounts; Phoenix requires OTel daemons and Docker containers.
- **Solution 3.1 (Local-First Streamlit Workbench):** Zero-config interactive web UI that launches in 1 second.
- **Solution 3.2 (File-Backed Data Engine):** Datasets and experiment logs stored in local version-controlled JSONL/Parquet files with zero external database dependencies.

---

## 3. Feature Prioritization (MoSCoW Framework)

| Category | Feature | Rationale | Phase |
|---|---|---|---|
| **Must Have (MVP)** | **Deterministic Tool Evaluator Suite** | Essential core: Tool selection, schema validation, entity match, and trajectory match. | Phase 4-5 |
| **Must Have (MVP)** | **Multi-Variant Experiment Runner** | Run baseline vs candidate variants against a versioned benchmark dataset. | Phase 4-5 |
| **Must Have (MVP)** | **Release Gate Policy Engine** | Configurable pass/fail thresholds for quality, latency, cost, and high-risk tools. | Phase 4-5 |
| **Must Have (MVP)** | **Automated Release Decision Brief** | Generate an executive-ready, evidence-backed sign-off brief (Markdown). | Phase 4-5 |
| **Must Have (MVP)** | **Local Streamlit Workbench UI** | Interactive side-by-side comparison, row inspection, and gate visualization. | Phase 4-5 |
| **Must Have (MVP)** | **Banking / Customer Support Benchmark** | Realistic 25+ row benchmark with 8 real tools and subtle failure modes. | Phase 4-5 |
| **Should Have** | CLI Runner for CI/CD | Headless execution in GitHub Actions (`agenteval run ...`). | Phase 6 |
| **Should Have** | LLM-as-Judge Evaluator with Rubric | Qualitative task completion and tone evaluator. | Phase 6 |
| **Could Have** | DuckDB Query Console | Direct SQL querying over experiment traces. | Post-MVP |
| **Could Have** | PDF / HTML Export for Brief | Formatted export for corporate compliance. | Post-MVP |
| **Won't Have (Initial)** | Full OpenTelemetry APM Collector | Do not compete with Phoenix or Datadog for live streaming production traffic. | Out of scope |
| **Won't Have (Initial)** | Autonomous Rollback / Continuous Deploy | Human-in-the-loop decision-making only. | Out of scope |

---

## 4. MVP Success Criteria & Metrics

### Developer Utility Metrics (Open Source)
- **Time to First Evaluation:** Under 60 seconds from `git clone` to viewing a live experiment comparison and release brief.
- **Zero API Key Requirement for Deterministic Core:** Developers can run the benchmark and evaluators 100% offline without needing OpenAI or Anthropic keys.
- **Test Coverage:** >= 85% test coverage across core evaluator and gate modules.

### Product Management Rigor (Portfolio & Interviews)
- Every product decision is mapped to a verified market gap from our competitive teardowns.
- Complete documentation from Charter -> Discovery -> Strategy -> PRD -> Code -> Benchmark -> Launch.
