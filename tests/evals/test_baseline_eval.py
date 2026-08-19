from faultline.evals.baseline import evaluate_baseline


def test_database_pool_baseline_evaluation_passes() -> None:
    result = evaluate_baseline()

    assert result.passed is True
    assert result.root_cause_match is True
    assert result.evidence_grounded is True
    assert result.confidence >= 0.8
