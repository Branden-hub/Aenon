"""Self improvement capability for the Aenon agent."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

from core.aenon import CapabilityBase, CapabilityResponse, GoalDescriptor


class SelfImprovement(CapabilityBase):
    """Analyse the agent's tools and suggest refinements."""

    def __init__(self, config: Dict | None):
        super().__init__(config)
        self.registry: Dict[str, Dict[str, Any]] = {}

    def register_algorithm(self, name: str, telemetry_fn: Callable[[], Dict[str, Any]]) -> None:
        """Register an algorithm that can be introspected."""

        self.registry[name] = {"telemetry_fn": telemetry_fn}

    def applies(self, goal: GoalDescriptor) -> bool:
        text = f"{goal.domain} {goal.description}".lower()
        keywords = {"improve", "optimise", "optimize", "refine", "self"}
        return any(keyword in text for keyword in keywords)

    def execute(self, goal: GoalDescriptor) -> CapabilityResponse:
        suggestions = self._build_suggestions(goal)
        insights = self._collect_feedback()
        summary = "Identified improvement opportunities for the agent's toolkit."

        return CapabilityResponse(
            capability="self_improvement",
            summary=summary,
            insights=insights,
            data={"suggestions": suggestions},
        )

    # ------------------------------------------------------------------
    def _collect_feedback(self) -> List[str]:
        if not self.aenon or not self.aenon.memory:
            return []
        feedback_entries = self.aenon.memory.retrieve("feedback", n_results=5)
        return [entry.get("content", {}).get("feedback", "") for entry in feedback_entries if entry.get("content")]

    def _build_suggestions(self, goal: GoalDescriptor) -> List[Dict[str, Any]]:
        suggestions: List[Dict[str, Any]] = []
        for name, payload in self.registry.items():
            telemetry_fn = payload.get("telemetry_fn")
            telemetry = telemetry_fn() if telemetry_fn else {}
            suggestions.append(
                {
                    "component": name,
                    "action": "Tune hyper-parameters based on recent telemetry.",
                    "telemetry": telemetry,
                }
            )

        if not suggestions:
            suggestions.append(
                {
                    "component": "core",
                    "action": "Introduce periodic retrospectives to review failed goals.",
                    "telemetry": {"goal_domain": goal.domain},
                }
            )
        return suggestions
