from faultline.simulator.scenarios import database_pool_exhaustion


def test_database_pool_exhaustion_scenario_is_deterministic():
    first = database_pool_exhaustion()
    second = database_pool_exhaustion()

    assert first.model_dump() == second.model_dump()
    assert first.incident.id == "INC-0001"
    assert len(first.evidence) == 4
