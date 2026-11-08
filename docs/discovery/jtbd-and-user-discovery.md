# Problem Discovery, Personas & Jobs-To-Be-Done (JTBD)

**Document Status:** Approved Foundation  
**Phase:** 2 — Problem Discovery  
**Target Market:** Applied AI Teams shipping tool-using agents  
**Date:** November 2026

---

## 1. Context & Research Synthesis

Through our competitive teardowns of Arize Phoenix, LangSmith, Braintrust, OpenAI Agent Evals, and Google Gen AI Evaluation, we validated that while the AI observability space is crowded with trace collectors, **agent release decision-making remains unassisted and broken**.

Agent systems differ fundamentally from static LLM completions or standard RAG pipelines:
1. **Multi-Turn Action Space:** An agent executes real-world actions via APIs (transferring money, cancelling orders, querying databases). A failure is not just a stylistic typo—it can trigger an unauthorized database mutation or financial error.
2. **Cascading Failure Modes:** A subtle prompt modification can cause the model to pick an incorrect tool, hallucinate arguments that fail downstream JSON schema validation, or enter redundant infinite execution loops.
3. **Multi-Dimensional Trade-Offs:** Moving from a smaller model to a larger model (or adding detailed system instructions) often improves tool routing precision by 2-4% at the expense of +30% latency and +40% token cost.

---

## 2. Target Personas

```
┌─────────────────────────────────────────┐      ┌─────────────────────────────────────────┐
│     Persona A: The Applied AI Engineer  │      │       Persona B: The AI Product Manager  │
├─────────────────────────────────────────┤      ├─────────────────────────────────────────┤
│ Role: Implements agent workflows, tool  │      │ Role: Defines product requirements,     │
│ schemas, prompts, and orchestration.   │      │ evaluates customer impact, and owns the │
│ Goal: Rapid iteration, fast local evals,│      │ release readiness sign-off.             │
│ debugging root-cause regressions.       │      │ Goal: Balances quality vs latency vs    │
│ Pain: Writing boilerplate eval code for │      │ cost; needs clear evidence to justify   │
│ every tool; slow SaaS eval runs.        │      │ shipping changes to production.         │
└─────────────────────────────────────────┘      └─────────────────────────────────────────┘
```

### Persona A: The Applied AI Engineer ("Dev Dave")
- **Profile:** Software engineer specializing in LLM application development (Python, LangChain/LangGraph/PydanticAI, FastAPI).
- **Core Needs:**
  - Fast, local-first feedback loop. Does not want to wait 10 minutes for cloud telemetry or run heavy Docker containers just to test a prompt change.
  - Deterministic testing: Needs unit-test-like evaluators for tool calling (schema validation, parameter accuracy) that execute locally in milliseconds without burning API credits.
  - Precise root-cause isolation: When a test fails, needs immediate visibility into whether the failure was tool routing, argument synthesis, schema mismatch, or trajectory looping.
- **Quote:** *"I tweaked the tool docstrings and now 3 tests are failing. I don't need a 20-node flamegraph—I just need to know which arguments were hallucinated and which tool was incorrectly chosen."*

### Persona B: The AI Product Manager ("PM Priya")
- **Profile:** Product Manager owning AI agent customer features (customer support bots, automated enterprise workflows, financial assistants).
- **Core Needs:**
  - Defensible decision-making: Needs to answer the sprint question: *"Can we ship prompt v2 to production on Monday?"*
  - Risk governance: High-risk tools (e.g., `execute_refund`, `delete_account`) cannot regress, even if overall accuracy numbers look better on average.
  - Cross-functional communication: Needs a clean, executive-ready **Release Decision Brief** linking metrics to concrete examples to review with Engineering Leads and Risk/Legal teams.
- **Quote:** *"Engineering says prompt v2 scored 92% instead of 89%, but latency jumped by 400ms and one customer received an incorrect refund in testing. We spent 4 hours debating whether to ship."*

---

## 3. Jobs-To-Be-Done (JTBD) Framework

We apply the **Outcome-Driven Innovation (ODI)** framework:  
*When [situation], I want to [motivation/action], so I can [desired outcome].*

### Job 1: Rapid Local Agent Iteration (Engineering Focus)
> **When** I modify an agent's prompt, model, or tool schema,  
> **I want to** evaluate the candidate variant against a versioned benchmark dataset in seconds,  
> **So I can** immediately catch regressions in tool selection, argument accuracy, and trajectory flow before committing code.

### Job 2: Multi-Dimensional Trade-Off Resolution (PM & Eng Focus)
> **When** a candidate agent improves tool selection accuracy but increases latency and token cost,  
> **I want to** evaluate both variants side-by-side against explicit release criteria gates,  
> **So I can** objectively determine whether the quality gains outweigh the operational overhead without guesswork.

### Job 3: Zero-Tolerance Risk Governance (Safety & Compliance Focus)
> **When** evaluating agent updates that touch critical business functions,  
> **I want to** establish hard-blocker gates for sensitive tools (e.g., zero regression permitted on financial transactions),  
> **So I can** prevent catastrophic agent actions from reaching production.

### Job 4: Release Decision Communication (Cross-Functional Alignment)
> **When** completing an evaluation experiment,  
> **I want to** automatically generate an evidence-backed Release Decision Brief with linked trace examples,  
> **So I can** share an auditable sign-off artifact with engineering leads, product stakeholders, and compliance.

---

## 4. Validating the Value Proposition

| Customer Problem | Legacy Approach (Phoenix / LangSmith / Spreadsheets) | AgentEval Studio Approach | Measurable Value |
|---|---|---|---|
| **Release Paralysis** | Sifting through raw dashboards; ad-hoc Slack debates on whether to ship. | **Automated Policy Gate Engine**: Evaluates metrics against pre-configured pass/fail rules. | 80% reduction in time spent deciding whether to deploy an agent update. |
| **Boilerplate Tool Evals** | Writing custom Python scripts from scratch to check JSON schemas and tool names. | **Standardized Deterministic Tool Suite**: Built-in evaluators for precision/recall, schema, entity, trajectory. | Zero setup lines for tool evaluation; instant execution. |
| **Flaky & Costly Judges** | Running expensive LLM-as-judge prompts ($0.03-$0.10/run) for simple tool checks. | **Deterministic-First**: Evaluates tools and arguments using Python rules (free, 100% reproducible). | 90% reduction in evaluation API spend; sub-second execution. |
| **Infrastructure Overhead** | Setting up OTel collectors, SaaS cloud accounts, or persistent Docker databases. | **Local-First & File-Backed**: Runs via CLI or local Streamlit UI; datasets in JSONL/Parquet. | 1-minute time to first evaluation; complete data privacy. |
