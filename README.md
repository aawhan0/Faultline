# Faultline

Faultline is an MCP-native AI incident response system designed to investigate production incidents, gather evidence from operational systems, identify probable root causes, recommend remediation, and verify recovery.

## Overview

Modern production incidents often require engineers to correlate signals across logs, metrics, deployments, source code, and operational documentation. Faultline explores how an AI agent can perform that investigation through standardized MCP tools while remaining observable, testable, and safe to operate.

The project is designed as a local-first system that can run without paid AI APIs or cloud infrastructure, while keeping a clear path toward scalable deployment.

## Core Goals

- Investigate production-like incidents using an autonomous AI agent.
- Use Model Context Protocol (MCP) to expose operational capabilities as structured tools.
- Gather and correlate evidence from logs, metrics, source changes, deployments, and runbooks.
- Produce evidence-backed root-cause hypotheses rather than unsupported answers.
- Support controlled remediation with validation and human approval for destructive actions.
- Measure agent quality through automated evaluations and regression tests.
- Provide observability into agent decisions, tool usage, latency, failures, and outcomes.
- Maintain a zero-cost local development and evaluation path with replaceable infrastructure components.

## Planned Capabilities

### Incident Investigation

- Incident ingestion and normalization
- Evidence collection across operational sources
- Root-cause hypothesis generation
- Evidence-based diagnosis
- Recovery verification

### MCP Tooling

- Metrics inspection
- Log search and analysis
- Git history and deployment inspection
- Runbook retrieval
- Incident state management
- Controlled remediation actions

### AI Evaluation

Faultline will include a dedicated evaluation framework for measuring:

- Root-cause accuracy
- Evidence correctness
- Tool-selection quality
- Tool-use efficiency
- Diagnosis completeness
- Remediation accuracy
- Agent trajectory quality

Evaluation results will be used for regression testing across prompts, models, retrieval strategies, and agent changes.

### Reliability and Safety

- Structured tool inputs and outputs
- Timeouts and retries
- Failure handling and fallbacks
- Authentication and authorization
- Audit logging
- Human-in-the-loop approval for high-risk actions
- Rate limiting and controlled execution

## Architecture Direction

```text
Incident
   |
   v
AI Agent
   |
   v
MCP Tool Layer
   |
   +----------------+----------------+----------------+
   |                |                |
   v                v                v
Metrics           Logs           Git / Deployments
   |                |                |
   +----------------+----------------+
                    |
                    v
             Evidence Engine
                    |
                    v
              Root Cause
                    |
                    v
            Remediation Plan
                    |
             Human Approval
                    |
                    v
            Recovery Verification
                    |
                    v
                  Evals
```

## Local-First Design

The initial implementation is intended to run locally using open-source components such as:

- Python
- MCP SDK
- Ollama and a locally hosted open model
- FastAPI
- SQLite or PostgreSQL
- Prometheus
- Loki
- Docker

The system will keep model, storage, and infrastructure components replaceable so the same architecture can later support hosted models, distributed workers, managed databases, and cloud observability platforms.

## Project Status

Faultline is in the initial architecture and implementation stage. The first milestone is a complete vertical slice: a reproducible production-like incident, MCP-based evidence gathering, agent diagnosis, and an automated evaluation of the result.

## License

License to be added.