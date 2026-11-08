# AgentEval Studio

**The Collaborative Evaluation Workspace for AI Builders.**  
*Create evaluations. Discover community benchmarks. Test agents. Share results. Improve together.*

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-Active_Development-green.svg)](https://github.com/krishnamurthi-ramesh/AgentEval-Studio)

> **Think of AgentEval Studio as "ChatPRD for AI Evals":** Just as ChatPRD replaced the blank page for product managers with guided, structured workflows, AgentEval Studio replaces ad-hoc testing with an AI-assisted evaluation copilot, a community library of reusable Eval Packs, deterministic tool-agent test suites, and transparent release-gate decision briefs.

---

## The Vision: From Blank Page to Ship-Ready Agent

Building AI applications and agents is fast, but evaluating them is painful:
- **The "Blank Page" Problem:** Defining comprehensive test cases, edge cases, tool schemas, and evaluation rubrics from scratch is tedious.
- **The Cold-Start Trap:** Traditional evaluation platforms are either passive observability collectors (Arize Phoenix, LangSmith) or academic foundation-model leaderboards (Hugging Face, Kaggle).
- **The "Metric Soup" Release Paralysis:** Dashboards show raw numbers, but teams struggle to reconcile quality gains vs. latency/cost regressions and decide whether to ship.

**AgentEval Studio bridges this gap with 5 interconnected capabilities:**

1. 🪄 **Eval Copilot:** Describe your AI application or agent in plain English. The Copilot guides you through generating structured test cases, expected tool calls, edge cases, and deterministic rubrics.
2. 📦 **Community Eval Library:** Discover, fork, contribute, and install pre-packaged evaluation suites (e.g., `tool-calling-accuracy`, `rag-hallucination-detector`, `customer-support-banking`, `prompt-injection-guardrails`).
3. ⚡ **Eval Runner & Comparator:** Run evaluations locally against candidate prompts, models, or agent functions. Evaluate tool selection, JSON schema conformance, argument entity correctness, and multi-step trajectory flow in milliseconds.
4. 🚦 **Release Policy Gates:** Configure explicit deployment rules (e.g., minimum tool precision, max latency regression, zero tolerance on high-risk tools).
5. 📋 **Automated Release Decision Brief:** Turn complex evaluation trade-offs into an executive-ready, evidence-backed sign-off brief (Markdown/PDF) linking directly to failing traces.

---

## Quickstart

### 1. Install & Launch the Workbench
```bash
# Clone the repository
git clone https://github.com/krishnamurthi-ramesh/AgentEval-Studio.git
cd AgentEval-Studio

# Install dependencies
pip install -e .

# Launch the interactive Streamlit workbench
streamlit run agenteval/app.py
```

### 2. Run an Eval Pack via Python SDK
```python
from agenteval import load_pack, evaluate_agent
from agenteval.gates import ReleaseGatePolicy

# 1. Load a pre-built community Eval Pack
pack = load_pack("customer_support_banking")

# 2. Run against your agent variant
results = evaluate_agent(
    pack=pack,
    agent_fn=my_banking_agent,
    variant_name="router_prompt_v2"
)

# 3. Check Release Policy Gates
policy = ReleaseGatePolicy(
    min_tool_accuracy=0.90,
    max_latency_regression_pct=15.0,
    zero_tolerance_tools=["transfer_funds", "cancel_subscription"]
)
brief = policy.evaluate(results, baseline_results=baseline_v1)
print(brief.status)  # READY_TO_SHIP | BLOCKED | REQUIRES_REVIEW
```

---

## Competitive Teardowns & PM Research

AgentEval Studio is grounded in rigorous competitive analysis of the AI observability and evaluation landscape:

- [Arize Phoenix Teardown](docs/research/teardowns/arize-phoenix.md): Open-source OTel tracing, RAG-centric benchmarks, and the absence of release gates.
- [LangSmith Teardown](docs/research/teardowns/langsmith.md): Prompt playground flywheel, LangGraph state tracing, human queues, and cloud SaaS lock-in.
- [Braintrust Teardown](docs/research/teardowns/braintrust.md): Git-like immutable datasets, AI proxy caching, Quality-Cost-Speed scorecards.
- [OpenAI Agent Evals](docs/research/teardowns/openai-agent-evals.md): Trace grading across tools, guardrails, and handoffs; multi-tiered failure taxonomy.
- [Google Gen AI Evaluation](docs/research/teardowns/google-agent-evaluation.md): Trajectory metrics (exact match, in-order match, precision, recall), latency/cost tracking.
- [Kaggle Community Benchmarks](docs/research/teardowns/kaggle-community-benchmarks.md): Model-centric leaderboards vs. application-level eval packs.
- [Hugging Face Community Evals](docs/research/teardowns/huggingface-community-evals.md): Academic benchmark submission vs. fast developer testing.
- [Weval Teardown](docs/research/teardowns/weval.md): Crowdsourced qualitative leaderboards vs. local developer execution.
- [Competitive Synthesis & The Gap](docs/research/competitive-synthesis-and-gap.md): Why we built "ChatPRD for Evals".

---

## Project Roadmap

- [x] **Phase 1 — Competitive Research & Teardowns:** 8 in-depth platform teardowns & synthesis.
- [x] **Phase 2 — Problem Discovery:** Personas (Dev Dave & PM Priya), JTBD framework, community flywheel.
- [x] **Phase 3 — Product Strategy:** "ChatPRD for Evals" identity, Opportunity Solution Tree, MoSCoW prioritization.
- [x] **Phase 4 — PRD & Architecture:** Eval Pack specification, deterministic evaluator formulas, release gate engine.
- [ ] **Phase 5 — Working Implementation:**
  - [ ] Core evaluator engine (Tool selection, JSON schema, entity match, trajectory match).
  - [ ] Eval Copilot generator (AI-guided rubric & test creation).
  - [ ] Community Eval Pack library (4 built-in starter packs).
  - [ ] Release Gate Policy engine & Decision Brief generator.
  - [ ] Interactive Streamlit Workbench UI.
- [ ] **Phase 6 — Benchmark & Validation:** Test banking and support agent scenarios with realistic failure modes.
- [ ] **Phase 7 — Open-Source Launch & GTM:** Documentation, sample agent, CI workflow, and community contribution guide.

---

## Contributing

We welcome community contributions! You can contribute in three ways:
1. **Contribute an Eval Pack:** Submit a new reusable evaluation pack under `agenteval/library/packs/`.
2. **Add an Evaluator:** Implement new deterministic or model-based evaluators.
3. **Report Edge Cases:** Share real-world tool-agent failure modes.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
