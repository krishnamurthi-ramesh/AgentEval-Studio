# Executive Evaluation & Regression Analysis: Perplexity AI Quality Audit

- **Date:** November 2026
- **Dataset Size:** 151 Curated Queries across 10 Categories
- **Tested Models:** Perplexity Sonar (Default) vs. Perplexity Sonar Pro
- **Interactive Live Dashboard:** [View Live on Tableau Public](https://public.tableau.com/views/PerplexityAIQualityEvaluationHarness/PerplexityAIQualityEvaluationHarness?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

---

## 1. Executive Summary & North Star Findings

Over a rigorous benchmark of 151 production queries, Perplexity AI demonstrates high baseline utility for general information retrieval, but reveals significant degradation under epistemic stress (adversarial prompts, niche domains, and numerical constraints).

### Key Metrics Summary
- **Overall Mean Composite Score:** **3.84 / 5.0** (Grade: **B**)
- **Production Pass Rate (Score $\ge$ 3.0):** **84.8%**
- **Critical Failure Rate:** **6.6%** (10 out of 151 queries triggered automatic hard fails due to safety gaps or source fabrication)
- **Citation Hallucination Rate:** **26.2%** of all generated citations returned broken 404s, pointed to generic homepages, or failed to substantiate the specific metric claimed.

---

## 2. Dimensional Performance Breakdown

```
Dimension                Mean Score (1-5)    Risk Level
─────────────────────────────────────────────────────────────
Format & Usability            4.72           🟢 Minimal
Harmlessness & Safety         4.81           🟢 Minimal
Freshness (Recency)           4.18           🟡 Moderate
Factual Accuracy              3.94           🟡 Moderate
Completeness                  3.88           🟡 Moderate
Hedging & Calibration         3.71           🟠 High
Citation Accuracy             3.12           🔴 Critical Risk
```

### The Primary Failure Mode: "Authoritative Inaccuracy"
The biggest risk to user retention is not unreadable text or system crashes—it is **authoritative hallucination**.
When queried on high-entropy topics (e.g., local state policy changes or specific scientific RCT meta-analyses), Perplexity produces crisp, structured bullet points with superscript citation numbers. However, checking the raw URLs revealed:
1. **Source Mismatch:** 18% of cited links discussed the broad topic but did not contain the claimed statistic.
2. **Dead Links / Paywalls:** 8.2% of citations led to 404 errors or hard paywalls that prevented factual verification.

---

## 3. Category Vulnerability Heatmap

| Category | Mean Score | Primary Weakness |
|---|---|---|
| **Technical & Coding** | 4.35 | Code blocks accurate; occasionally misses newer framework API changes. |
| **Historical Facts** | 4.48 | Highest stability; minimal hallucination. |
| **Current Events & News** | 3.82 | Can conflate recent summit dates or previous year outcomes. |
| **Scientific & Medical** | 3.41 | Overconfident extrapolation from observational studies without clinical trial hedging. |
| **Adversarial / False Premise** | 2.95 | Struggles with negative constraint verification (e.g., asked to summarize a non-existent paper, it occasionally invents findings). |

---

## 4. Product Manager Recommendations & Roadmap

If I were the Product Manager leading Quality & Grounding at Perplexity, I would prioritize the following 3 initiatives on the product roadmap:

### 1. Pre-Generation Citation Verification Layer (P0)
- **Mechanism:** Implement a post-generation verification step that verifies whether the extracted claim has high semantic entailment with the fetched chunk before rendering the citation badge.
- **Expected Impact:** Reduces citation hallucination from 26% to under 8%, directly resolving the #1 user trust complaint.

### 2. Adaptive Hedging UI for Low-Grounding Confidence (P1)
- **Mechanism:** When retrieval confidence is low, replace assertive prose with visual hedging pills (e.g., *"Preliminary findings"* or *"Evidence is contested across sources"*).
- **Expected Impact:** Improves user trust calibration and prevents high-stakes embarrassment for enterprise/research users.

### 3. Automated Weekly CI/CD Evaluation Gate (P0)
- **Mechanism:** Incorporate this 151-case golden dataset into the pull-request pipeline. Any model fine-tune or routing tweak that causes > 2% drop in citation precision is automatically blocked from staging.

---

## 5. Artifacts & Reproducibility Links
- **Tableau Public Dashboard:** [Open Live Dashboard](https://public.tableau.com/views/PerplexityAIQualityEvaluationHarness/PerplexityAIQualityEvaluationHarness?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
- **Golden Benchmark Dataset:** `02-Eval-Dataset/golden-dataset.csv`
- **Evaluation Pipeline:** `04-Eval-Pipeline/eval_runner.py`
- **Scoring Rubric:** `03-Scoring-Rubric/scoring-rubric.md`

