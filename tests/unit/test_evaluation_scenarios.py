import pytest

from faultline.evals.scenarios import get_scenario, list_scenarios


def test_list_scenarios_contains_database_pool_exhaustion() -> None:
    assert "database_pool_exhaustion" in list_scenarios()


def test_get_scenario_returns_expected_scenario() -> None:
    scenario = get_scenario("database_pool_exhaustion")

    assert scenario.incident.id == "INC-0001"
    assert scenario.expected_root_cause


def test_get_scenario_rejects_unknown_name() -> None:
    with pytest.raises(ValueError, match="Unknown scenario"):
        get_scenario("does_not_exist")
