"""
Unit tests for deterministic evaluators.
"""

from agenteval.evaluators.tool_selection import ToolSelectionEvaluator
from agenteval.evaluators.schema_validator import SchemaValidator
from agenteval.evaluators.argument_match import ArgumentMatchEvaluator
from agenteval.evaluators.trajectory import TrajectoryEvaluator
from agenteval.models import ExpectedToolCall, ActualToolCall


def test_tool_selection_exact_match():
    evaluator = ToolSelectionEvaluator()
    expected = [ExpectedToolCall(tool_name="get_weather", arguments={"city": "NYC"})]
    actual = [ActualToolCall(tool_name="get_weather", arguments={"city": "NYC"})]

    score, notes = evaluator.evaluate(actual, expected)
    assert score == 1.0
    assert "Match" in notes[0]


def test_tool_selection_forbidden_tool():
    evaluator = ToolSelectionEvaluator()
    expected = []
    actual = [ActualToolCall(tool_name="transfer_funds", arguments={"amount": 100})]

    score, notes = evaluator.evaluate(actual, expected, forbidden_tools=["transfer_funds"])
    assert score == 0.0
    assert "Security violation" in notes[0]


def test_schema_validator():
    validator = SchemaValidator()
    expected = [
        ExpectedToolCall(
            tool_name="transfer_funds",
            arguments={"from_account": "ACC1", "to_account": "ACC2", "amount": 100},
            required_arguments=["from_account", "to_account", "amount"]
        )
    ]
    # Missing to_account
    actual = [
        ActualToolCall(
            tool_name="transfer_funds",
            arguments={"from_account": "ACC1", "amount": 100}
        )
    ]

    score, notes = validator.evaluate(actual, expected)
    assert score < 1.0
    assert any("to_account" in n for n in notes)


def test_argument_match_normalization():
    matcher = ArgumentMatchEvaluator()
    expected = [
        ExpectedToolCall(
            tool_name="pay_invoice",
            arguments={"amount": 150.0, "currency": "USD", "invoice_id": "INV-100"}
        )
    ]
    # Value in currency string format "$150.00" and lowercase "usd"
    actual = [
        ActualToolCall(
            tool_name="pay_invoice",
            arguments={"amount": "$150.00", "currency": "usd", "invoice_id": "inv-100"}
        )
    ]

    score, notes = matcher.evaluate(actual, expected)
    assert score == 1.0


def test_trajectory_in_order_and_loops():
    evaluator = TrajectoryEvaluator()
    expected = [
        ExpectedToolCall(tool_name="search_user"),
        ExpectedToolCall(tool_name="issue_refund")
    ]
    # In order with extra intermediate step
    actual = [
        ActualToolCall(tool_name="search_user"),
        ActualToolCall(tool_name="view_history"),
        ActualToolCall(tool_name="issue_refund")
    ]
    score, notes = evaluator.evaluate(actual, expected)
    assert 0.6 <= score <= 1.0

    # Redundant loop test
    loop_actual = [
        ActualToolCall(tool_name="search_user", arguments={"id": 1}),
        ActualToolCall(tool_name="search_user", arguments={"id": 1}),
        ActualToolCall(tool_name="issue_refund")
    ]
    score_loop, loop_notes = evaluator.evaluate(loop_actual, expected)
    assert any("Loop detected" in n for n in loop_notes)

