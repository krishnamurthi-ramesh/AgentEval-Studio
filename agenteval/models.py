"""
Data models and schemas for AgentEval Studio.
Defines EvalPack, EvalCase, ActualToolCall, Execution Results, and Release Gate configurations.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ExpectedToolCall(BaseModel):
    """Ground-truth expected tool invocation."""
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    is_high_risk: bool = False
    required_arguments: List[str] = Field(default_factory=list)


class RubricCriterion(BaseModel):
    """Qualitative or quantitative criterion for evaluating an agent response."""
    name: str
    description: str
    weight: float = 1.0
    pass_rule: Optional[str] = None


class EvalCase(BaseModel):
    """A single evaluation test case within an EvalPack."""
    id: str
    category: str = "general"
    user_input: str
    expected_trajectory: List[ExpectedToolCall] = Field(default_factory=list)
    expected_final_intent: Optional[str] = None
    expected_output_contains: Optional[List[str]] = None
    forbidden_tools: Optional[List[str]] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvalPack(BaseModel):
    """
    A self-contained, reusable evaluation pack.
    Can be discovered, shared, versioned, and forked across the community.
    """
    id: str
    name: str
    version: str = "1.0.0"
    author: str = "community"
    description: str
    category: str = "general"
    cases: List[EvalCase] = Field(default_factory=list)
    rubrics: List[RubricCriterion] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    recommended_gates: Optional[Dict[str, Any]] = None


class ActualToolCall(BaseModel):
    """Record of a tool call executed by an agent during evaluation."""
    tool_name: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    execution_success: bool = True
    output: Optional[Any] = None


class AgentRunResult(BaseModel):
    """Result of running an agent variant against a specific test case."""
    case_id: str
    variant_name: str
    actual_trajectory: List[ActualToolCall] = Field(default_factory=list)
    final_response: str = ""
    latency_ms: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost_usd: float = 0.0
    error: Optional[str] = None


class RowScorecard(BaseModel):
    """Detailed evaluation breakdown for a single test row."""
    case_id: str
    variant_name: str
    tool_selection_score: float = 1.0
    schema_score: float = 1.0
    argument_score: float = 1.0
    trajectory_score: float = 1.0
    passed: bool = True
    is_high_risk_failure: bool = False
    diagnostic_notes: List[str] = Field(default_factory=list)


class VariantScorecard(BaseModel):
    """Aggregated evaluation metrics for a specific agent variant."""
    variant_name: str
    total_cases: int
    passed_cases: int
    pass_rate: float
    avg_tool_accuracy: float
    avg_argument_score: float
    avg_trajectory_score: float
    p50_latency_ms: float
    p90_latency_ms: float
    total_cost_usd: float
    high_risk_failures: int
    rows: List[RowScorecard] = Field(default_factory=list)


class ReleaseGatePolicy(BaseModel):
    """Policy rules governing whether an agent variant is approved for release."""
    min_pass_rate: float = 0.85
    min_tool_accuracy: float = 0.90
    min_argument_score: float = 0.85
    min_trajectory_score: float = 0.80
    max_latency_regression_pct: float = 20.0  # Max % increase vs baseline
    max_cost_regression_pct: float = 25.0     # Max % increase vs baseline
    zero_tolerance_tools: List[str] = Field(default_factory=lambda: ["transfer_funds", "cancel_subscription", "delete_account"])


class GateResult(BaseModel):
    """Outcome of evaluating a single release gate."""
    gate_name: str
    passed: bool
    threshold: Any
    actual_value: Any
    is_hard_blocker: bool = False
    message: str = ""


class ReleaseDecisionBrief(BaseModel):
    """Executive decision brief synthesizing the release recommendation."""
    candidate_variant: str
    baseline_variant: Optional[str] = None
    status: str  # "READY_TO_SHIP" | "BLOCKED" | "REQUIRES_REVIEW"
    gates_evaluated: List[GateResult] = Field(default_factory=list)
    total_gates: int = 0
    passed_gates: int = 0
    failed_gates: int = 0
    hard_blockers: List[str] = Field(default_factory=list)
    trade_offs_summary: str = ""
    failing_cases_summary: List[Dict[str, Any]] = Field(default_factory=list)
    markdown_content: str = ""

