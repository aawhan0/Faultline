# Vertical Slice Status

## Current Milestone

The first deterministic Faultline investigation path is now represented end-to-end:

```text
Incident
  -> MCP evidence provider
  -> evidence investigation
  -> diagnosis engine
  -> structured diagnosis
  -> evaluation
```

## Current Baseline

The implementation uses a deterministic diagnosis engine so the workflow can be tested without an LLM or paid service.

The baseline is intentionally treated as a reference implementation. The next AI milestone is to introduce a model-backed diagnosis engine and compare it against this baseline using the same evaluation contract.

## Known Limitations

- No model-backed reasoning yet.
- No HTTP API yet.
- MCP is currently represented through an internal provider boundary and deterministic simulator rather than a deployed MCP server transport.
- No real production observability sources are connected.
- No remediation execution is enabled.

These limitations are intentional for the first vertical slice.
