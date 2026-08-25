from faultline.evals import __main__


def test_cli_main_exists() -> None:
    assert callable(__main__.main)
