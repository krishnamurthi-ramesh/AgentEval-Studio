# Market Landscape — Agent Evaluation & Experimentation

**Research date:** 8 November 2026  
**Purpose:** Establish what existing tools already do before asserting a gap.

## Executive readout

Agent evaluation is an established product category. Current platforms already support meaningful combinations of tracing, datasets, evaluators, experiment runs, prompt/model comparisons, and debugging. A generic "dashboard to compare agent versions" is not a defensible differentiation claim.

The product opportunity must be narrower and evidence-led. A candidate direction is a product-facing release decision workflow that connects evaluator outcomes, tool-use quality, cost, latency, failure examples, and explicit release criteria. This is only a hypothesis; vendors already cover portions of this workflow.

## Competitive capability map

| Product | Documented capabilities from current sources | Product questions for teardown |
|---|---|---|
| **Arize Phoenix** | Open-source observability; OpenTelemetry tracing; evaluations; datasets; experiments; prompt playground and prompt management. | How does Phoenix connect trace-level evidence to dataset experiments? Which views are approachable to PMs versus engineers? What can be used self-hosted? |
| **LangSmith** | Evaluations before/after shipping; expert feedback; prompt iteration; side-by-side comparisons across prompt versions, model providers, and agent systems; framework-agnostic trace ingestion. | How does it structure the evaluation lifecycle? How visible are cost, latency, risk, and release criteria? How does human review fit? |
| **Braintrust** | Structured comparison of models using the same real inputs; dataset versioning; automated scoring; explicit quality, cost, and latency comparison. | How are datasets versioned? How does it handle real production data and annotations? How does it translate results into decisions? |
| **OpenAI Agent Evals** | Trace grading can inspect model calls, tool calls, guardrails, and handoffs; graders can test tool choice, handoffs, instructions, and workflow regressions. | How are traces and grader results surfaced to product stakeholders? What is the current lifecycle of platform APIs and product surfaces? |
| **Google Gen AI evaluation** | Final-response evaluation and trajectory evaluation; metrics include exact, in-order and any-order trajectory match, tool precision/recall, latency, and failure. Current docs label the feature Preview / Pre-GA. | How configurable are metrics? What are the usability and governance trade-offs? What does Preview status mean for production dependence? |

## Competitive facts and sources

### Arize Phoenix

- Project repository describes Phoenix as an open-source AI observability platform for experimentation, evaluation, and troubleshooting.
- Listed capabilities include tracing, evaluation, datasets, experiments, playground, prompt management, and MCP access.
- Dataset concepts describe examples with inputs and optional references/outputs/metadata; datasets can come from production, staging, evaluations, or manual creation.

Sources:
- https://github.com/Arize-ai/phoenix
- https://github.com/Arize-ai/phoenix/blob/main/docs/phoenix/datasets-and-experiments/concepts-datasets.mdx

### LangSmith

- Product page describes running evals before and after shipping, gathering expert feedback, and iterating on prompts.
- Comparison view supports side-by-side comparison of datasets across prompt versions, model providers, and agent systems.
- It states that it can ingest traces from frameworks beyond LangChain/LangGraph.

Sources:
- https://www.langchain.com/langsmith/evaluation
- https://docs.langchain.com/langsmith/evaluation

### Braintrust

- Article dated 20 March 2026 recommends running multiple models against the same real inputs and automatically scoring outputs.
- The article explicitly discusses quality, cost, and latency as model-selection factors.
- It describes dataset versioning so each experiment is pinned to the dataset version used.

Source:
- https://www.braintrust.dev/articles/how-to-test-ai-models

### OpenAI Agent Evals

- Current developer guide describes traces as end-to-end records of model calls, tool calls, guardrails, and handoffs.
- Trace grading can evaluate tool choice, handoff behavior, instruction adherence, and safety-related behavior.
- OpenAI's Evals documentation also describes datasets, graders, and evaluation workflows. Check the current deprecations page before depending on any specific legacy Evals surface or API.

Sources:
- https://developers.openai.com/api/docs/guides/agent-evals
- https://developers.openai.com/api/docs/guides/evals
- https://developers.openai.com/api/docs/guides/evaluation-best-practices
- https://developers.openai.com/api/docs/guides/evaluation-getting-started

### Google Gen AI evaluation

- Current documentation describes both final-response and trajectory evaluation.
- Trajectory metrics include exact match, in-order match, any-order match, precision, recall, single-tool-use, plus latency and failure reporting.
- The current documentation marks this evaluation feature as Preview / Pre-GA; do not imply general availability.

Source:
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-agents

## Initial strategic interpretation

1. **Do not compete on generic tracing.** Phoenix and LangSmith already provide strong observability and tracing workflows.
2. **Do not compete on generic experiment comparison.** Phoenix, LangSmith, and Braintrust already document experiment comparison across datasets and variants.
3. **Do not claim tool-trajectory evaluation is new.** Google and OpenAI both document trajectory or trace grading capabilities.
4. **Investigate decision usability.** Is there a gap between engineering-grade evaluation evidence and the product team's release decision? What exactly is missing, and for whom?
5. **Explore an opinionated narrow use case.** Tool-using customer-support or operations agents may provide a concrete domain for a reproducible benchmark, but this segment is not yet selected.

## What remains unknown

- Which target team experiences the most friction in converting evals into a ship/hold decision.
- Whether current products already solve the problem through configuration, templates, or integrations.
- Which metric trade-offs matter by use case.
- Whether PM-facing UX is a real buying need or merely a nice-to-have.
- How much integration effort teams would tolerate.
