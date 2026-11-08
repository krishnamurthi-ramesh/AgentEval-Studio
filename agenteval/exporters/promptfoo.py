"""
Promptfoo exporter for AgentEval Studio.
Converts any EvalPack into a valid, production-ready promptfooconfig.yaml file.
"""

from typing import Dict, Any
import yaml
from agenteval.models import EvalPack


def export_to_promptfoo_yaml(pack: EvalPack, model_providers: list = None) -> str:
    """
    Convert an EvalPack to Promptfoo YAML configuration string.
    """
    model_providers = model_providers or [
        "openai:gpt-4o-mini",
        "anthropic:messages:claude-3-5-haiku-20241022"
    ]

    tests = []
    for c in pack.cases:
        assertions = []

        if not c.expected_trajectory and c.forbidden_tools:
            # Adversarial refusal assertion
            for forbidden in c.forbidden_tools:
                assertions.append({
                    "type": "not-contains",
                    "value": forbidden,
                    "description": f"Must not invoke forbidden tool: {forbidden}"
                })
        elif c.expected_trajectory:
            for exp in c.expected_trajectory:
                assertions.append({
                    "type": "contains",
                    "value": exp.tool_name,
                    "description": f"Must invoke expected tool: {exp.tool_name}"
                })
                for arg_key, arg_val in exp.arguments.items():
                    assertions.append({
                        "type": "contains",
                        "value": str(arg_val),
                        "description": f"Must include argument value {arg_key}={arg_val}"
                    })

        test_item = {
            "description": f"[{c.category}] {c.id}",
            "vars": {
                "user_input": c.user_input
            },
            "assert": assertions
        }
        tests.append(test_item)

    config = {
        "description": f"{pack.name} (v{pack.version}) — Exported by AgentEval Studio",
        "prompts": [
            "You are an AI assistant. Answer user prompt using tools if necessary: {{user_input}}"
        ],
        "providers": model_providers,
        "tests": tests
    }

    return yaml.dump(config, sort_keys=False, default_flow_style=False)
