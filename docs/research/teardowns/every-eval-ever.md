# Competitive Teardown: Every Eval Ever

**Project:** Every Eval Ever  
**Organization:** EvalEval Coalition  
**Primary Focus:** Crowdsourced evaluation metadata schema, benchmark registry, and score verification  
**Source:** [Every Eval Ever GitHub Repository](https://github.com/evaleval/every_eval_ever)

---

## 1. Overview & Vision
Every Eval Ever is an open coalition effort to map, index, and validate every AI evaluation benchmark published globally. It focuses on solving the benchmark metadata reproducibility crisis.

### Core Capabilities
- **Shared Schema:** Standardized JSON/YAML metadata schema describing benchmark provenance, licensing, dataset splits, and evaluation metrics.
- **Result Validation:** Tools to verify whether claimed benchmark scores were generated with identical prompt templates and evaluation harnesses.

---

## 2. Key Learnings for AgentEval Studio
- **Metadata Provenance Matters:** Community developers will only trust reusable evaluation packs if provenance (author, license, target model, holdout split) is clearly defined and validated.
- **The Gap:** Every Eval Ever is an archival catalog. It does not provide tools for developers to write, lint, or run tests on their own agents.

AgentEval Studio adopts the rigor of metadata schemas while focusing on **application-level developer authoring**.
