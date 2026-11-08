"""
Trajectory evaluation: Sequence match, In-order subsequence, and Redundant Loop detection.
"""

from typing import List, Tuple
from agenteval.evaluators.base import BaseEvaluator
from agenteval.models import ActualToolCall, ExpectedToolCall


def is_subsequence(sub: List[str], full: List[str]) -> bool:
    """Check if sub is an ordered subsequence of full."""
    it = iter(full)
    return all(item in it for item in sub)


def detect_redundant_loops(calls: List[ActualToolCall]) -> List[str]:
    """Detect if the agent repeated the exact same tool call consecutively."""
    loop_warnings = []
    for i in range(len(calls) - 1):
        c1, c2 = calls[i], calls[i + 1]
        if c1.tool_name == c2.tool_name and c1.arguments == c2.arguments:
            loop_warnings.append(
                f"Loop detected: Consecutive duplicate call to '{c1.tool_name}' with identical arguments."
            )
    return loop_warnings


class TrajectoryEvaluator(BaseEvaluator):
    """
    Evaluates multi-step agent trajectories:
    - Checks in-order execution of prerequisite tools.
    - Penalizes redundant loops and circular retries.
    """

    @property
    def name(self) -> str:
        return "trajectory_flow"

    def evaluate(
        self,
        actual: List[ActualToolCall],
        expected: List[ExpectedToolCall],
        **kwargs
    ) -> Tuple[float, List[str]]:
        notes: List[str] = []

        actual_seq = [call.tool_name for call in actual]
        expected_seq = [exp.tool_name for exp in expected]

        # Check for redundant loops
        loop_warnings = detect_redundant_loops(actual)
        notes.extend(loop_warnings)

        if not expected_seq and not actual_seq:
            return 1.0, ["Optimal: Clean empty trajectory."]

        if not expected_seq and actual_seq:
            return 0.0, [f"Unnecessary trajectory: Agent executed steps {actual_seq}"]

        if expected_seq and not actual_seq:
            return 0.0, [f"Empty trajectory: Expected {expected_seq}, but agent executed nothing."]

        # Check Exact Match
        if actual_seq == expected_seq:
            score = 1.0
            notes.append(f"Exact trajectory match: {' -> '.join(actual_seq)}")
        # Check In-Order Subsequence Match
        elif is_subsequence(expected_seq, actual_seq):
            # Subsequence holds, but extra steps occurred
            overhead_steps = len(actual_seq) - len(expected_seq)
            penalty = min(0.15 * overhead_steps, 0.4)
            score = max(0.6, 1.0 - penalty)
            notes.append(
                f"In-order match with detour: Expected {' -> '.join(expected_seq)}, Actual {' -> '.join(actual_seq)}"
            )
        else:
            # Check overlap fraction
            matches = sum(1 for t in expected_seq if t in actual_seq)
            score = (matches / len(expected_seq)) * 0.5
            notes.append(
                f"Trajectory out of order: Expected {' -> '.join(expected_seq)}, got {' -> '.join(actual_seq)}"
            )

        # Apply loop penalty
        if loop_warnings:
            score = max(0.0, score - 0.25 * len(loop_warnings))

        return round(score, 3), notes

