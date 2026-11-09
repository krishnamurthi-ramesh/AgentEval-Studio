# Perplexity AI — Research Synthesis for LLM Product Eval Harness

> **Project:** LLM Product Eval Harness (AI PM Portfolio — Project 1)
> **Date:** November 2026
> **Purpose:** Comprehensive research to inform the design of a product-quality evaluation framework targeting Perplexity AI's answer engine.

---

## Table of Contents

1. [Product Overview & Current State](#1-product-overview--current-state)
2. [Pricing & Tier Structure](#2-pricing--tier-structure)
3. [Documented Failure Modes](#3-documented-failure-modes)
4. [User Complaints (Categorized)](#4-user-complaints-categorized)
5. [Competitive Landscape & Benchmarks](#5-competitive-landscape--benchmarks)
6. [Industry Eval Methodology — Best Practices](#6-industry-eval-methodology--best-practices)
7. [Implications for Eval Harness Design](#7-implications-for-eval-harness-design)
8. [Sources](#8-sources)

---

## 1. Product Overview & Current State

### 1.1 What Perplexity AI Is

Perplexity AI is a **Retrieval-Augmented Generation (RAG) answer engine** — it queries the live web for every prompt, retrieves relevant documents, and synthesizes a cited answer grounded in those sources. Unlike pure LLMs (ChatGPT, Claude), Perplexity's entire UX is designed around **inline, numbered source citations** (`[1][2][3]`), making it a "search engine that answers" rather than a "chatbot that sometimes Googles."

As of November 2026, Perplexity has expanded far beyond its original search-answer scope into a full **multi-model agentic productivity platform**.

### 1.2 Core Product Features (Nov 2026)

| Feature | Description |
|---|---|
| **Standard AI Search** | RAG-based Q&A with inline citations from live web results. |
| **Deep Research** | Multi-step agentic research workflow — iterates across multiple queries, reads full pages, synthesizes long-form reports. Integrated into the Computer architecture for faster execution. |
| **Perplexity Computer** | Overarching agent layer that coordinates across ~20 AI models, routing sub-tasks to the best-suited model (reasoning, extraction, synthesis). Can interact with local files, desktop apps, and workflows. Available on Mac, Windows, Linux. |
| **Model Council** | Runs a single query simultaneously across multiple frontier models and merges insights side-by-side. Available on Max and Enterprise Max tiers. |
| **Comet Browser** | Perplexity's native browser (macOS, Windows, iOS, Android). Embeds an AI assistant for in-page research, auto-summarization, form-filling, and autonomous multi-step web tasks. Enterprise MDM/security policy controls available. |
| **Brain & Memory Layer** | Persistent context and memory that adapts to user preferences over time. |
| **Learn Step-by-Step** | Educational mode that breaks down complex concepts iteratively. |
| **Create Files & Apps** | Generate functional spreadsheets, documents, and lightweight web apps from conversational prompts (formerly "Labs"). |
| **Agent API** | Developer-facing API for building live-web-backed applications. Replaces legacy Sonar chat API. |
| **Decisions API** | Grounds automated decision-making frameworks in real-time web data. |
| **Email Task Submission** | Send tasks directly via `computer@perplexity.com`. |

### 1.3 Key Integrations & Partnerships

- **Samsung Galaxy S26:** OS-level integration into Galaxy system apps and Bixby search.
- **Microsoft 365 & Slack:** Computer and agent workflows embedded in Word, Excel, PowerPoint, Outlook, Teams, and Slack.
- **CrowdStrike:** Enterprise security partnership for Comet browser deployment.

### 1.4 Underlying Models

Perplexity routes across ~20 models including frontier reasoning models, open-weight architectures, and specialized configurations. Pro users can select specific models (e.g., Claude, Gemini) for certain queries. The system automatically selects models for Computer workflows.

---

## 2. Pricing & Tier Structure

### 2.1 Individual Plans

| Tier | Price | Key Features |
|---|---|---|
| **Free** | $0/mo | Standard AI search, limited daily Pro searches, basic models |
| **Pro** | $17/mo (annual) / $20/mo (monthly) | Deep Research, Perplexity Computer access, 4,000 bonus credits, file/document analysis, image generation, model choice, premium data sources (PitchBook, Statista) |
| **Max** | $167/mo (annual) / $200/mo (monthly) | Maximum Computer usage, 35,000 bonus + 10,000 recurring monthly credits, frontier models, Model Council, highest memory limits, priority feature access |

### 2.2 Enterprise Plans (Per Seat)

| Tier | Price | Key Features |
|---|---|---|
| **Enterprise Pro** | $34/seat/mo (annual) / $40/seat/mo (monthly) | SSO, SOC 2 Type II, shared Projects, File Connectors, 500 monthly + 8,500 bonus credits/seat |
| **Enterprise Max** | $271/seat/mo (annual) / $325/seat/mo (monthly) | SCIM provisioning, audit logs, custom data retention, multi-model comparison, 15,000 monthly + 40,000 bonus credits/seat |

### 2.3 Credit System

Perplexity Computer's agentic workflows consume credits (metered). Extra credits: ~100 credits for $1.

---

## 3. Documented Failure Modes

### 3.1 Failure Mode Taxonomy

Based on research, Perplexity's failure modes cluster into **5 distinct categories**:

#### FM-1: Citation Hallucination (The Core Weakness)

**What:** Perplexity generates URLs or references that look legitimate but either lead to dead pages, don't contain the claimed information, or are completely fabricated.

**Hard data:** The **Columbia Journalism Review (CJR)** study found a **~37% citation hallucination rate** — over a third of Perplexity citations were misattributed, contained dead/unmatched links, or didn't support the specific claim made.

**Sub-types:**
- **Dead/non-existent links:** Generated URLs that 404 or never existed.
- **Misattributed claims:** Source is real, but Perplexity misinterprets the context or weaves text from multiple unrelated sources into a false conclusion.
- **"Real Org, Fake Report" trap:** Cites a legitimate entity (WEF, McKinsey, a government agency) but invents the specific study title, date, or statistic.

#### FM-2: Confident Misinformation ("Authoritative Inaccuracy")

**What:** Errors are presented with an air of verified fact — clean paragraphs, inline citation numbers, professional formatting — creating undeserved trust. The danger is NOT blatant nonsense; it's plausible, well-formatted, wrong answers that users don't question.

**Example pattern:** User queries Perplexity with a false premise ("Explain how Company X's 2024 merger caused their stock crash" when no merger happened). Instead of correcting the premise, Perplexity finds tangential snippets and weaves them into a coherent, fabricated narrative.

#### FM-3: Reasoning vs. Factuality Paradox

**What:** Integration of advanced reasoning models improves multi-step analysis but introduces a trade-off: the reasoning model overcomplicates straightforward retrieval tasks or hallucinated granular data points (specific stats, dates, percentages) while maintaining an intensely confident tone.

**Key risk area:** Deep Research mode, which chains multiple model calls and can amplify small errors through multiple reasoning steps.

#### FM-4: Niche/Recent Topic Hallucination

**What:** When prompted about very recent events, obscure domains, or complex verticals (legal analysis, niche SaaS, specialized financial metrics), the system runs out of grounding evidence and "fills in the gaps" with plausible fabrication.

#### FM-5: Source Quality Contamination

**What:** Perplexity indexes the live web and can pull from low-authority blogs, content-farm aggregators, or AI-generated SEO articles. If multiple low-quality sites echo misinformation, Perplexity's ranking algorithm treats them as consensus — presenting false rumors as verified facts.

**Additional sub-type:** Context window overload during PDF/document analysis — model maps answers to wrong sections, confidently cites a page number or table that contains entirely different figures.

### 3.2 Failure Mode Summary Table

| ID | Failure Mode | Severity | Frequency | Detection Difficulty |
|---|---|---|---|---|
| FM-1 | Citation Hallucination | **Critical** | ~37% of citations (CJR) | Medium — requires clicking through links |
| FM-2 | Authoritative Inaccuracy | **Critical** | Unknown but systemic | **High** — formatted to look trustworthy |
| FM-3 | Reasoning-Factuality Paradox | **High** | Elevated in Deep Research | Medium — cross-reference granular data |
| FM-4 | Niche/Recent Hallucination | **High** | Elevated in specialized domains | Medium — domain expertise needed |
| FM-5 | Source Quality Contamination | **Medium** | Variable by topic | Low — source authority is checkable |

---

## 4. User Complaints (Categorized)

Based on Reddit (r/perplexity_ai, r/ArtificialIntelligence) and review analysis:

### Category 1: Pricing & Subscription Issues
- **"Bait-and-switch":** Annual subscribers renewed expecting "unlimited" Pro searches and Deep Research, then faced unexpected limitations or restructured tiers.
- **Billing bugs:** Difficulty reaching human support; automated responses fail to resolve subscription/billing issues.
- **Credit confusion:** Opaque credit system for Computer workflows makes it hard to predict costs.

### Category 2: Product "Enshittification"
- **Feature gating:** Features previously available to Pro users locked behind Max tier or moved into ecosystem add-ons (Comet browser, Computer).
- **Aggressive UI defaults:** Updates push newer tools or task integrations automatically; hard to customize or disable.
- **Removal of features:** Users feel the product keeps removing access to things they paid for.

### Category 3: Model & Output Quality
- **Model inconsistencies:** Using third-party models through Perplexity feels less optimized vs. subscribing directly to Claude Pro or ChatGPT Plus.
- **Deep Research unreliability:** Mixed results in complex research tasks.
- **Hallucination frustration:** Users share specific examples of wrong answers that "looked right."

### Category 4: Competition & Migration
- **"Wrapper" criticism:** Perplexity is seen as a wrapper around other models; Google Gemini now offers built-in web search + auto-citations for free.
- **User migration:** Long-time users reporting switching to ChatGPT Plus, Claude Pro, or Google Gemini for daily use.
- **Value proposition erosion:** At $17-200/mo, increasingly hard to justify vs. free alternatives with similar capabilities.

---

## 5. Competitive Landscape & Benchmarks

### 5.1 Head-to-Head Accuracy Comparison

| Metric | Perplexity AI | ChatGPT Search | Google AI Overviews |
|---|---|---|---|
| **Hallucination Rate** | ~5% (general queries) | ~7-12% | Low for factual; variable for complex |
| **Citation Hallucination** | ~37% (CJR study) | Not measured separately | N/A (different format) |
| **Architecture** | RAG-first (every query triggers web search) | General-purpose LLM + search tool | Search index + AI synthesis layer |
| **Citation Style** | Inline numbered `[1][2]` per-sentence | Aggregated carousels / end-notes | Carousel / card format |
| **Source Preference** | Recent articles, Reddit, 30-day window | Tier-1 sources, news networks, Wikipedia | SEO-ranked via E-E-A-T signals |

### 5.2 Best-In-Class by Use Case

| Use Case | Winner | Why |
|---|---|---|
| **Academic/Scientific Research** | **Perplexity** | Lowest general hallucination rate, superior citation format, multi-model selection |
| **Complex Reasoning & Multi-Step Logic** | **ChatGPT** | Deeper reasoning tracks, native code execution, stronger analytical chains |
| **Local Info / Daily Logistics / News** | **Google** | Unmatched infrastructure: Maps, local business data, flight/weather, real-time news indexing |
| **Source Transparency & Verification** | **Perplexity** | Every sentence anchored to numbered, clickable inline link |
| **Enterprise Workflow Integration** | **Tie** | Perplexity (M365/Slack integration) vs. Google (Workspace native) vs. OpenAI (enterprise APIs) |

### 5.3 Key Competitive Dynamics

1. **Google's free AI Mode** is the existential threat — it offers RAG-style answers with citations backed by the world's best search index, for free.
2. **ChatGPT Search** is weaker on citation fidelity but stronger on reasoning — users with complex analytical needs prefer it.
3. **Perplexity's moat** is citation UX and multi-model routing, but this is narrowing as competitors add similar features.

---

## 6. Industry Eval Methodology — Best Practices

### 6.1 Core Principle: Application-Specific Evals Over Academic Benchmarks

The industry has moved decisively from general benchmarks (MMLU, HellaSwag) to **application-specific, production-gated evaluation pipelines**. General benchmarks reveal almost nothing about how a model performs on YOUR specific domain data and prompts.

### 6.2 The 6-Layer Eval Framework

#### Layer 1: Golden Dataset Construction
- Curate a versioned dataset of application-specific inputs → expected behaviors/reference outputs.
- **Seed with real failures:** Use production failure cases, edge cases from user support tickets, not idealized test prompts.
- Refresh weekly. Target 200+ test cases minimum.
- Use synthetic data generators (RAGAS, framework-native tools) to scale the dataset without losing signal.

#### Layer 2: Multi-Metric Strategy (Three Families)

| Family | What It Measures | Speed/Cost | Examples |
|---|---|---|---|
| **Deterministic** | Exact matches, schema validation, tool-call args | Fast, cheap | JSON parse success, URL validity check, exact answer match |
| **Semantic / Rubric-Based (LLM-as-Judge)** | Faithfulness, relevance, harmfulness | Moderate | Frontier model grades output against rubric |
| **Composite Agent/RAG** | Multi-step trajectory quality | Slow, expensive | Retrieval relevance, citation validity, planning accuracy, tool-selection correctness |

#### Layer 3: LLM-as-Judge Calibration
- Baseline judge performance against human expert judgments.
- Take 50+ historical failure cases, have domain expert grade with binary pass/fail.
- Tweak judge system prompt until verdicts align with human intuition.
- Use a powerful frontier model as judge — smaller/older judges fail consistency tests.

#### Layer 4: CI/CD Integration ("Shift-Left")
- Trigger automated eval on every prompt change, model version change, retriever config change.
- Treat eval scores as unit test pass/fail — block merges on regression past threshold.

#### Layer 5: Continuous Production Monitoring
- OpenTelemetry-compatible tracing for every input, retrieved chunk, sub-agent call, output.
- Continuously sample 5-10% of live production traffic.
- Run async evaluations on traces to detect data drift, latency spikes, silent hallucinations.

#### Layer 6: Separate Evaluation from Guardrails
- **Async evaluators** = background metrics, trend tracking, regression flagging (for engineering team).
- **Runtime guardrails** = synchronous, inline interception of malicious inputs, toxic content, prohibited actions (millisecond-level).
- Never confuse the two — offline evaluators cannot stop harmful live content due to latency.

### 6.3 Key Eval Frameworks & Tools in Use

| Tool / Framework | Purpose |
|---|---|
| **RAGAS** | RAG-specific evaluation (faithfulness, answer relevancy, context precision/recall) |
| **DeepEval** | Open-source LLM evaluation with 14+ metrics, pytest integration |
| **Galtea** | Enterprise LLM evaluation platform with calibrated judges |
| **FutureAGI** | Production LLM observability and eval |
| **OpenTelemetry** | Tracing foundation for production monitoring |
| **Mastra** | Agent evaluation framework |
| **LaunchDarkly (AI Configs)** | Feature-flagged model/prompt rollouts with eval gates |

---

## 7. Implications for Eval Harness Design

Based on this research, the eval harness for Perplexity should prioritize:

### 7.1 Priority Eval Dimensions (Ranked)

| Priority | Dimension | Why | Metric Type |
|---|---|---|---|
| **P0** | **Citation Validity** | 37% citation hallucination rate is the #1 documented failure; this IS Perplexity's core value prop | Deterministic (URL check) + Semantic (content match) |
| **P0** | **Factual Accuracy** | Confident misinformation is the highest-risk failure mode | LLM-as-Judge with rubric |
| **P1** | **Source Quality** | SEO spam / content-farm contamination creates systematic errors | Deterministic (domain authority scoring) |
| **P1** | **False Premise Handling** | "Yes-man" search bias is a documented, testable failure pattern | Adversarial test cases |
| **P1** | **Niche Domain Accuracy** | Legal, financial, medical, technical verticals trigger elevated hallucination | Domain-specific golden datasets |
| **P2** | **Deep Research Fidelity** | Multi-step reasoning amplifies errors; high-value feature for Pro/Max users | Composite agent metrics |
| **P2** | **Recency Accuracy** | Recent events trigger gap-filling hallucination | Time-stamped golden dataset |
| **P3** | **Response Latency** | User experience metric; Deep Research can be slow | Deterministic (timing) |
| **P3** | **Cross-Model Consistency** | Model Council and model selection create variance | Statistical comparison |

### 7.2 Test Case Categories to Build

1. **Citation Audit Battery:** 100+ queries across domains; check every citation for (a) URL validity, (b) content-claim alignment, (c) source authority.
2. **False Premise Battery:** 50+ queries with deliberately false premises to test correction vs. confabulation behavior.
3. **Niche Domain Battery:** 50+ queries in legal, medical, financial, and technical domains with known-correct answers from authoritative sources.
4. **Recency Battery:** 50+ queries about events from the past 7/30/90 days with verified ground truth.
5. **Adversarial Source Battery:** Queries where SEO spam / content farms dominate search results; test whether Perplexity elevates low-quality sources.
6. **Deep Research Regression Suite:** 25+ multi-step research tasks with verified expected outputs and intermediate step validation.

### 7.3 Architecture Recommendations

- Use **RAGAS** metrics (faithfulness, context precision, context recall) as the RAG-specific eval backbone.
- Implement **LLM-as-Judge** with a calibrated frontier model for open-ended quality assessment.
- Build **deterministic validators** for citation URL checking, JSON schema validation, and timing.
- Design for **CI/CD integration** from day one — eval should run on every test suite change.
- Include **production sampling hooks** for eventual live monitoring.

---

## 8. Sources

### Accuracy & Hallucination Research
- Columbia Journalism Review — AI search citation reliability study (~37% citation hallucination rate for Perplexity)
- Reddit r/perplexity_ai — User-reported hallucination examples and discussions
- Neil Patel analysis — Perplexity accuracy assessment
- India Times — AI search engine accuracy comparison
- Suprmind.ai — Reasoning model trade-off analysis

### User Complaints & Product Sentiment
- Reddit r/perplexity_ai — Subscription complaints, "enshittification" discussions, migration threads
- Reddit r/ArtificialIntelligence — Comparative AI tool discussions

### Competitive Benchmarks
- Fabric.so — Multi-engine AI search comparison
- Lumichats.com — Perplexity vs ChatGPT vs Google accuracy analysis (~5% Perplexity hallucination rate, ~7-12% ChatGPT)
- PingPrime.ai — Source preference and bias analysis across AI search engines
- Sigma Browser — AI search engine feature comparison
- Zapier — Practical AI search tool comparison

### Product Features & Updates
- Perplexity.ai (official) — Product documentation, pricing, feature announcements
- SecondTalent.com — Comprehensive 2026 product update roundup
- ReleaseBot.io — Feature tracking and changelog analysis
- Nocode.mba — Pricing tier analysis
- Krater.ai — Feature and pricing breakdown

### Eval Methodology
- Galtea.ai — LLM evaluation best practices guide (golden datasets, judge calibration, production monitoring)
- FutureAGI — Multi-layered metric strategy framework
- DeepEval — Open-source eval metrics documentation
- Mastra.ai — Agent evaluation methodology
- LaunchDarkly — Feature-flagged AI evaluation patterns

---

> **Next Step:** Use this research to design the eval harness schema, test case specifications, and metric definitions in `02-Design/`.

