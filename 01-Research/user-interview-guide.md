# User Interview Guide — Perplexity AI Eval Harness
## Semi-Structured Interview Protocol (8-10 Power Users)

> **Duration:** 25-30 minutes per interview
> **Format:** Video call (Zoom/Google Meet) or in-person
> **Recording:** Ask permission. Transcribe for quotes.
> **Recruitment:** LinkedIn DM to heavy Perplexity users, Reddit r/perplexity contributors, Twitter/X power users

---

## Pre-Interview Setup
- [ ] Confirm participant uses Perplexity 3+ times/week
- [ ] Get consent for recording and anonymized quotes
- [ ] Have Perplexity open on your screen for live testing
- [ ] Prepare note-taking template (below)

---

## Interview Flow

### Part 1: Warm-up & Context (3 min)

> *"Thanks for joining. I'm researching how people use AI search tools and where they break down. There are no right or wrong answers — I'm especially interested in when things go WRONG."*

1. **Tell me about your workflow. When does Perplexity come into your day?**
   - *Probe:* What triggers you to open Perplexity vs. Google vs. ChatGPT?
   - *Probe:* Is it your first stop or your last resort?

2. **What's the most recent thing you searched on Perplexity?**
   - *Probe:* Did you get a good answer? How did you decide it was good?

---

### Part 2: Trust & Verification Behavior (7 min)

3. **When you read a Perplexity answer, do you click the citations?**
   - *Probe:* Always? Only for certain topics? What triggers a click?
   - *Probe:* Have you ever clicked a citation and found it doesn't support the claim?

4. **Tell me about a time Perplexity got something WRONG.**
   - *Probe deeply:* What was the query? What did it say? How did you realize it was wrong?
   - *Probe:* What did you do next?
   - *Probe:* Did it affect your trust going forward?

5. **Are there topics you've STOPPED asking Perplexity about?**
   - *Probe:* What happened that made you stop?
   - *Probe:* Where do you go instead for that topic?

6. **How do you decide whether to trust an answer without checking?**
   - *Probe:* Is it the confidence of the language? The number of citations? The source quality?

---

### Part 3: Live Testing (10 min)

> *"I'd love to try a few queries together and hear your reaction in real-time."*

Run these 5 queries live with the participant watching. Ask them to "think aloud":

| # | Query | What we're testing |
|---|-------|--------------------|
| 1 | "What is [their company/university]'s revenue/ranking in 2026?" | Entity-specific factual accuracy, freshness |
| 2 | "Compare [two products they know well]" | Comparative accuracy, bias, source diversity |
| 3 | "Is [a recent controversial claim] true?" | Handling of contested information, hedging |
| 4 | "What are the side effects of [a common medication they know]?" | High-stakes accuracy, safety, source quality |
| 5 | A query about a niche topic they're expert in | Expert-level accuracy, depth, hallucination |

**For each query, ask:**
- "What's your immediate reaction to this answer?"
- "Anything here that seems off or suspicious?"
- "Would you trust this enough to act on it / share it?"
- "If you were grading this answer A through F, what grade?"

---

### Part 4: Ideal State & Wrap-up (5 min)

7. **If you could redesign one thing about how Perplexity presents answers, what would it be?**
   - *Probe:* Is it about the answer itself, the sources, the confidence level, the format?

8. **Imagine Perplexity showed a "confidence score" next to each answer — like "85% confident." Would that change how you use it?**
   - *Probe:* Would you trust high-confidence answers more? Would low-confidence answers be useful or annoying?

9. **What would make you trust Perplexity enough to use it for a work presentation or an important decision?**

10. **Anything else about your experience that we haven't covered?**

---

## Note-Taking Template

Copy this for each interview:

```
## Interview #[N] — [Date]

**Participant:** [Anonymous ID, e.g., P01]
**Profile:** [Role, usage frequency, plan type]
**Duration:** [X] minutes

### Key Quotes (verbatim)
1. "___"
2. "___"
3. "___"

### Failure Stories
- Story 1: [Query] → [What went wrong] → [What they did]
- Story 2: ...

### Trust Signals
- What makes them trust: ___
- What breaks trust: ___
- Verification behavior: ___

### Live Test Reactions
| Query | Grade | Key reaction |
|-------|-------|-------------|
| 1     |       |             |
| 2     |       |             |
| 3     |       |             |
| 4     |       |             |
| 5     |       |             |

### Topics They Avoid on Perplexity
- ___

### Ideal State / Wish
- ___

### My Observations (non-verbal, hesitations, surprise)
- ___
```

---

## Synthesis Framework

After all 8-10 interviews, synthesize using this structure:

### 1. Failure Taxonomy (from interview data)
| Failure Type | Frequency (how many participants mentioned) | Severity (user impact) | Example |
|---|---|---|---|

### 2. Trust Model
```
Trust = f(Source Quality, Answer Confidence, Past Experience, Topic Sensitivity)
```
Map which factors matter most across participants.

### 3. Verification Behavior Segments
- **Always Verify:** Who? Why? What triggers?
- **Selective Verify:** What topics trigger checking?
- **Never Verify:** Who? What's at risk?

### 4. Top 5 Insights (with quote evidence)
Each insight needs: the finding, the participant count, 1-2 supporting quotes, and the implication for the eval harness.

