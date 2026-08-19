# Faultline Development Workflow

Faultline uses an issue-driven, branch-based development process.

## Change Lifecycle

```text
Issue
  |
  v
Branch
  |
  v
Implementation + Tests
  |
  v
Pull Request
  |
  v
Checks + Review
  |
  v
Merge to main
  |
  v
Close Issue
```

## Branch Strategy

`main` is the integration branch and should remain deployable.

Work is performed on focused branches:

- `feature/<name>`
- `fix/<name>`
- `refactor/<name>`
- `test/<name>`
- `docs/<name>`
- `chore/<name>`

Branches should represent one logical unit of work and should normally map to one issue.

## Issues

Every meaningful change should start with an issue. Issues should contain enough context for the implementation to have a clear definition of done.

Recommended labels:

### Type

- `feature`
- `fix`
- `refactor`
- `test`
- `docs`
- `chore`

### Area

- `agent`
- `mcp`
- `evals`
- `api`
- `simulator`
- `observability`
- `security`
- `infra`
- `testing`

### Priority

- `priority: high`
- `priority: medium`
- `priority: low`

### Status

- `status: in progress`
- `status: blocked`
- `status: ready for review`

## Pull Requests

Pull requests should:

1. Reference the issue they implement.
2. Explain the design and implementation clearly.
3. Include relevant tests or validation evidence.
4. Call out operational, security, and evaluation considerations.
5. Keep the scope focused.

## Commits

Use conventional prefixes and concise descriptions:

```text
feat: add incident ingestion
fix: handle empty log results
refactor: split evidence service
test: cover root cause scoring
docs: document MCP contracts
chore: update CI configuration
```

Commits should describe one coherent change and avoid unrelated formatting or cleanup.

## AI-Specific Engineering Expectations

Changes to agent behavior should be treated as software changes, not only prompt changes. When applicable, changes should include:

- deterministic or reproducible test cases
- evaluation coverage
- model/prompt configuration notes
- tool-call behavior checks
- failure-mode testing
- comparison against an existing baseline

## Merging

A change is ready to merge when the issue acceptance criteria are satisfied, relevant automated checks pass, the pull request has been reviewed, and any required follow-up work is documented.
