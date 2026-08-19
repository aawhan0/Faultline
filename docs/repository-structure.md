# Repository Structure

```text
Faultline/
├── docs/
│   ├── architecture.md
│   └── repository-structure.md
├── src/
│   └── faultline/
│       ├── api/
│       ├── agent/
│       ├── core/
│       ├── evals/
│       ├── mcp/
│       └── simulator/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evals/
├── README.md
└── ...
```

The structure deliberately separates domain logic, agent behavior, protocol/tool integration, incident simulation, and evaluation. Infrastructure configuration will be introduced only when a concrete component requires it.
