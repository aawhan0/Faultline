# Faultline Architecture

## System Boundary

Faultline is organized around an incident-response agent that interacts with operational capabilities through MCP. The agent should not know the implementation details of logs, metrics, source control, or remediation systems. Those capabilities are exposed through explicit, validated tools.

```text
                           Incident
                              |
                              v
                       +--------------+
                       | Faultline API |
                       +------+-------+
                              |
                              v
                       +--------------+
                       | Agent Runtime |
                       +------+-------+
                              |
                              v
                       +--------------+
                       |   MCP Layer   |
                       +------+-------+
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
         Metrics            Logs       Git / Deployments
             |                |                |
             +----------------+----------------+
                              |
                              v
                       +--------------+
                       | Evidence     |
                       | Correlation  |
                       +------+-------+
                              |
                              v
                       Diagnosis / Plan
                              |
                       +------+-------+
                       | Safety Gate   |
                       +------+-------+
                              |
                    Human approval when needed
                              |
                              v
                         Remediation
                              |
                              v
                     Recovery verification
                              |
                              v
                           Evals
```

## Repository Boundaries

### `src/faultline/api`
Application-facing HTTP interface and request lifecycle orchestration. This layer should translate external requests into internal application commands without containing agent-specific reasoning.

### `src/faultline/agent`
Agent runtime, planning, tool selection, evidence gathering, hypothesis generation, diagnosis, and remediation planning.

### `src/faultline/mcp`
MCP server and tool definitions. Tools should expose narrow operational capabilities with typed inputs, typed outputs, validation, and explicit error behavior.

### `src/faultline/core`
Shared domain models and contracts: incidents, evidence, hypotheses, diagnoses, remediation plans, tool results, and execution metadata.

### `src/faultline/simulator`
Deterministic production-like incident scenarios and mock operational backends used for local development, demos, and evaluation datasets.

### `src/faultline/evals`
Offline and integration evaluations for agent quality, tool use, evidence grounding, and regression detection. Evals are treated as a product capability rather than a final-stage test suite.

### `tests`
Unit tests for isolated components, integration tests for cross-component behavior, and evaluation tests for end-to-end agent behavior.

## Initial Vertical Slice

The first implementation should prove one complete path before additional infrastructure is added:

1. Start a deterministic incident scenario.
2. Expose the scenario through MCP tools.
3. Let the agent inspect the available evidence.
4. Produce a structured diagnosis with supporting evidence.
5. Compare the result with the scenario ground truth.
6. Record evaluation metrics.

The first slice should not execute real destructive remediation. Remediation is introduced only after the investigation and evaluation path is stable.

## Design Principles

- MCP is a boundary between the agent and operational capabilities.
- Domain contracts are explicit and strongly typed.
- Incident scenarios are reproducible so agent behavior can be evaluated deterministically.
- Evals run independently of any single model provider.
- Model, storage, and infrastructure adapters remain replaceable.
- High-risk actions are separated from diagnosis and require an explicit safety gate.
- The local development path should remain usable without paid services.
