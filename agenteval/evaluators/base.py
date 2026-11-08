"""
Base evaluator interface for AgentEval Studio.
"""

from abc import ABC, abstractmethod
from typing import Tuple, List, Any


class BaseEvaluator(ABC):
    """Abstract base class for all deterministic and model-based evaluators."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Evaluator identifier."""
        pass

    @abstractmethod
    def evaluate(self, actual: Any, expected: Any, **kwargs) -> Tuple[float, List[str]]:
        """
        Evaluate actual output against expected ground truth.
        Returns:
            Tuple of (score: float [0.0 to 1.0], diagnostic_notes: List[str])
        """
        pass

