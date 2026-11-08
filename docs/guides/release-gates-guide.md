# Release Policy Gates & CI/CD Integration

Release Policy Gates transform evaluation metrics into an auditable product deployment decision: **`READY TO SHIP`**, **`BLOCKED`**, or **`REQUIRES PM REVIEW`**.

---

## 1. How Policy Gates Work

The `PolicyGateEngine` evaluates candidate variants against explicit release rules:

```
                                [ Candidate Variant Results ]
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
       [ Gate 1: High-Risk Blocker ]                       [ Gate 2: Quality Gates ]
       Any regression on zero_tolerance_tools?             Tool Accuracy >= Threshold?
       YES ──► BLOCKED                                     Argument Score >= Threshold?
       NO                                                  NO ──► BLOCKED
        │                                                  YES
        └───────────────────────────┬───────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
       [ Gate 3: Latency Regression ]      [ Gate 4: Cost Regression ]
       Latency delta <= max_allowed?       Cost delta <= max_allowed?
       YES                                 YES
        │                                   │
        └───────────────────┬───────────────┘
                            ▼
              ┌───────────────────────────┐
              │  STATUS: READY TO SHIP    │
              │  Generate Decision Brief  │
              └───────────────────────────┘
```

---

## 2. Gate Definitions

| Gate | Default Rule | Type | Failure Outcome |
|---|---|---|---|
| **Zero-Tolerance Tools** | `errors == 0` on sensitive tools | Hard Blocker | **`BLOCKED`** |
| **Tool Selection Accuracy** | $\ge 90\%$ accuracy | Quality Gate | **`BLOCKED`** if failed with other gates |
| **Argument Correctness** | $\ge 85\%$ entity match | Quality Gate | **`BLOCKED`** |
| **Benchmark Pass Rate** | $\ge 85\%$ pass rate | Quality Gate | **`BLOCKED`** |
| **Latency Regression** | $\le +20\%$ vs baseline | Operational Gate | **`REQUIRES REVIEW`** |
| **Cost Regression** | $\le +25\%$ vs baseline | Operational Gate | **`REQUIRES REVIEW`** |

---

## 3. GitHub Actions CI/CD Integration

You can gate pull requests automatically by adding a gate check step to your workflow:

```yaml
name: Agent Release Gates

on:
  pull_request:
    branches: [ main ]

jobs:
  eval-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e .
      - name: Run Release Gate Check
        run: |
          agenteval gates --pack customer_support_banking --candidate v3 --baseline v1
```

If the status is `BLOCKED`, the CLI exits with code `1`, preventing PR merges on policy regressions!

