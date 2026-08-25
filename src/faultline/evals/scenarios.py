from __future__ import annotations

from collections.abc import Callable

from faultline.core.models import IncidentScenario
from faultline.simulator.scenarios import database_pool_exhaustion

ScenarioFactory = Callable[[], IncidentScenario]


_SCENARIOS: dict[str, ScenarioFactory] = {
    "database_pool_exhaustion": database_pool_exhaustion,
}


def get_scenario(name: str) -> IncidentScenario:
    """Create a scenario by its registered name."""

    try:
        factory = _SCENARIOS[name]
    except KeyError as exc:
        available = ", ".join(sorted(_SCENARIOS))
        raise ValueError(
            f"Unknown scenario '{name}'. Available scenarios: {available}"
        ) from exc

    return factory()


def list_scenarios() -> list[str]:
    """Return registered scenario names in deterministic order."""

    return sorted(_SCENARIOS)
