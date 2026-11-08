# Opportunity Decision Record (ODR): Build vs. No-Build

**Decision Date:** 8 November 2026  
**Status:** **APPROVED — Conditional GO**  
**Decision Title:** Narrow AgentEval Studio from generic evaluation dashboard to **Application-Level Eval Pack Authoring & Quality Linter**.

---

## 1. Context & The "No-Build" Filter

When evaluating product opportunities in AI engineering, the temptation is to build a comprehensive platform: a dashboard with tracing, datasets, model playgrounds, leaderboards, and execution runners.

However, competitive analysis reveals:
1. **Tracing & Dashboards are saturated:** Arize Phoenix, Langfuse, LangSmith, and Braintrust already provide production tracing and experiment comparison.
2. **Leaderboards are commoditized:** Hugging Face and Kaggle own foundation model benchmarks.
3. **Execution engines already exist:** Promptfoo and DeepEval are established, mature CLI test runners.

**Attempting to compete head-on across all five layers would result in a bloated, undifferentiated product that fails to gain traction.**

---

## 2. The Decision: What We Will Build

We narrow the initial product scope to the critical unmet workflow step: **Authoring and Linting Evaluation Packs**.

```
┌────────────────────────────────────────────────────────┐
│               The AgentEval Studio Wedge               │
└───────────────────────────┬────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
  [ Behaviour-to-Eval Copilot ]    [ Eval Quality Linter ]
  Turns informal user requirements  Checks for missing negative
  or failure reports into balanced  cases, ambiguous criteria,
  test cases & tool schemas.        and safety holes.
            │                               │
            └───────────────┬───────────────┘
                            ▼
               [ Export to Promptfoo / CI ]
               Runs through established test runners;
               reusable and zero vendor lock-in.
```

### Why this is a winning product decision:
1. **Solves the "Blank Page" Bottleneck:** Developers spend days trying to design good evaluation cases; our Copilot generates them in 60 seconds.
2. **Introduces Test Quality Assurance (The Linter):** No existing tool checks whether the test suite itself is defective or overfitted before execution.
3. **Synergistic, Not Competitive with Established Tools:** By exporting to Promptfoo YAML and DeepEval, we do not ask users to rip and replace their existing test runners; we make their existing runners 10x more useful!
4. **Natural Community Flywheel:** Developers share evaluation packs via GitHub pull requests, creating a decentralized library of tests for real-world agent behaviors.

---

## 3. Decision Matrix

| Dimension | Option A: Full Observability Platform | Option B: Community Leaderboard | Option C: Eval Pack Authoring & Quality Linter (CHOSEN) |
|---|---|---|---|
| **Market Saturation** | Extreme (Phoenix, Langfuse, Datadog) | High (Hugging Face, Kaggle) | **Low (Unserved authoring friction)** |
| **Developer Adoption Speed** | Slow (requires OTel setup) | Slow (cold-start content trap) | **Instant (generates tests in 60s)** |
| **Maintenance Overhead** | Heavy (distributed DBs, collectors) | Heavy (GPU compute infrastructure) | **Lightweight (client-side & CLI)** |
| **Integration with Existing Tools** | Competitive / Displace | Siloed | **Complementary (Exports to Promptfoo)** |
| **Strategic Verdict** | ❌ REJECT | ❌ REJECT | ✅ **APPROVED (Conditional GO)** |
