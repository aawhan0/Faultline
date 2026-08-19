# Faultline

**MCP-native AI incident response for production-like systems.**

Faultline is a local-first incident investigation system that combines **Model Context Protocol (MCP)** tools, deterministic evidence retrieval, and replaceable LLM providers to investigate production incidents and produce evidence-grounded diagnoses.

The project is being built as an engineering-focused AI system: every important boundary is typed, testable, replaceable, and evaluated.

---

## What Faultline Does

Given an incident, Faultline can:

1. Retrieve the incident and operational evidence through MCP-compatible tools.
2. Give that evidence to an investigation agent.
3. Ask a local LLM to reason over the collected evidence.
4. Parse and validate the model's structured diagnosis.
5. Reject diagnoses that reference evidence that was never retrieved.
6. Produce a structured `Diagnosis` containing:
   - root cause
   - supporting evidence IDs
   - confidence
   - recommended action
7. Evaluate the diagnosis against a canonical incident scenario.

The current implementation runs entirely locally using **Ollama + Qwen2.5 3B**, so no paid model API is required.

---

## Current Architecture

```text
                         ┌──────────────────────┐
                         │       Incident       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Agent Runtime     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      LLMAgent        │
                         └──────────┬───────────┘
                                    │
                       ┌────────────┴────────────┐
                       │                         │
                       ▼                         ▼
              ┌─────────────────┐       ┌─────────────────┐
              │ EvidenceProvider│       │  LLMProvider    │
              │      (MCP)      │       │                 │
              └────────┬────────┘       └────────┬────────┘
                       │                         │
                       ▼                         ▼
              ┌─────────────────┐       ┌─────────────────┐
              │ Simulator / MCP │       │ OllamaProvider  │
              │ Evidence Tools  │       │  Qwen2.5 3B     │
              └─────────────────┘       └────────┬────────┘
                                                 │
                                                 ▼
                                      Structured LLM Response
                                                 │
                                                 ▼
                                      Parse + Normalize + Validate
                                                 │
                                                 ▼
                                           ┌───────────┐
                                           │ Diagnosis │
                                           └─────┬─────┘
                                                 │
                                                 ▼
                                          LLM Evaluation
```

### Design Principles

- **MCP-native:** operational capabilities are exposed behind structured tool boundaries.
- **Provider-agnostic:** the agent does not depend directly on Ollama or a specific model.
- **Evidence-grounded:** the agent rejects unknown evidence IDs returned by the model.
- **Structured outputs:** model responses are normalized and validated into Pydantic models.
- **Local-first:** the development path works without paid cloud AI services.
- **Test-driven:** unit, integration, protocol, and model-backed evaluation tests protect the architecture.
- **Replaceable infrastructure:** model providers and evidence providers can be swapped without rewriting the agent.

---

## MCP Layer

Faultline uses the Model Context Protocol to expose incident investigation capabilities.

The current MCP server exposes:

- `get_incident`
- `search_evidence`

The MCP integration is tested through an in-memory MCP client/server session, so protocol behavior is tested independently of the HTTP deployment environment.

The evidence boundary is represented by:

```python
class EvidenceProvider(Protocol):
    def get_incident(self, incident_id: str) -> Incident: ...

    def search_evidence(
        self,
        incident_id: str,
        query: str,
    ) -> list[Evidence]: ...
```

This allows the current simulator-backed provider to eventually be replaced with real production integrations.

---

## LLM Layer

The reasoning layer is deliberately separated from the model implementation.

```text
LLMAgent
   │
   └── LLMProvider
          │
          ├── OllamaProvider      ← current
          ├── future hosted model
          └── future alternative model
```

The current local implementation uses:

- **Ollama**
- **Qwen2.5 3B**
- HTTP API at `http://localhost:11434`

The LLM adapter is responsible only for communicating with the model. The agent remains responsible for investigation logic, evidence grounding, and diagnosis validation.

### LLM Output Validation

Faultline does not blindly trust model output.

The LLM response passes through:

```text
Raw model output
      ↓
Markdown/code-fence cleanup
      ↓
JSON parsing
      ↓
Required-field validation
      ↓
Confidence normalization
      ↓
Evidence grounding
      ↓
Pydantic Diagnosis validation
```

Common model variations such as:

```json
{"confidence": 95}
```

or:

```json
{"confidence": "High"}
```

are normalized into the internal `0.0–1.0` confidence contract.

Evidence IDs that were not actually retrieved are rejected rather than silently accepted.

---

## Canonical Incident

Faultline currently uses a reproducible database-pool exhaustion scenario as its canonical incident.

The simulated incident contains signals including:

- HTTP 500 errors rising sharply after deployment.
- Database connection-pool timeouts.
- Connections pinned at the configured pool limit.
- Deployment `8f31c2` changing `max_overflow` from `20` to `0`.

The expected causal chain is:

```text
Deployment change
      ↓
max_overflow: 20 → 0
      ↓
Database connection-pool exhaustion
      ↓
Requests wait for connections
      ↓
HTTP 500 rate increases
```

This scenario provides a deterministic foundation for testing whether an LLM can identify the correct cause and supporting evidence.

---

## Evaluation

Faultline currently has automated model-backed evaluation against the canonical scenario.

The evaluation checks that the LLM:

- identifies the correct incident;
- produces a meaningful database/pool-related root cause;
- cites real evidence IDs;
- identifies `EV-003`, the deployment configuration change;
- returns a valid confidence score;
- provides a remediation action.

This is intentionally stronger than testing whether an LLM merely returns valid JSON.

The long-term evaluation framework will measure:

- root-cause accuracy;
- evidence correctness;
- evidence coverage;
- tool-selection quality;
- tool-use efficiency;
- diagnosis completeness;
- remediation accuracy;
- agent trajectory quality;
- regression across prompts and models.

---

## Development Status

### Completed

- [x] Core incident/evidence/diagnosis models
- [x] Deterministic incident simulator
- [x] MCP server
- [x] MCP protocol integration tests
- [x] Evidence provider abstraction
- [x] Agent runtime abstraction
- [x] Replaceable `LLMProvider` boundary
- [x] Local Ollama provider
- [x] Qwen2.5 3B local inference
- [x] Structured LLM response parsing
- [x] Confidence normalization
- [x] Evidence-grounding validation
- [x] Real Ollama integration test
- [x] Canonical LLM evaluation
- [x] 30 automated tests passing at the current milestone

### Next

- [ ] Dedicated multi-run LLM evaluation harness
- [ ] Quantitative evaluation metrics and regression thresholds
- [ ] More incident scenarios
- [ ] Better evidence retrieval and ranking
- [ ] Additional operational MCP tools
- [ ] Agent tool-selection / investigation loop
- [ ] Recovery verification
- [ ] Controlled remediation with human approval
- [ ] Observability and agent trajectory tracing
- [ ] Production infrastructure integrations

---

## Local Development

### Requirements

- Python 3.11+
- Git
- Ollama
- A locally available model such as `qwen2.5:3b`

### Setup

Create and activate a virtual environment:

```powershell
python -m venv faultline-venv
.\faultline-venv\Scripts\Activate.ps1
```

Install the project and development dependencies according to the repository configuration.

Start Ollama and make sure the model is available:

```powershell
ollama pull qwen2.5:3b
ollama run qwen2.5:3b "Say hello in one sentence."
```

Verify the model is loaded:

```powershell
ollama ps
```

### Run Tests

Run the complete test suite:

```powershell
pytest -q
```

Run MCP integration tests:

```powershell
pytest -q tests\integration\test_mcp_server.py
```

Run the real Ollama integration test:

```powershell
pytest -q tests\integration\test_ollama_agent.py
```

Run the canonical LLM evaluation:

```powershell
pytest -q tests\integration\test_llm_evaluation.py
```

Run Ruff:

```powershell
ruff check src tests
```

> Keep feature-specific Ruff checks clean before committing. Repository-wide lint findings unrelated to the current feature should be handled separately rather than mixed into feature commits.

---

## Project Structure

```text
Faultline/
├── src/
│   └── faultline/
│       ├── agent/
│       │   ├── diagnosis.py
│       │   ├── llm.py
│       │   ├── llm_agent.py
│       │   ├── ollama.py
│       │   └── runtime.py
│       ├── core/
│       │   └── models.py
│       ├── evals/
│       │   └── baseline.py
│       ├── mcp/
│       │   ├── client.py
│       │   ├── server.py
│       │   └── simulator_provider.py
│       └── simulator/
│           └── scenarios.py
│
├── tests/
│   ├── integration/
│   │   ├── test_llm_evaluation.py
│   │   ├── test_mcp_server.py
│   │   ├── test_ollama_agent.py
│   │   └── test_vertical_slice.py
│   └── unit/
│       ├── test_agent_runtime.py
│       ├── test_llm.py
│       ├── test_llm_agent.py
│       ├── test_llm_runtime.py
│       └── test_ollama.py
│
├── pyproject.toml
└── README.md
```

---

## Roadmap

Faultline is intentionally being developed as a sequence of increasingly realistic vertical slices:

```text
1. Deterministic incident simulation
          ↓
2. MCP evidence access
          ↓
3. Deterministic diagnosis
          ↓
4. Replaceable LLM agent
          ↓
5. Local Ollama inference
          ↓
6. Model-backed evaluation          ← current stage
          ↓
7. Multi-run evaluation harness
          ↓
8. Richer MCP tools + retrieval
          ↓
9. Autonomous investigation loop
          ↓
10. Recovery verification
          ↓
11. Controlled remediation
          ↓
12. Production integrations
```

The guiding principle is simple: **build the safety and evaluation boundaries before giving the agent more power.**

---

## License

License to be added.
