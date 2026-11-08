"""
Unit tests for the Release Policy Gate Engine.
"""

from agenteval.models import VariantScorecard, RowScorecard, ReleaseGatePolicy
from agenteval.gates import PolicyGateEngine


def test_policy_gate_blocks_high_risk_failures():
    engine = PolicyGateEngine(ReleaseGatePolicy())

    card = VariantScorecard(
        variant_name="candidate_v2",
        total_cases=10,
        passed_cases=8,
        pass_rate=0.8,
        avg_tool_accuracy=0.92,
        avg_argument_score=0.90,
        avg_trajectory_score=0.90,
        p50_latency_ms=120,
        p90_latency_ms=200,
        total_cost_usd=0.015,
        high_risk_failures=1, # 1 high risk error!
        rows=[]
    )

    brief = engine.evaluate_release(card)
    assert brief.status == "BLOCKED"
    assert len(brief.hard_blockers) == 1
    assert "High-risk tool failure" in brief.hard_blockers[0]


def test_policy_gate_ready_to_ship():
    engine = PolicyGateEngine(ReleaseGatePolicy(min_pass_rate=0.85, min_tool_accuracy=0.90))

    candidate = VariantScorecard(
        variant_name="candidate_v3",
        total_cases=10,
        passed_cases=10,
        pass_rate=1.0,
        avg_tool_accuracy=1.0,
        avg_argument_score=0.95,
        avg_trajectory_score=1.0,
        p50_latency_ms=105,
        p90_latency_ms=150,
        total_cost_usd=0.012,
        high_risk_failures=0,
        rows=[]
    )

    baseline = VariantScorecard(
        variant_name="baseline_v1",
        total_cases=10,
        passed_cases=7,
        pass_rate=0.7,
        avg_tool_accuracy=0.85,
        avg_argument_score=0.80,
        avg_trajectory_score=0.85,
        p50_latency_ms=100,
        p90_latency_ms=140,
        total_cost_usd=0.010,
        high_risk_failures=0,
        rows=[]
    )

    brief = engine.evaluate_release(candidate, baseline)
    assert brief.status == "READY_TO_SHIP"
    assert brief.failed_gates == 0
    assert "READY TO SHIP" in brief.markdown_content
