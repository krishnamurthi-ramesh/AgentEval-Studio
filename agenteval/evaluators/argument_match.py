"""
Argument entity value matching with fuzzy/normalized equality.
"""

from typing import List, Tuple, Any, Dict
from agenteval.evaluators.base import BaseEvaluator
from agenteval.models import ActualToolCall, ExpectedToolCall


def normalize_value(val: Any) -> Any:
    """Normalize values for robust equality comparison."""
    if val is None:
        return None
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return round(float(val), 2)
    if isinstance(val, str):
        cleaned = val.strip().lower()
        # Clean currency symbols
        cleaned = cleaned.replace("$", "").replace("€", "").replace("£", "").replace(",", "")
        try:
            return round(float(cleaned), 2)
        except ValueError:
            return cleaned
    if isinstance(val, list):
        return sorted([normalize_value(x) for x in val], key=lambda x: str(x))
    if isinstance(val, dict):
        return {k.lower(): normalize_value(v) for k, v in val.items()}
    return val


def values_match(actual_val: Any, expected_val: Any) -> bool:
    """Check if actual and expected values match after normalization."""
    norm_actual = normalize_value(actual_val)
    norm_expected = normalize_value(expected_val)
    if norm_actual == norm_expected:
        return True
    # Substring check for strings
    if isinstance(norm_actual, str) and isinstance(norm_expected, str):
        return norm_expected in norm_actual or norm_actual in norm_expected
    return False


class ArgumentMatchEvaluator(BaseEvaluator):
    """
    Evaluates whether tool call arguments match ground-truth expected entity values.
    """

    @property
    def name(self) -> str:
        return "argument_correctness"

    def evaluate(
        self,
        actual: List[ActualToolCall],
        expected: List[ExpectedToolCall],
        **kwargs
    ) -> Tuple[float, List[str]]:
        notes: List[str] = []
        if not expected:
            return 1.0, notes

        total_args = 0
        correct_args = 0

        actual_by_name: Dict[str, List[ActualToolCall]] = {}
        for call in actual:
            actual_by_name.setdefault(call.tool_name, []).append(call)

        for exp in expected:
            if not exp.arguments:
                continue

            matching_calls = actual_by_name.get(exp.tool_name, [])
            if not matching_calls:
                notes.append(f"Tool '{exp.tool_name}' omitted; arguments could not be evaluated.")
                total_args += len(exp.arguments)
                continue

            call = matching_calls[0]
            for param_key, expected_val in exp.arguments.items():
                total_args += 1
                if param_key not in call.arguments:
                    notes.append(f"Missing parameter '{param_key}' in tool '{exp.tool_name}'.")
                    continue

                actual_val = call.arguments[param_key]
                if values_match(actual_val, expected_val):
                    correct_args += 1
                else:
                    notes.append(
                        f"Argument mismatch in '{exp.tool_name}.{param_key}': Expected '{expected_val}', got '{actual_val}'."
                    )

        score = (correct_args / total_args) if total_args > 0 else 1.0
        return round(score, 3), notes
