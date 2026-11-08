# Technical Capability Teardown: OpenAI Agent Evals

**Capability Focus:** Trace grading, tool selection, guardrails, handoffs, and agent-level failure modes  
**Vendor:** OpenAI  
**Research Date:** November 2026  
**Sources:** [OpenAI Agent Evals Guide](https://developers.openai.com/api/docs/guides/agent-evals), [OpenAI Evals Documentation](https://developers.openai.com/api/docs/guides/evals)

---

## 1. Overview & Context

OpenAI categorizes agent evaluation into trace grading across discrete lifecycle stages:
1. **Model Calls:** Prompt adherence and reasoning validity.
2. **Tool Selection & Calls:** Function routing and argument formatting.
3. **Guardrails & Safety:** Input/output safety filters.
4. **Handoffs:** Multi-agent transitions.

---

## 2. Agent-Level Failure Taxonomy

OpenAI defines agent-level evaluation along three core failure tiers:
- **Tool Routing Failures:** Wrong tool selected, omitted mandatory tool, or redundant calls.
- **Argument & Data Failures:** JSON schema mismatches, hallucinated entity parameters, or missing required keys.
- **Trajectory & State Failures:** Infinite loops, premature stops, or out-of-order execution.

---

## 3. Shortcomings for Day-to-Day Builders
- OpenAI Agent Evals is provided as architectural guidance and disparate API scripts; there is no standalone, local workbench or quality linter to inspect test suites before execution.
- Tightly optimized for OpenAI API formats; adapting to open-source models requires manual plumbing.
