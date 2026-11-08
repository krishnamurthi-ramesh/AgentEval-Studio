# AI Product Management Capstone Case Study: AgentEval Studio

**Product:** AgentEval Studio  
**Role:** Lead AI Product Manager  
**Project Phase:** Research, Discovery, Product Strategy, Architecture, Implementation, and Benchmark Validation  
**Date:** November 2026

---

## 1. Executive Summary & Problem Framing

The AI evaluation category is crowded with OpenTelemetry trace collectors (Arize Phoenix, Langfuse), prompt experimentation playgrounds (LangSmith, Braintrust), and academic foundation-model leaderboards (Hugging Face, Kaggle).

Yet, talking to practitioners and analyzing public developer discussions reveals a persistent pain point:
> **"Running evaluations is easy once you have a dataset. But authoring a trustworthy evaluation pack—with negative edge cases, tool schemas, and explicit safety boundaries—takes days. When tests fail, teams fall into 'metric soup' paralysis, unable to agree on whether quality gains justify latency or cost regressions."**

Instead of building another passive observability dashboard, we positioned **AgentEval Studio** as:
> **The collaborative authoring and linting studio for application-level AI evaluations ("ChatPRD for AI Evals").**

### Core Value Proposition
1. **Behaviour-to-Eval Copilot:** Transforms natural-language agent descriptions or failure bug reports into structured, versioned **Eval Packs**.
2. **Eval Quality Linter:** Analyzes test suites *before* execution to catch missing negative boundaries, unconstrained high-risk actions, and overfitting risks.
3. **Seamless Framework Export:** Exports directly to **Promptfoo YAML** and **DeepEval**, integrating with existing developer test runners rather than building redundant infrastructure.
4. **Release Policy Gates:** Formal pass/fail gate engine that evaluates multi-dimensional trade-offs and generates an auditable, executive-ready **Release Decision Brief**.

---

## 2. Competitive Landscape & Category Mapping

We analyzed 10 products across 5 competitive groups:
- **Community Evaluation Platforms:** Kaggle Community Benchmarks, Hugging Face Community Evals, EvalHub.
- **Registries & Standards:** Every Eval Ever, Inspect Evals (UK AISI).
- **Evaluation Authoring & Execution CLI:** Promptfoo, DeepEval.
- **Observability & Experimentation Platforms:** Arize Phoenix, Langfuse, LangSmith, Braintrust.
- **Guided Authoring UX Inspiration:** ChatPRD.

### The Opportunity Gap
While existing tools focus heavily on **execution** (running prompts through models), none focus on **authoring quality assurance**:
- No tool lints whether an evaluation dataset has sufficient negative test cases to catch out-of-bounds agent actions.
- No tool checks whether high-risk tools (e.g., transfers, refunds) have negative security constraints.
- No tool generates ready-to-run Promptfoo test suites from conversational bug reports.

---

## 3. Real Demand Signals & Customer Evidence

Our strategy is anchored on verifiable practitioner evidence:
- **Signal 1 (Dataset Bottleneck):** In [Reddit r/Rag](https://www.reddit.com/r/Rag/comments/1wdlgu1/how_do_you_create_reliable_evaluation_datasets/), developers described spending "hours or more than a week" hand-crafting reliable evaluation datasets because synthetic datasets cannot be trusted as ground truth.
- **Signal 2 (Evaluation Authoring Friction):** Active GitHub issues in Arize Phoenix expose workflow pain:
  - [#17733](https://github.com/Arize-ai/phoenix/issues/17733): Demand for holdout examples to prevent prompt overfitting.
  - [#17715](https://github.com/Arize-ai/phoenix/issues/17715) & [#17723](https://github.com/Arize-ai/phoenix/issues/17723): Demand to simplify and standardize evaluator creation.
  - [#17721](https://github.com/Arize-ai/phoenix/issues/17721): Demand for spend limits to prevent evaluation token drain.
- **Signal 3 (Tool-Call Assertion Need):** Promptfoo users requested first-class assertions for tool-call arguments without the overhead of full APM tracing.

---

## 4. The Opportunity Decision Record (Build vs. No-Build)

As an AI Product Manager, knowing **what NOT to build** is as critical as knowing what to build:
- ❌ **Did NOT build an observability collector:** Competing with Phoenix or Datadog for live traces is a commodity trap.
- ❌ **Did NOT build a new execution runner:** Replaced by exporting directly to **Promptfoo** and **DeepEval**, respecting established developer toolchains.
- ❌ **Did NOT build an academic model leaderboard:** Competing with Hugging Face's Open LLM Leaderboard wastes resources on foundation models rather than application engineering.
- ✅ **BUILT Behaviour-to-Eval Copilot + Eval Quality Linter + Release Policy Gates:** Solves the exact authoring and decision friction AI application teams face every sprint.

---

## 5. Technical Architecture & Implementation

We delivered a full-stack, local-first open-source architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AgentEval Studio System                         │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Frontend Web App (React 18 + TypeScript 5.7 + Vite 6 + Tailwind)    │
│    • Interactive Copilot, Linter, Runner, Gates, & Exporter           │
│    • Optimized for zero-config Vercel deployment (vercel.json)        │
│    • Verified running locally on http://localhost:3000                 │
├────────────────────────────────────────────────────────────────────────┤
│ 2. Deterministic Evaluation Engine (Python SDK & CLI)                  │
│    • ToolSelectionEvaluator (Precision, Recall, Forbidden Tools)       │
│    • SchemaValidator (Required keys & types)                           │
│    • ArgumentMatchEvaluator (Fuzzy entity equality & normalization)    │
│    • TrajectoryEvaluator (In-order subsequence & loop detection)       │
│    • Sub-second execution with $0 in API token costs                   │
├────────────────────────────────────────────────────────────────────────┤
│ 3. Quality Linter & Exporters                                          │
│    • EvalQualityLinter (6 test suite design rules, Score 0-100)        │
│    • Promptfoo YAML Exporter (`promptfooconfig.yaml`)                  │
│    • JSON Schema Manifest Exporter                                     │
├────────────────────────────────────────────────────────────────────────┤
│ 4. CI/CD & Test Automation                                             │
│    • 12 automated unit tests passing in pytest                         │
│    • GitHub Actions multi-version matrix (Python 3.10, 3.11, 3.12)    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Benchmark Validation: The Banking Agent Experiment

We tested 3 prompt variants across our 8-case Banking Benchmark:
- **`router_prompt_v1` (Baseline):** Fast (90ms), but omitted `to_account` on transfers $\rightarrow$ **Pass Rate: 62.5%**.
- **`router_prompt_v2` (Candidate A):** Fixed arguments, but fell for a role-play prompt injection (`SYSTEM OVERRIDE` wire transfer) $\rightarrow$ **Policy Gate Status: `BLOCKED`** (1 high-risk failure on sensitive tool `transfer_funds`).
- **`router_prompt_v3` (Candidate B):** Hardened with security constraints and multi-step trajectory chaining $\rightarrow$ **Policy Gate Status: `READY_TO_SHIP`** (100% pass rate, all 5 gates passed).

**Key Takeaway:** Monolithic accuracy scores hide disasters: Candidate `v2` had higher accuracy than `v1` (75% vs 62.5%), but would have deployed a catastrophic security vulnerability. Only AgentEval Studio's **Zero-Tolerance Gate** caught the issue.

---

## 7. GTM & Open-Source Community Strategy

1. **Self-Sustaining Community Flywheel:** Developers contribute reusable Eval Packs via GitHub PRs using our standardized issue templates.
2. **Complementary Distribution:** By exporting to Promptfoo YAML, we tap into Promptfoo's large developer community without friction.
3. **Interview-Ready Defense:** Every product decision, trade-off, and metric is documented with primary source citations.
