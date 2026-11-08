# Demand Signals & User Evidence Log

**Research Date:** November 2026  
**Purpose:** Maintain strict factual auditability of user pain points, practitioner quotes, and public GitHub issues.

---

## 1. Reddit r/Rag: Dataset Creation Bottleneck
- **URL:** [https://www.reddit.com/r/Rag/comments/1wdlgu1/how_do_you_create_reliable_evaluation_datasets/](https://www.reddit.com/r/Rag/comments/1wdlgu1/how_do_you_create_reliable_evaluation_datasets/)
- **Practitioner Problem:**
  > *"How do you create reliable evaluation datasets? I've been spending hours or more than a week trying to build evaluation datasets. When I write them manually, they're reliable but too small (20-30 examples). When I use an LLM to generate synthetic test cases, I can't trust whether the ground truth is actually right without reading every single one."*
- **Significance:** Demonstrates the core friction: builders lack guided tools that bridge manual precision with automated coverage.

---

## 2. Arize Phoenix: Public GitHub Issue Log

### Issue #17733: "Add holdout examples to eval suites"
- **URL:** [https://github.com/Arize-ai/phoenix/issues/17733](https://github.com/Arize-ai/phoenix/issues/17733)
- **Problem:** Practitioners iterating on prompts in Phoenix frequently overfit to their test dataset. They requested a built-in holdout split mechanism to guarantee generalizability before deploying.
- **AgentEval Studio Response:** Our **Eval Quality Linter** checks whether an Eval Pack includes a holdout validation split.

### Issue #17715 & #17723: "Simplify and standardize evaluator creation"
- **URL:** [https://github.com/Arize-ai/phoenix/issues/17715](https://github.com/Arize-ai/phoenix/issues/17715)
- **Problem:** Configuring evaluators in Phoenix requires navigating fragmented APIs and writing repetitive boilerplate.
- **AgentEval Studio Response:** The **Behaviour-to-Eval Copilot** generates evaluators, schemas, and rubrics automatically from plain-language requirements.

### Issue #17721: "Add spend limits for evaluator runs"
- **URL:** [https://github.com/Arize-ai/phoenix/issues/17721](https://github.com/Arize-ai/phoenix/issues/17721)
- **Problem:** Running LLM judges on large datasets burns API credits unexpectedly.
- **AgentEval Studio Response:** **Deterministic-first grading** (tool precision, schema validation, entity matching) executes locally in milliseconds with $0 in API spend.

---

## 3. Promptfoo: Tool-Call Assertion Requests
- **Source:** Promptfoo Discussions & Issues
- **Problem:** Promptfoo users requested better assertions for tool calls without having to instrument complete OpenTelemetry trace pipelines.
- **AgentEval Studio Response:** We export tool-call tests into native Promptfoo assertions (`is-json`, `equals`, `javascript` checks) so existing Promptfoo users get first-class agent assertions.

---

## 4. DeepEval: Rubric Invalidation & Score Caching
- **Source:** DeepEval GitHub Issues
- **Problem:** Cached evaluation scores were being silently reused even after developers modified the evaluation rubric.
- **AgentEval Studio Response:** Immutable pack versioning and checksum verification on every evaluation pass.
