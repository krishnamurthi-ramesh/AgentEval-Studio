# Perplexity AI — LLM Product Eval Harness

## 🎯 One-Line Pitch
A systematic quality evaluation system for Perplexity AI that catches hallucinations, citation errors, and quality regressions before users do — the exact skill top AI PM teams hire for.

## What This Project Proves About Me
1. **I can define "good" for a probabilistic system** — not vibes, but measurable rubrics
2. **I build eval infrastructure** — golden datasets, automated pipelines, regression tracking
3. **I think in failure modes** — every test case maps to a real user pain
4. **I do competitive analysis with data, not opinions** — side-by-side benchmarks with scores
5. **I communicate technical findings to non-technical stakeholders** — executive summary + dashboard

## Project Structure
```
Project-1-Eval-Harness/
├── 01-Research/                    ← User research, competitive teardown, failure taxonomy
│   ├── perplexity-research-synthesis.md
│   ├── user-survey-template.md
│   ├── user-interview-guide.md
│   └── competitive-teardown.md
├── 02-Eval-Dataset/                ← The golden dataset (150+ test cases)
│   ├── golden-dataset.csv
│   ├── dataset-design-doc.md
│   └── adversarial-test-cases.csv
├── 03-Scoring-Rubric/              ← How each response is graded
│   ├── scoring-rubric.md
│   └── calibration-protocol.md
├── 04-Eval-Pipeline/               ← Automated evaluation scripts
│   ├── eval_runner.py
│   ├── llm_judge.py
│   └── requirements.txt
├── 05-Dashboard/                   ← Streamlit dashboard for results
│   ├── dashboard.py
│   └── sample_results.json
├── 06-Analysis-Report/             ← Findings and recommendations
│   ├── eval-results-analysis.md
│   └── executive-summary.md
└── 07-Deliverables/                ← Final portfolio-ready artifacts
    ├── PRD.md
    ├── one-page-problem-brief.md
    └── demo-walkthrough-script.md
```

## Timeline
- **Days 1-3:** Research, teardown, user survey/interviews
- **Days 4-5:** Design golden dataset and scoring rubric
- **Days 6-8:** Build eval pipeline and run evaluations
- **Days 9-10:** Build dashboard, write analysis, finalize deliverables

## Honest Label
`Evaluation system tested on [N] test cases across [M] query categories. Results are observational from public API access, not from internal Perplexity data.`

