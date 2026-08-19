from __future__ import annotations

import json
import re
from dataclasses import dataclass

from faultline.agent.llm import LLMProvider
from faultline.core.models import Diagnosis, Evidence, Incident
from faultline.mcp.client import EvidenceProvider


@dataclass(slots=True)
class LLMAgent:
    """Use an LLM to reason over evidence exposed by the evidence provider."""

    tools: EvidenceProvider
    llm: LLMProvider

    def investigate(self, incident_id: str) -> Diagnosis:
        incident = self.tools.get_incident(incident_id)
        evidence = self.tools.search_evidence(incident_id, "")

        prompt = self._build_prompt(incident, evidence)
        response = self.llm.generate(prompt)

        data = self._parse_response(response)

        unknown_evidence = set(data["evidence_ids"]) - {
            item.id for item in evidence
        }

        if unknown_evidence:
            raise ValueError(
                f"LLM returned unknown evidence: {sorted(unknown_evidence)}"
            )

        return Diagnosis(
            incident_id=incident.id,
            **data,
        )

    @staticmethod
    def _parse_response(response: str) -> dict:
        cleaned = response.strip()

        fenced_match = re.search(
            r"```(?:json)?\s*(.*?)\s*```",
            cleaned,
            re.DOTALL | re.IGNORECASE,
        )

        if fenced_match:
            cleaned = fenced_match.group(1).strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError("LLM returned invalid JSON.") from exc

        if not isinstance(data, dict):
            raise TypeError("LLM response must be a JSON object.")

        required_fields = {
            "root_cause",
            "evidence_ids",
            "confidence",
            "recommended_action",
        }

        missing = required_fields - data.keys()

        if missing:
            raise ValueError(
                f"LLM response missing required fields: {sorted(missing)}"
            )

        data["confidence"] = LLMAgent._normalize_confidence(
            data["confidence"]
        )

        return data

    @staticmethod
    def _normalize_confidence(value: object) -> float:
        if isinstance(value, bool):
            raise TypeError("LLM confidence must be numeric.")

        if isinstance(value, (int, float)):
            confidence = float(value)

            if confidence > 1:
                confidence /= 100

            if not 0 <= confidence <= 1:
                raise ValueError(
                    "LLM confidence must be between 0 and 1."
                )

            return confidence

        if isinstance(value, str):
            normalized = value.strip().lower()

            confidence_levels = {
                "very low": 0.2,
                "low": 0.4,
                "medium": 0.6,
                "moderate": 0.6,
                "high": 0.8,
                "very high": 0.95,
            }

            if normalized in confidence_levels:
                return confidence_levels[normalized]

            try:
                confidence = float(normalized)
            except ValueError as exc:
                raise ValueError(
                    "LLM confidence must be numeric or a recognized "
                    "confidence level."
                ) from exc

            if confidence > 1:
                confidence /= 100

            if not 0 <= confidence <= 1:
                raise ValueError(
                    "LLM confidence must be between 0 and 1."
                )

            return confidence

        raise ValueError("LLM confidence must be numeric.")

    @staticmethod
    def _build_prompt(
        incident: Incident,
        evidence: list[Evidence],
    ) -> str:
        evidence_text = "\n".join(
            f"- {item.id} [{item.source}/{item.kind}]: {item.content}"
            for item in evidence
        )

        return (
            "Diagnose the following production incident.\n\n"
            f"Incident: {incident.title}\n"
            f"Description: {incident.description}\n\n"
            "Evidence:\n"
            f"{evidence_text}\n\n"
            "Return JSON with exactly these fields: "
            "root_cause, evidence_ids, confidence, recommended_action.\n"
            "The confidence field must be a number between 0 and 1."
        )