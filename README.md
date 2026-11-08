# AgentEval Studio

**An open-source, decision-oriented evaluation workbench for tool-using AI agents.**

> Status: **Discovery / product definition.** This repository is an AI Product Management capstone in progress. The proposed product scope is a hypothesis, not a validated market gap. No production evaluator or agent runner is claimed yet.

AgentEval Studio explores a practical question for teams shipping AI agents:

**When prompt, model, tool schema, or agent logic changes, what evidence should a product team review before deciding to ship?**

The project will investigate a focused workflow for evaluating agent variants against a fixed, versioned dataset; inspecting tool selection and argument quality; comparing quality, latency, and cost; and producing a transparent release-readiness brief.

## Why this project exists

AI agent evaluation is an established category. Existing tools already support combinations of tracing, datasets, evaluators, experiments, and comparisons. AgentEval Studio will not claim to invent those capabilities. The project will first study the competitive landscape and test whether a narrower product opportunity exists around **turning evaluation evidence into an understandable, configurable product release decision**.

## Product thesis (unvalidated)

For product and applied-AI teams shipping tool-using agents, comparing variants can require interpreting multiple evaluator scores, traces, failure examples, latency, and cost. A focused decision workflow may help teams understand trade-offs and document a ship / hold / investigate recommendation without hiding the underlying evidence.

## Screenshot reference

The initial visual reference supplied with this project shows an experiment-comparison interface with three variants (`router_prompt_v1`, `router_prompt_v2`, `router_prompt_v3`), evaluator dimensions such as `Arguments` and `function_selection`, summary charts, filters, and row-level explanations. It informs the workflow to investigate; it is not a claim of original UI design or proof of a market gap.

## Discovery questions

1. Who owns the decision to release an agent or prompt change?
2. What evaluation artifacts do they use today: datasets, traces, spreadsheets, dashboards, human review, or CI checks?
3. Which failure types matter most for their use case: wrong tool, wrong arguments, unsafe action, incomplete task, bad final answer, latency, or cost?
4. How do they resolve trade-offs when one variant is more accurate but slower or more expensive?
5. What evidence is missing from existing tools, if any?
6. Would a product-facing decision brief add value beyond current evaluation platforms?

## Competitive products to study

| Product | Primary research focus | Official source |
|---|---|---|
| Arize Phoenix / Arize AX | Open-source tracing, datasets, evaluations, experiments, prompt iteration | https://github.com/Arize-ai/phoenix |
| LangSmith | Pre/post-deployment evaluation, trace inspection, experiment comparison, human feedback | https://www.langchain.com/langsmith/evaluation |
| Braintrust | Dataset-based model/agent testing, reproducible experiments, quality/cost/latency trade-offs | https://www.braintrust.dev/articles/how-to-test-ai-models |
| OpenAI Agent Evals | Trace grading across model calls, tools, guardrails, and handoffs | https://developers.openai.com/api/docs/guides/agent-evals |
| Google Gen AI evaluation | Final-response and trajectory evaluation, tool-call path metrics | https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-agents |

See [`docs/research/market-landscape.md`](docs/research/market-landscape.md) and the teardown briefs under [`docs/research/teardowns/`](docs/research/teardowns/).

## Proposed product workflow (to validate)

1. Create or import a versioned evaluation dataset.
2. Register two or more agent / prompt / model variants.
3. Run each variant against the same dataset.
4. Evaluate final-task quality and tool-use behavior.
5. Compare quality, latency, cost, and failure examples.
6. Review configurable release criteria and generate an evidence-linked decision brief.

This is a proposed workflow, not an implemented feature list.

## Non-goals for the first release

- Rebuilding a full observability platform.
- Replacing Arize Phoenix, LangSmith, Braintrust, or cloud evaluation products.
- Claiming one universal agent-quality score.
- Automatically shipping or rolling back agents without human approval.
- Claiming model-agnostic or framework-agnostic support before integrations are tested.

## Planned stack (provisional)

- Python for evaluation and data-processing logic.
- Streamlit for an initial local-first UI prototype.
- Pandas / DuckDB for dataset analysis.
- Provider adapters added only when a concrete use case requires them.
- Deterministic evaluators first; LLM-as-judge only with rubric, calibration, and human review.

## Repository roadmap

- [x] Create project charter and initial research map.
- [x] Record the supplied experiment-comparison screenshot as a product reference.
- [x] Complete competitive teardowns ([Arize Phoenix](docs/research/teardowns/arize-phoenix.md), [LangSmith](docs/research/teardowns/langsmith.md), [Braintrust](docs/research/teardowns/braintrust.md), [OpenAI Agent Evals](docs/research/teardowns/openai-agent-evals.md), [Google Gen AI Eval](docs/research/teardowns/google-agent-evaluation.md)).
- [x] Synthesize competitive gap & strategic differentiation ([Competitive Synthesis & Gap Analysis](docs/research/competitive-synthesis-and-gap.md)).
- [ ] Validate primary user and problem through a small number of practitioner conversations or public, attributable evidence.
- [ ] Select a narrow MVP wedge and define success criteria.
- [ ] Build a reproducible local demo with a small, clearly labelled benchmark dataset.
- [ ] Add tests, CI, documentation, and a demo walkthrough.
- [ ] Publish a case study with measured results and limitations.

## Evidence and integrity policy

- Distinguish **source fact**, **our interpretation**, **hypothesis**, and **measured result**.
- Cite current vendor documentation for product capabilities.
- Do not invent user interviews, customer metrics, model results, cost savings, or willingness to pay.
- Keep synthetic benchmark results explicitly labelled as synthetic.
- Report limitations and failed experiments alongside successful results.

## Contributing

This repository is in discovery. See [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening a contribution or suggesting a feature.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
