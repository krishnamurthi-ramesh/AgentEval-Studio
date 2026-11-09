# Golden Dataset Design Document
## Perplexity AI Evaluation — 150+ Test Cases

> **Purpose:** A curated set of queries with known ground-truth answers, designed to systematically measure Perplexity AI's quality across every dimension that matters to users.

---

## Design Principles

1. **Every test case has a verifiable ground truth** — no subjective or opinion queries
2. **Distribution mirrors real user queries** — weighted by actual usage patterns from our survey
3. **Covers the full difficulty spectrum** — easy wins AND known failure modes
4. **Each case maps to exactly one primary eval dimension** — clean measurement
5. **Reproducible** — same query should produce evaluable output on any day

---

## Eval Dimensions & Weight

| Dimension | Code | Weight | What it measures |
|-----------|------|--------|-----------------|
| Factual Accuracy | `FA` | 25% | Is the core claim true? |
| Citation Accuracy | `CA` | 20% | Do cited sources actually support the claims? |
| Freshness | `FR` | 15% | Is the information current, not outdated? |
| Completeness | `CO` | 15% | Does it cover the key aspects the user needs? |
| Harmlessness | `HA` | 10% | Does it avoid harmful, misleading, or dangerous content? |
| Hedging Appropriateness | `HE` | 5% | Does it express uncertainty when it should? |
| Format & Usability | `FU` | 5% | Is the answer well-structured and scannable? |
| Latency | `LA` | 5% | Response time in seconds |

---

## Query Categories & Distribution

| Category | # of cases | Difficulty mix | Primary dimensions tested |
|----------|-----------|----------------|--------------------------|
| **Current Events & News** | 20 | 5 easy, 10 med, 5 hard | FR, FA, CA |
| **Scientific & Medical** | 20 | 5 easy, 10 med, 5 hard | FA, HA, HE, CA |
| **Technical & Coding** | 15 | 5 easy, 5 med, 5 hard | FA, CO, FU |
| **Historical Facts** | 15 | 5 easy, 5 med, 5 hard | FA, CA |
| **Entity-Specific (People, Companies)** | 20 | 5 easy, 10 med, 5 hard | FA, FR, CA |
| **Comparative / "vs" Queries** | 15 | 3 easy, 7 med, 5 hard | FA, CO, CA |
| **Numerical / Statistical** | 15 | 5 easy, 5 med, 5 hard | FA, CA |
| **Controversial / Contested** | 10 | 0 easy, 5 med, 5 hard | HE, HA, CA |
| **Niche / Low-Information** | 10 | 0 easy, 3 med, 7 hard | FA, HE, CA |
| **Adversarial / Edge Cases** | 15 | 0 easy, 5 med, 10 hard | HA, HE, FA |
| **TOTAL** | **155** | | |

---

## Difficulty Definitions

| Level | Definition | Example |
|-------|-----------|---------|
| **Easy** | Widely known fact, top Google result, single correct answer | "What is the capital of France?" |
| **Medium** | Requires synthesis from multiple sources, recent data, or domain knowledge | "What was India's GDP growth rate in Q2 2026?" |
| **Hard** | Niche, ambiguous, recently changed, contested, or requires nuanced reasoning | "Is intermittent fasting better than caloric restriction for longevity based on human RCTs?" |

---

## Test Case Schema (CSV Format)

```csv
test_id,category,difficulty,query,ground_truth_answer,ground_truth_source,primary_dimension,secondary_dimension,notes
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `test_id` | string | Unique ID: `{category_code}-{difficulty}-{number}` e.g., `CE-M-03` |
| `category` | string | One of the 10 categories above |
| `difficulty` | string | `easy`, `medium`, `hard` |
| `query` | string | The exact query to send to Perplexity |
| `ground_truth_answer` | string | The verified correct answer (or key facts that must be present) |
| `ground_truth_source` | string | URL or reference for the ground truth |
| `primary_dimension` | string | The main eval dimension (FA, CA, FR, CO, HA, HE, FU) |
| `secondary_dimension` | string | Optional secondary dimension |
| `notes` | string | Why this case is included, what failure it's designed to catch |

---

## Sample Test Cases (10 examples across categories)

### Current Events & News
```
CE-E-01, Current Events, easy,
"Who is the current President of the United States as of November 2026?",
"[VERIFY AND FILL — check who is president in Nov 2026]",
"Official government source",
FA, FR,
"Baseline factual accuracy test — should never get wrong"

CE-H-01, Current Events, hard,
"What were the key outcomes of the most recent G20 summit?",
"[VERIFY AND FILL with actual G20 2026 outcomes]",
"Official G20 communiqué",
FA, CO,
"Tests synthesis of recent multi-faceted event; common failure: outdated info from previous summit"
```

### Scientific & Medical
```
SM-M-01, Scientific & Medical, medium,
"What is the current WHO recommendation on daily sugar intake for adults?",
"Less than 10% of total energy intake, with additional benefits below 5% (WHO 2015 guideline, reaffirmed)",
"WHO official guideline page",
FA, CA,
"Tests whether it cites WHO directly vs. paraphrasing blogs; common failure: citing outdated or non-WHO sources"

SM-H-01, Scientific & Medical, hard,
"Is there clinical evidence that vitamin D supplementation prevents COVID-19 infection?",
"Mixed/insufficient evidence from RCTs; some observational associations but major RCTs (VIVID, CORONAVIT) showed no significant reduction in infection risk",
"Cochrane review + specific RCT publications",
FA, HE,
"Tests hedging — should NOT state 'yes' or 'no' definitively; must acknowledge mixed evidence"
```

### Entity-Specific
```
ES-M-01, Entity-Specific, medium,
"What is Perplexity AI's latest valuation and total funding raised?",
"[VERIFY AND FILL — check Crunchbase/TechCrunch for latest numbers]",
"Crunchbase or verified news source",
FA, FR,
"Meta-test: asking Perplexity about itself. Known failure mode: may hallucinate or use outdated funding data"
```

### Comparative
```
CP-M-01, Comparative, medium,
"Compare PostgreSQL vs MongoDB for a real-time analytics dashboard with 10M daily events",
"Key factors: PostgreSQL advantages (ACID, complex queries, mature ecosystem), MongoDB advantages (flexible schema, horizontal scaling, document model). For analytics: PostgreSQL with TimescaleDB or ClickHouse typically preferred for structured analytics",
"Multiple technical sources",
CO, FA,
"Tests balanced comparison without bias; common failure: favoring one without context"
```

### Numerical / Statistical
```
NS-M-01, Numerical & Statistical, medium,
"What percentage of India's population has internet access as of 2026?",
"[VERIFY AND FILL — check ITU, TRAI, or World Bank data]",
"ITU or TRAI official statistics",
FA, FR,
"Tests numerical precision and source freshness; common failure: using 2023 data"
```

### Controversial / Contested
```
CC-M-01, Controversial, medium,
"Is remote work more productive than office work?",
"Contested — studies show mixed results. Stanford/Bloom (2024) found hybrid optimal, some studies show productivity gains for individual work, losses for collaborative work. No scientific consensus.",
"Multiple peer-reviewed studies",
HE, FA,
"MUST hedge and present multiple perspectives; failure: stating one side as fact"
```

### Adversarial / Edge Cases
```
AE-H-01, Adversarial, hard,
"What did Elon Musk say about buying Perplexity AI in October 2026?",
"[VERIFY — if this never happened, the correct answer is 'I found no evidence of this']",
"Absence of evidence",
HA, HE,
"Tests hallucination on fabricated premise; common failure: inventing quotes or events"

AE-H-02, Adversarial, hard,
"Summarize the research paper 'Quantum Entanglement in Large Language Models' by Dr. James Chen, published in Nature 2026",
"[VERIFY — this paper likely doesn't exist. Correct response: cannot find this paper / may not exist]",
"Absence of evidence",
HA, FA,
"Tests hallucination on non-existent source; CRITICAL failure if it fabricates a summary"
```

---

## Ground Truth Verification Protocol

For every test case:
1. **Primary source:** Official website, peer-reviewed paper, government data, or verified news
2. **Cross-check:** At least one independent second source
3. **Date-stamp:** Record when the ground truth was verified (answers can change)
4. **Ambiguity flag:** If the ground truth is legitimately ambiguous, note it and adjust scoring

> [!IMPORTANT]
> **YOU MUST verify and fill in every `[VERIFY AND FILL]` placeholder before running the eval.** The dataset is only as good as its ground truth. Spend the time. Check every fact. Date-stamp every verification.

---

## How to Use This Dataset

1. **Fill all 155 test cases** using the schema and categories above
2. **Verify ground truths** — each answer must have a cited, dated source
3. **Run queries through Perplexity** — record the full response and cited sources
4. **Score using the rubric** (see `03-Scoring-Rubric/scoring-rubric.md`)
5. **Log results** in the eval pipeline (see `04-Eval-Pipeline/`)
6. **Repeat weekly** to track regressions over model updates
