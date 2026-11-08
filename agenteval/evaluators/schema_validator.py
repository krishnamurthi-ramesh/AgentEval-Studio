"""
Schema and required argument validation for tool calls.
"""

from typing import List, Tuple, Dict, Any
from agenteval.evaluators.base import BaseEvaluator
from agenteval.models import ActualToolCall, ExpectedToolCall


class SchemaValidator(BaseEvaluator):
    """
    Validates that tool calls contain all required arguments and appropriate types.
    """

    @property
    def name(self) -> str:
        return "schema_validation"

    def evaluate(
        self,
        actual: List[ActualToolCall],
        expected: List[ExpectedToolCall],
        **kwargs
    ) -> Tuple[float, List[str]]:
        notes: List[str] = []
        if not expected:
            return 1.0, notes

        total_checks = 0
        passed_checks = 0

        # Match tool calls by name
        actual_by_name: Dict[str, List[ActualToolCall]] = {}
        for call in actual:
            actual_by_name.setdefault(call.tool_name, []).append(call)

        for exp in expected:
            req_args = exp.required_arguments or list(exp.arguments.keys())
            total_checks += len(req_args)

            matching_calls = actual_by_name.get(exp.tool_name, [])
            if not matching_calls:
                notes.append(f"Missing call: Expected '{exp.tool_name}' was not called.")
                continue

            # Check arguments of the first matching call
            call = matching_calls[0]
            for arg_name in req_args:
                if arg_name in call.arguments and call.arguments[arg_name] is not None:
                    passed_checks += 1
                else:
                    notes.append(
                        f"Missing argument: Tool '{exp.tool_name}' missing required argument '{arg_name}'."
                    )

        score = (passed_checks / total_checks) if total_checks > 0 else 1.0
        return round(score, 3), notes
