# Technical Capability Teardown: Google Gen AI Agent Evaluation

**Capability Focus:** Final-response evaluation, tool trajectory evaluation, precision, recall, and execution paths  
**Vendor:** Google Cloud / Gemini Enterprise Agent Platform  
**Research Date:** November 2026  
**Status in Docs:** Preview / Pre-GA  
**Source:** [Google Cloud: Evaluate Agents in Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/evaluation-agents)

---

## 1. Overview & Trajectory Metrics

Google Cloud’s Gemini Enterprise Agent Platform formally separates final-response evaluation from trajectory path evaluation.

### Core Mathematical Trajectory Metrics
- **Exact Trajectory Match:** Binary check ($T_{actual} == T_{reference}$) on exact tool sequence, count, and arguments.
- **In-Order Trajectory Match:** Subsequence check ($T_{reference} \subseteq T_{actual}$ preserving order).
- **Tool Call Precision & Recall:** $\frac{|T_{actual} \cap T_{reference}|}{|T_{actual}|}$ (penalizes over-tooling) and $\frac{|T_{actual} \cap T_{reference}|}{|T_{reference}|}$ (penalizes under-tooling).

---

## 2. Limitations
- **Preview / Pre-GA:** Cloud enterprise feature requiring Vertex AI contracts.
- **No Guided Authoring:** Does not assist developers in creating trajectories or validating dataset quality before running evaluations.
