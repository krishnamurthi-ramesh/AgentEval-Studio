# Product Teardown Framework

## 1. Product Overview & Market Positioning
- **Product Name & Vendor:**
- **Primary Value Proposition:**
- **Target Audience / Persona:**
- **Deployment & Hosting Model:** (Open-source self-hosted, cloud SaaS, hybrid)

## 2. Onboarding & Developer Experience
- **Time to First Evaluation / "Hello World":**
- **SDK & Framework Support:**
- **Configuration & Setup Complexity:**
- **Local vs Cloud Dependencies:**

## 3. Core Architecture & Trace Ingestion
- **Data Model:** (Traces, spans, sessions, runs)
- **Ingestion Protocol:** (OpenTelemetry, custom REST/gRPC API)
- **Storage & Query Layer:** (Postgres, ClickHouse, SQLite, DuckDB, proprietary)
- **Agent/Tool Representation:** How tool calls, arguments, and trajectories are captured.

## 4. Dataset & Experiment Management
- **Dataset Creation & Versioning:** How test cases are curated, split, and pinned.
- **Experiment Execution Workflow:** How variants (prompts, models, code) are executed against datasets.
- **Comparison UX:** How side-by-side runs are compared.

## 5. Evaluator Architecture
- **Built-in Evaluators:** (Exact match, regex, cosine similarity, schema validation)
- **LLM-as-Judge Support:** Custom prompts, rubrics, few-shot calibration.
- **Agent-Specific Evaluators:** Tool selection, argument validation, trajectory adherence, cycle detection.

## 6. Row-Level Inspection & Debugging
- **Drill-down Capabilities:** Trace inspection, span timeline, intermediate tool steps.
- **Explanations:** Why did an evaluator fail? Is rationale surfaced?
- **Filtering & Failure Clustering:** Slicing failures by metadata, tool, or error class.

## 7. Release Decision & Governance Workflows
- **Decision Support:** Does it help answer "Should we deploy this?"
- **Regression Detection:** Flagging regressions against a baseline.
- **Gate Criteria:** Configurable thresholds (pass/fail blocks).
- **Audit & Exportability:** Sharing decisions with cross-functional stakeholders.

## 8. Pricing & Commercial Model
- **Tiers & Metering:** Free tier limits, seat-based vs consumption-based pricing.
- **Self-Hosted Limitations:** Differences between open-source community edition and enterprise cloud.

## 9. Strategic Strengths, Weaknesses & The Gap
- **What they do exceptionally well:**
- **Where practitioners struggle / Friction points:**
- **Implication for AgentEval Studio:**
