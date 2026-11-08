# Project Charter — AgentEval Studio

## 1. Project Overview & Vision
AgentEval Studio is an open-source evaluation and experiment workbench built specifically for tool-using AI agents. Its primary goal is to turn technical evaluation traces into clear, defensible, and actionable release decisions for applied AI engineering and product teams.

## 2. Core Objectives
1. **Developer Value:** Provide a transparent, local-first open-source workbench with low setup friction, reproducible benchmarks, and clean extensibility that AI developers actively want to clone, use, and star.
2. **AI PM Rigor:** Demonstrate end-to-end product management leadership through methodical competitive teardowns, customer problem discovery, evidence-based prioritization, technical architecture, and a structured go-to-market plan.

## 3. Scope & Boundary
### In Scope
- Evaluating multi-step tool-using agents against fixed, versioned datasets.
- Fine-grained multi-dimensional evaluation: Tool selection, argument correctness, execution success, trajectory flow, task completion, groundedness, latency, and cost.
- Side-by-side experiment comparison of prompt, model, and logic variants.
- Configurable release gate evaluation (pass/fail thresholds, regression criteria).
- Generating structured release decision briefs linking metrics to specific trace examples.

### Out of Scope (Initial Phase)
- General LLM observability / production tracing platform (e.g., competing with Datadog, Phoenix, LangSmith for live traffic).
- "Black-box" universal quality scores that aggregate metrics into an opaque single number.
- Automatic CD deployments or unverified autonomous rollbacks.

## 4. Key Milestones
- **Phase 1: Competitive Teardowns & Landscape Analysis** (Arize Phoenix, LangSmith, Braintrust, OpenAI Agent Evals, Google Gen AI Eval).
- **Phase 2: Problem Discovery & Target Persona Definition** (JTBD, pains, opportunity sizing).
- **Phase 3: Product Strategy & Opportunity Solution Tree** (Prioritization & MVP scoping).
- **Phase 4: PRD & Technical Architecture** (Data schema, evaluator interfaces, storage engine).
- **Phase 5: Implementation & Local UI** (Workbench core, deterministic + LLM-as-judge evaluators, comparison UI).
- **Phase 6: Benchmark & Validation** (Tool-agent failure cases, cost/latency trade-off tests).
- **Phase 7: Open-Source Launch & GTM** (Docs, demo video, release brief template, launch distribution).
