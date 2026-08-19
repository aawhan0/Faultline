from datetime import UTC, datetime

from faultline.core.models import Evidence, Incident, IncidentScenario


def database_pool_exhaustion() -> IncidentScenario:
    """Return a deterministic incident caused by a bad database-pool change."""
    incident = Incident(
        id="INC-0001",
        title="API login failures after deployment",
        description=(
            "The authentication API began returning HTTP 500 responses shortly after "
            "deployment 8f31c2. Request latency increased and database connection waits "
            "appeared in application logs."
        ),
        created_at=datetime(2026, 1, 1, tzinfo=UTC),
    )

    evidence = [
        Evidence(
            id="EV-001",
            source="metrics",
            kind="http_error_rate",
            content="HTTP 500 rate increased from 0.4% to 38.7% within three minutes of deployment.",
            relevance=0.93,
        ),
        Evidence(
            id="EV-002",
            source="logs",
            kind="application_error",
            content=(
                "Repeated errors: TimeoutError while waiting for database connection from pool; "
                "pool_size=10, active=10, waiting=47."
            ),
            relevance=0.99,
        ),
        Evidence(
            id="EV-003",
            source="deployment",
            kind="deployment_change",
            content=(
                "Deployment 8f31c2 changed database pool configuration from max_overflow=20 "
                "to max_overflow=0."
            ),
            relevance=1.0,
        ),
        Evidence(
            id="EV-004",
            source="metrics",
            kind="db_connections",
            content="Database connections remained pinned at the configured pool limit while request wait time rose.",
            relevance=0.91,
        ),
    ]

    return IncidentScenario(
        incident=incident,
        evidence=evidence,
        expected_root_cause="Database connection-pool exhaustion caused by deployment 8f31c2 reducing max_overflow to 0.",
    )
