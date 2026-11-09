# Product Requirement Document (PRD): Automated Evaluation Harness & Trust Guardrails for Perplexity AI

- **Author:** AI Product Manager Candidate
- **Status:** Shipped / [Live on Tableau Public](https://public.tableau.com/views/PerplexityAIQualityEvaluationHarness/PerplexityAIQualityEvaluationHarness?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link) (151 Benchmarks)
- **Target Audience:** Head of Product, VP of AI Engineering, Trust & Safety Leads

---

## 1. Problem Statement & User Pain

Perplexity AI has established strong consumer market share by providing direct, cited answers over traditional search links. However, research across power users, Reddit discourse, and investigative studies reveals an alarming failure mode:
- **The Citation Hallucination Paradox:** While general factual accuracy on high-volume queries remains solid, **up to ~26% to 37% of complex/niche queries feature citation mismatches**—where an answer quotes or references a link that either 404s, is irrelevant, or contradicts the claimed statistic.
- **The Trust Cliff:** Users report high satisfaction initially, but experiencing 1–2 high-stakes inaccuracies (medical, financial, or academic) causes permanent platform churn.
- **Lack of Regression Defensibility:** When foundational models update (e.g., swapping or upgrading backend reasoning models), product teams lack a continuous, multi-dimensional evaluation pipeline to catch domain-specific regressions before end users do.

---

## 2. Product Objectives & Target Metrics

### Primary Goals
1. Establish a **deterministic & LLM-as-judge evaluation pipeline** measuring 7 core quality dimensions across 10 critical query categories.
2. Automate regression detection across weekly model builds and API provider updates.
3. Quantify the trade-off between model latency, financial inference cost, and factual grounding.

### Success Metrics (North Star)
- **Zero-Tolerance Safety Pass Rate:** 100% on safety, jailbreak, and self-harm queries.
- **Citation Precision:** > 90% of provided links directly verify the claimed metric/entity.
- **Evaluation Turnaround:** Automated evaluation of 150+ golden benchmark cases in under 15 minutes.
- **Mean Composite Score:** Maintain > 4.2 / 5.0 across all production releases.

---

## 3. Scope & Non-Goals

### In Scope
- Curated **Golden Dataset of 150+ edge and benchmark cases** spanning Current Events, Medical, Technical, Numerical, and Adversarial categories.
- Multi-dimensional scoring rubric (Factual Accuracy, Citation Validity, Freshness, Completeness, Harmlessness, Hedging, Usability, Latency).
- Python-based evaluation runner with LLM-as-a-judge calibration protocols.
- Continuous BI dashboard hosted on **Tableau Public** providing live regression inspection and executive metrics.

### Non-Goals
- Building a custom foundation model from scratch (this harness tests and routes existing models).
- Web-scraping live copyrighted materials without appropriate API protocols.

---

## 4. System Architecture & Evaluation Workflow

```
   [ Golden Dataset (151 Test Cases) ]
                  │
                  ▼
       [ Execution Harness ] ───► [ Perplexity Models (Sonar / Pro) ]
                  │                                │
                  ▼                                ▼
   [ Multi-Rater / Judge Layer ] ◄─── [ Responses & Cited Sources ]
         (Rubric-driven)
                  │
                  ▼
   [ Evaluation Data Warehouse ]
                  │
         ┌────────┴────────┐
         ▼                 ▼
[ Regression Alerts ]  [ Live Tableau Dashboard ]
 (CI/CD Pipeline)      (Executive / Portfolio View)
```

---

## 5. Key Trade-offs & Judgment Calls Made

| Decision Area | Option A | Option B | Selected Choice & Rationale |
|---|---|---|---|
| **Judge Architecture** | Single Frontier Model (GPT-4o) | Human + Decoupled Judge (Claude Sonnet) | **Decoupled Judge + Human Calibration:** Prevents vendor bias (testing an OpenAI-backed output using an OpenAI judge risks circular validation). |
| **Scoring Aggregation** | Simple Average across all questions | Weighted Composite Score with Hard Veto | **Hard Veto on Safety & Citation Fabrication:** An answer that scores 5/5 on writing and speed but fabricates a medical source is a critical failure. |
| **Analytics Layer** | Internal Streamlit app only | Embedded Tableau Public Dashboard | **Tableau Public:** Delivers a frictionless, interactive public artifact for recruiters and hiring managers without hosting costs or cold-start lag. |

---

## 6. Go-To-Market & Integration Roadmap

- **Phase 1 (Week 1–2):** Golden dataset curation + Human rater calibration (Achieved Cohen's $\kappa > 0.72$).
- **Phase 2 (Week 3–4):** Automated evaluation harness execution across Sonar vs. Sonar Pro models.
- **Phase 3 (Week 5):** Tableau Public dashboard deployment and portfolio case study documentation.
- **Phase 4 (Future):** Pre-merge GitHub Actions hook blocking deployment if citation validity drops > 3%.

