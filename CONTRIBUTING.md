# Contributing to Faultline

Faultline is developed using a GitHub issue and pull request workflow. Even though this is currently a solo project, the repository follows practices intended for production software development.

## Development Workflow

1. Create or select a GitHub issue for the work.
2. Create a focused branch from `main`.
3. Implement the change and add appropriate tests.
4. Keep commits small and descriptive.
5. Open a pull request against `main`.
6. Review the diff, checks, and issue acceptance criteria.
7. Merge only after the change is complete and verified.
8. Delete the merged branch when it is no longer needed.

## Branch Naming

Use descriptive prefixes:

- `feature/` for new functionality
- `fix/` for bug fixes
- `refactor/` for internal restructuring
- `test/` for test-focused work
- `docs/` for documentation
- `chore/` for tooling and repository maintenance

Examples:

```text
feature/mcp-log-tool
fix/agent-timeout
refactor/evidence-model
chore/ci-pipeline
```

## Commit Messages

Use concise, imperative commit messages with a conventional prefix:

```text
feat: add log search tool
fix: handle unavailable metrics backend
refactor: isolate incident domain models
test: add evidence validation cases
docs: document agent evaluation flow
chore: configure CI checks
```

## Pull Requests

Every pull request should explain:

- What changed
- Why it changed
- How it was tested
- Any important design or operational considerations

Keep pull requests focused on one logical change whenever practical.

## Issues

Issues should describe a concrete piece of work and include acceptance criteria when the work is non-trivial. Use labels to identify the change type, technical area, priority, and status where applicable.

## Quality Bar

Faultline is intended to demonstrate production-oriented engineering practices. Changes should therefore consider:

- Correctness and test coverage
- Failure handling
- Clear interfaces and contracts
- Observability
- Security implications
- Evaluation impact for AI behavior
- Operational simplicity

Experimental work is welcome, but it should remain isolated from stable paths until it is validated.
