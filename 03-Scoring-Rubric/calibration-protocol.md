# Calibration Protocol — Multi-Rater Scoring Alignment
## Ensuring Reproducible Evaluation Results

---

## Why Calibration Matters

If two people using the same rubric score the same response differently, the eval harness is broken. Calibration ensures:
- **Reproducibility:** Any evaluator produces consistent scores
- **Credibility:** Results can be defended in an interview
- **LLM-Judge alignment:** The automated judge matches human judgment

---

## Calibration Process (3 Raters Minimum)

### Step 1: Select Calibration Set
Pick 20 test cases from the golden dataset that span:
- 4+ categories (Current Events, Scientific, Technical, Adversarial)
- All 3 difficulty levels (easy, medium, hard)
- Expected scores across the full 1-5 range

### Step 2: Independent Scoring
Each rater independently scores all 20 responses using the rubric.
- No discussion before scoring
- Each rater records their scores AND written justification
- Time limit: 5 minutes per response maximum

### Step 3: Calculate Agreement
```
Inter-Rater Reliability Metrics:
- Cohen's Kappa (κ) for each pair of raters
- Krippendorff's Alpha for all raters combined

Target: κ > 0.7 (substantial agreement)
Minimum acceptable: κ > 0.6 (moderate agreement)
```

### Step 4: Reconciliation Session
For every case where raters disagree by ≥2 points:
1. Each rater explains their reasoning
2. Identify the ambiguity in the rubric that caused the disagreement
3. Add a clarifying rule to the rubric
4. Re-score that case to consensus

### Step 5: Document Anchor Examples
Create 2-3 "anchor" examples for each score level (1-5) on each dimension.

Example anchors for Factual Accuracy:

**FA = 5 (Anchor):**
> Query: "What is the speed of light?"
> Response: "The speed of light in a vacuum is approximately 299,792,458 meters per second"
> Why 5: Exact number, correct units, correct condition (vacuum)

**FA = 3 (Anchor):**
> Query: "When was Python created?"
> Response: "Python was created by Guido van Rossum in 1989 and is primarily used for web development"
> Why 3: Creator correct, year wrong (1991 not 1989), use case incomplete (not just web dev)

**FA = 1 (Anchor):**
> Query: "Who is the CEO of Google?"
> Response: "The CEO of Google is Larry Page" [as of 2026, it's Sundar Pichai]
> Why 1: Completely wrong, outdated by years, confidently stated

### Step 6: Re-test
After anchoring, score 10 new responses independently. κ should improve.

---

## LLM Judge Calibration

### Process
1. Human-score the 20 calibration cases
2. Run the same 20 through LLM judge (Claude Sonnet recommended)
3. Compare scores dimension-by-dimension
4. For each disagreement ≥ 2 points, add the case + human rationale as a few-shot example in the judge prompt
5. Re-run the LLM judge with updated prompt
6. Target: κ > 0.7 between LLM judge and human consensus

### Calibration Log Template

| Test ID | Dimension | Human Score | LLM Score | Δ | Resolution |
|---------|-----------|-------------|-----------|---|------------|
| CE-M-01 | FA | 4 | 3 | 1 | Acceptable — within tolerance |
| SM-H-01 | HE | 2 | 4 | 2 | LLM too generous on hedging — added few-shot example |

---

## Ongoing Calibration
- Re-calibrate every 4 weeks (model updates may change outputs)
- Add any new "surprising" scores to the anchor examples
- Track calibration drift over time

