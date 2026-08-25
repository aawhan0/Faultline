from __future__ import annotations

import argparse

from faultline.agent.llm_agent import LLMAgent
from faultline.agent.ollama import OllamaProvider
from faultline.evals.aggregate import run_evaluations
from faultline.evals.report import EvaluationReport
from faultline.evals.scenarios import get_scenario, list_scenarios
from faultline.mcp.simulator_provider import SimulatorEvidenceProvider


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Faultline LLM evaluations."
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Number of evaluation runs.",
    )
    parser.add_argument(
        "--model",
        default="qwen2.5:3b",
        help="Ollama model to evaluate.",
    )
    parser.add_argument(
        "--scenario",
        default="database_pool_exhaustion",
        choices=list_scenarios(),
        help="Incident scenario to evaluate.",
    )

    args = parser.parse_args()

    if args.runs <= 0:
        parser.error("--runs must be greater than zero.")

    scenario = get_scenario(args.scenario)
    provider = SimulatorEvidenceProvider()

    agent = LLMAgent(
        tools=provider,
        llm=OllamaProvider(model=args.model),
    )

    aggregate = run_evaluations(
        agent=agent,
        scenario=scenario,
        required_evidence_ids={"EV-002", "EV-003"},
        runs=args.runs,
    )

    report = EvaluationReport(
        aggregate=aggregate,
        model=args.model,
        scenario=args.scenario,
    )

    print(report.to_text())


if __name__ == "__main__":
    main()
