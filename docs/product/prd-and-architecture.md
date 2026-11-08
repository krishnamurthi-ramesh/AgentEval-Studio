# Product Requirements Document (PRD) & Technical Architecture

**Document Version:** 1.0.0  
**Phase:** 4 — PRD and Architecture  
**Product:** AgentEval Studio  
**Date:** November 2026

---

## 1. Product Overview & User Stories

AgentEval Studio is an open-source evaluation workbench and release gate engine designed specifically for tool-using AI agents.

### User Stories

#### Epic 1: Deterministic Agent Evaluation
- **US 1.1:** As an Applied AI Engineer, I want to evaluate an agent's tool call against a ground-truth expected tool so that I can compute tool selection precision, recall, and accuracy without paying for LLM judge calls.
- **US 1.2:** As an Applied AI Engineer, I want tool call arguments to be automatically validated against standard JSON schemas so that syntax errors and missing parameters are flagged deterministically.
- **US 1.3:** As an Applied AI Engineer, I want argument values to be compared against ground-truth entity values (with fuzzy normalization for dates, numbers, and casing) so that hallucinated values are instantly caught.
- **US 1.4:** As an Applied AI Engineer, I want multi-step agent trajectories to be scored using Exact Match, In-Order Subsequence Match, and Redundant Cycle Detection.

#### Epic 2: Multi-Variant Experiment Comparison
- **US 2.1:** As an AI Product Manager, I want to compare 2 or 3 agent variants (e.g., `baseline_v1`, `prompt_tuned_v2`, `model_swapped_v3`) evaluated over the exact same benchmark dataset in a side-by-side view.
- **US 2.2:** As an AI Product Manager, I want to see aggregate metrics for each variant: Tool Accuracy, Argument Conformance, Trajectory Success, p50/p90 Latency, and Cost per 1k runs.
- **US 2.3:** As an Applied AI Engineer, I want to inspect individual test rows and view why an evaluator failed, seeing the exact difference between expected parameters and generated parameters.

#### Epic 3: Release Policy Gate Engine & Decision Brief
- **US 3.1:** As an AI Product Manager, I want to configure Release Criteria Gates:
  - Minimum overall tool accuracy threshold (e.g., `>= 90%`).
  - Maximum permissible latency increase (e.g., `<= +20%`).
  - Maximum permissible cost increase (e.g., `<= +25%`).
  - Zero-tolerance high-risk tool blockers (e.g., no regressions allowed on `transfer_funds` or `delete_account`).
- **US 3.2:** As an AI Product Manager, I want the workbench to evaluate candidate variants against these gates and output a clear decision status: `READY TO SHIP`, `BLOCKED BY REGRESSION`, or `REQUIRES REVIEW`.
- **US 3.3:** As a cross-functional team, I want to export an evidence-backed **Release Decision Brief** (in Markdown) that details the pass/fail gates, metric trade-offs, and links directly to failing test cases for auditability.

---

## 2. Technical Architecture & System Design

```
┌────────────────────────────────────────────────────────────────────────┐
│                          User Interfaces                               │
│       ┌───────────────────────────┐    ┌───────────────────────────┐   │
│       │   Streamlit Local UI      │    │      CLI Test Runner      │   │
│       │  (Interactive Workbench)  │    │   (`agenteval evaluate`)  │   │
│       └─────────────┬─────────────┘    └─────────────┬─────────────┘   │
└─────────────────────┼────────────────────────────────┼─────────────────┘
                      ▼                                ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        AgentEval Studio Core                           │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    Evaluation Engine                             │  │
│  │  ┌────────────────────┐ ┌───────────────────┐ ┌────────────────┐ │  │
│  │  │ Tool Selection Eval│ │ Argument Validator│ │ Trajectory Eval│ │  │
│  │  └────────────────────┘ └───────────────────┘ └────────────────┘ │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
│                                     ▼                                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                     Release Policy Engine                        │  │
│  │  ┌────────────────────┐ ┌───────────────────┐ ┌────────────────┐ │  │
│  │  │ Threshold Checker  │ │ High-Risk Blocker │ │ Decision Brief │ │  │
│  │  └────────────────────┘ └───────────────────┘ └────────────────┘ │  │
│  └──────────────────────────────────┬───────────────────────────────┘  │
└─────────────────────────────────────┼──────────────────────────────────┘
                                      ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         Data & Storage Layer                           │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌────────────────┐  │
│  │ Benchmark Datasets  │  │ Experiment Results  │  │ Exported Briefs│  │
│  │ (JSONL / Schemas)   │  │ (Parquet / JSONL)   │  │ (Markdown)     │  │
│  └─────────────────────┘  └─────────────────────┘  └────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Schema & Core Primitives

### 1. Benchmark Example Schema (`BenchmarkItem`)
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ExpectedToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    is_high_risk: bool = False

class BenchmarkItem(BaseModel):
    id: str
    category: str # e.g. "account_management", "payments", "inquiries"
    user_input: str
    expected_trajectory: List[ExpectedToolCall]
    expected_final_intent: Optional[str] = None
    tags: List[str] = []
```

### 2. Actual Agent Execution Trace (`AgentExecutionResult`)
```python
class ActualToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    execution_success: bool = True
    output: Optional[Any] = None

class AgentExecutionResult(BaseModel):
    item_id: str
    variant_name: str # e.g. "router_prompt_v1", "router_prompt_v2"
    actual_trajectory: List[ActualToolCall]
    final_response: str
    latency_ms: float
    prompt_tokens: int
    completion_tokens: int
    total_cost_usd: float
    error: Optional[str] = None
```

### 3. Evaluation Result Schema (`EvaluationScorecard`)
```python
class RowEvaluationResult(BaseModel):
    item_id: str
    variant_name: str
    # Metric scores between 0.0 and 1.0
    tool_selection_score: float # Precision / Exact tool match
    argument_correctness_score: float # JSON schema + entity equality
    trajectory_score: float # In-order sequence match
    passed_all: bool
    is_high_risk_failure: bool
    diagnostic_notes: List[str] # Detailed explanation of discrepancies
```

### 4. Release Gate Configuration (`ReleaseGatePolicy`)
```python
class ReleaseGatePolicy(BaseModel):
    min_tool_accuracy: float = 0.90 # 90% minimum tool selection
    min_argument_correctness: float = 0.90 # 90% schema and value conformance
    min_trajectory_score: float = 0.85 # 85% sequence flow
    max_latency_regression_pct: float = 20.0 # Max +20% latency increase vs baseline
    max_cost_regression_pct: float = 25.0 # Max +25% cost increase vs baseline
    zero_tolerance_tools: List[str] = ["transfer_funds", "cancel_subscription", "delete_account"]
```

---

## 4. Evaluator Mathematical Formulations

### 1. Tool Selection Accuracy & Recall
For a given test item with expected tools $E = [t_1, t_2, ...]$ and actual tools $A = [a_1, a_2, ...]$:
$$\text{Tool Precision} = \frac{|A \cap E|}{|A|} \quad (\text{penalizes redundant/unneeded tool calls})$$
$$\text{Tool Recall} = \frac{|A \cap E|}{|E|} \quad (\text{penalizes omitted necessary tool calls})$$
$$\text{Single-Turn Tool Accuracy} = \mathbb{I}(a_1 == t_1)$$

### 2. Argument Conformance & Entity Correctness
For an invoked tool with expected arguments $Args_E$ and actual arguments $Args_A$:
1. **Schema Check:** $Args_A$ is validated against the tool's JSON Schema (types, required fields). Score is 0 if schema fails.
2. **Entity Value Accuracy:** For every key $k \in Args_E$:
   $$\text{Arg Score} = \frac{\sum_{k \in Args_E} \text{Match}(Args_A.get(k), Args_E[k])}{|Args_E|}$$
   Where $\text{Match}(v_a, v_e)$ applies fuzzy normalization (e.g., float precision, case-insensitive string matching, date parsing).

### 3. Trajectory Sequence Matching (In-Order Subsequence)
Let $S_E$ be the ordered sequence of tool names in the ground-truth trajectory, and $S_A$ be the actual sequence:
- **Exact Match:** $S_A == S_E$ (Binary 1 or 0).
- **In-Order Match:** Returns 1 if $S_E$ is a subsequence of $S_A$, 0 otherwise.
- **Redundant Loop Penalty:** If any tool is invoked consecutively with identical arguments $> 1$ times without progress, apply a penalty.

---

## 5. Release Gate Logic & Decision Brief Engine

The Release Policy Engine evaluates candidate variant $V_{cand}$ against baseline variant $V_{base}$:

```
                                [ Candidate Variant Results ]
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
       [ Gate 1: High-Risk Blocker ]                       [ Gate 2: Quality Gates ]
       Any regression on zero_tolerance_tools?             Tool Accuracy >= Threshold?
       YES ──► BLOCKED                                     Argument Score >= Threshold?
       NO                                                  NO ──► BLOCKED
        │                                                  YES
        └───────────────────────────┬───────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
       [ Gate 3: Latency Regression ]      [ Gate 4: Cost Regression ]
       Latency delta <= max_allowed?       Cost delta <= max_allowed?
       YES                                 YES
        │                                   │
        └───────────────────┬───────────────┘
                            ▼
              ┌───────────────────────────┐
              │  STATUS: READY TO SHIP    │
              │  Generate Decision Brief  │
              └───────────────────────────┘
```

If any hard blocker or critical quality gate fails, status is marked **`BLOCKED BY REGRESSION`**.  
If quality passes but latency or cost breaches the ceiling by $< 10\%$, status is marked **`REQUIRES PM EXCEPTION REVIEW`**.

