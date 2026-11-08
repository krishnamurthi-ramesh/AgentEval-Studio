# Competitive Teardown: EvalHub

**Product:** EvalHub  
**License:** Open Source  
**Primary Focus:** Evaluation orchestration, benchmark registry, collections, and framework adapters  
**Source:** [EvalHub GitHub Repository](https://github.com/eval-hub/eval-hub)

---

## 1. Product Overview & Context

EvalHub attempts to solve benchmark fragmentation by providing a unified catalog and execution adapter layer across disparate evaluation frameworks (LM-Eval-Harness, Lighteval, Inspect, Promptfoo).

### Core Capabilities
- **Unified Registry:** Catalogs evaluation benchmarks from various academic and open-source sources.
- **Adapter Layer:** Connects benchmark datasets to different execution engines.
- **Benchmark Collections:** Allows users to group benchmarks into thematic test suites.

---

## 2. Strengths & Limitations

### Strengths
- Reduces framework fragmentation by standardizing benchmark discovery.
- Cross-framework metadata mapping.

### Limitations
- **Registry Only:** EvalHub is a directory and orchestrator; it does not help users **author** new evaluations or lint their quality.
- **Foundation Model Bias:** Focuses on pretraining/finetuning benchmarks rather than agent API tool-calling workflows.
- **Low Authoring Guidance:** Zero conversational assistance or edge-case synthesis.

---

## 3. Takeaway for AgentEval Studio
EvalHub proves the need for standardizing evaluation definitions. However, standardizing metadata is not enough—builders need **guided authoring** and **test quality verification**. AgentEval Studio delivers that front-end creation wedge.
