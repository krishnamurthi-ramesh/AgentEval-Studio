# Problem Hypotheses & Customer Discovery

## Background
Agentic AI systems introduce non-deterministic, multi-step behavior (tool invocations, argument synthesis, branching, recovery loops) that standard LLM evaluation frameworks (which focus primarily on single-turn prompt-response text similarity or RAG relevance) struggle to evaluate meaningfully.

## Primary Problem Hypotheses

### Hypothesis 1: The "Metric Soup" Release Paralysis
**Observation:** Modern evaluation tools present a collection of raw numbers: precision, recall, latency, cost, groundedness, schema match.
**Pain Point:** When variant `v2` improves overall task success by 3% but regresses on tool selection accuracy for high-risk tools and adds 400ms latency, engineering and product managers enter debate paralysis. There is no explicit framework or release gate mechanism to evaluate trade-offs against predefined release criteria.

### Hypothesis 2: Obscured Failure Trajectories in Tool Calling
**Observation:** Agents fail in subtle, multi-step ways: choosing the right tool with hallucinated arguments, calling tools in an inefficient loop, failing to parse tool output, or hallucinating the final answer despite correct tool execution.
**Pain Point:** Most platforms treat the final answer as the primary evaluation target. Diagnosing *where* in the tool-use trajectory the agent drifted requires hunting through multi-level span trees across hundreds of test rows.

### Hypothesis 3: Tool-Call Schema & Argument Evaluation Gap
**Observation:** Evaluators in existing platforms are heavily oriented around text-to-text comparison (BLEU, ROUGE, cosine similarity, or freeform LLM judge).
**Pain Point:** Tool-using agents require structured evaluation: Did the tool name match the required action? Did arguments validate against the JSON schema? Were entity values correctly extracted from context? Teams frequently write custom ad-hoc scripts because off-the-shelf evaluators don't treat tool calls as first-class evaluation entities.

### Hypothesis 4: Heavy Infrastructure Overhead for Quick Iteration
**Observation:** Existing enterprise observability platforms require configuring OpenTelemetry collectors, cloud accounts, multi-tenant databases, and background daemon services.
**Pain Point:** Developers iterating locally on a prompt or model change want a zero-configuration, local-first CLI/workbench that can run an evaluation benchmark in 10 seconds, produce a diff, and export a release brief without signing up for SaaS or deploying Docker clusters.
