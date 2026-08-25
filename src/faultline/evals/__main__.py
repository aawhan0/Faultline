from __future__ import annotations

import argparse

from faultline.agent.llm_agent import LLMAgent
from faultline.agent.ollama import OllamaProvider
from faultline.evals.aggregate import run_evaluations
from faultline.evals.report import EvaluationReport
from faultline.mcp.simulator_provider import SimulatorEvidenceProvider
from faultline.simulator.scenarios import database_pool_exhaustion


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

    args = parser.parse_args()

    scenario = database_pool_exhaustion()
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

    report = EvaluationReport(aggregate=aggregate)

    print(report.to_text())


if __name__ == "__main__":
    main()
