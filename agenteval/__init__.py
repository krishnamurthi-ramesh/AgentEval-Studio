"""
AgentEval Studio — The Collaborative Evaluation Workspace for AI Builders.
"ChatPRD for AI Evals"
"""

from agenteval.models import (
    EvalPack,
    EvalCase,
    ExpectedToolCall,
    ActualToolCall,
    AgentRunResult,
    RowScorecard,
    VariantScorecard,
    ReleaseGatePolicy,
    ReleaseDecisionBrief,
)
from agenteval.library import list_packs, load_pack, save_pack
from agenteval.runner import EvalRunner
from agenteval.gates import PolicyGateEngine
from agenteval.copilot import EvalCopilot

__version__ = "0.1.0"

__all__ = [
    "EvalPack",
    "EvalCase",
    "ExpectedToolCall",
    "ActualToolCall",
    "AgentRunResult",
    "RowScorecard",
    "VariantScorecard",
    "ReleaseGatePolicy",
    "ReleaseDecisionBrief",
    "list_packs",
    "load_pack",
    "save_pack",
    "EvalRunner",
    "PolicyGateEngine",
    "EvalCopilot",
]

