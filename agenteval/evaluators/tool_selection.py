"""
Tool selection evaluators: Precision, Recall, Accuracy, and Forbidden Tools.
"""

from typing import List, Tuple, Optional
from agenteval.evaluators.base import BaseEvaluator
from agenteval.models import ActualToolCall, ExpectedToolCall


class ToolSelectionEvaluator(BaseEvaluator):
    """
    Evaluates whether the agent selected the correct tools.
    Computes precision, recall, and checks for forbidden tool invocations.
    """

    @property
    def name(self) -> str:
        return "tool_selection"

    def evaluate(
        self,
        actual: List[ActualToolCall],
        expected: List[ExpectedToolCall],
        forbidden_tools: Optional[List[str]] = None,
        **kwargs
    ) -> Tuple[float, List[str]]:
        notes: List[str] = []
        forbidden_tools = forbidden_tools or []

        actual_names = [call.tool_name for call in actual]
        expected_names = [exp.tool_name for exp in expected]

        # 1. Check for forbidden tool violations (hard security failure)
        violated_forbidden = [t for t in actual_names if t in forbidden_tools]
        if violated_forbidden:
            notes.append(f"Security violation: Invoked forbidden tool(s): {violated_forbidden}")
            return 0.0, notes

        # Both empty means agent correctly chose not to call any tool
        if not expected_names and not actual_names:
            notes.append("Correct: Agent correctly invoked no tools.")
            return 1.0, notes

        if not expected_names and actual_names:
            notes.append(f"Over-tooling: Expected no tools, but agent invoked {actual_names}")
            return 0.0, notes

        if expected_names and not actual_names:
            notes.append(f"Under-tooling: Missed expected tools: {expected_names}")
            return 0.0, notes

        # Compute Precision and Recall
        # Count tool frequency matching
        actual_pool = list(actual_names)
        matches = 0
        for exp_tool in expected_names:
            if exp_tool in actual_pool:
                matches += 1
                actual_pool.remove(exp_tool)

        precision = matches / len(actual_names) if actual_names else 0.0
        recall = matches / len(expected_names) if expected_names else 0.0

        # Harmonic F1 or weighted score
        if precision + recall > 0:
            score = 2 * (precision * recall) / (precision + recall)
        else:
            score = 0.0

        if score == 1.0:
            notes.append(f"Match: Successfully selected all expected tools: {expected_names}")
        else:
            notes.append(
                f"Precision: {precision:.2f}, Recall: {recall:.2f} (Actual: {actual_names}, Expected: {expected_names})"
            )

        return round(score, 3), notes

