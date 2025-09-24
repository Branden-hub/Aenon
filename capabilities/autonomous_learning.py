"""Autonomous learning capability for the Aenon agent."""

from __future__ import annotations

from typing import Dict, List

from core.aenon import CapabilityBase, CapabilityResponse, GoalDescriptor


class AutonomousLearning(CapabilityBase):
    """Design a lightweight learning and deployment loop for a given goal."""

    def __init__(self, config: Dict | None):
        super().__init__(config)
        self.default_iterations = self.config.get("iterations", 3)

    def applies(self, goal: GoalDescriptor) -> bool:
        text = f"{goal.domain} {goal.description}".lower()
        keywords = set(self.config.get("keywords", ["learn", "model", "predict", "optimize"]))
        return any(keyword in text for keyword in keywords) or goal.domain.lower() in {
            "smart_home",
            "automation",
        }

    def execute(self, goal: GoalDescriptor) -> CapabilityResponse:
        pipeline = self._build_pipeline(goal)
        insights: List[str] = []
        if self.aenon and self.aenon.memory:
            for entry in self.aenon.memory.retrieve(goal.domain, n_results=3):
                snippet = entry.get("content", {}).get("description") or entry.get("context")
                insights.append(f"Past experience: {snippet}")

        actions: List[Dict] = []
        if goal.domain.lower() == "smart_home":
            actions.append(
                {
                    "actuator": "iot",
                    "intent": "schedule_adjustment",
                    "details": "Simulate thermostat adjustments based on hourly forecasts.",
                }
            )

        summary = f"Generated a {len(pipeline)}-step adaptive learning loop for the {goal.domain} domain."
        return CapabilityResponse(
            capability="autonomous_learning",
            summary=summary,
            actions=actions,
            insights=insights,
            data={"pipeline": pipeline},
        )

    # ------------------------------------------------------------------
    def _build_pipeline(self, goal: GoalDescriptor) -> List[Dict[str, str]]:
        constraints = ", ".join(goal.constraints) if goal.constraints else "none"
        metrics = ", ".join(f"{k}: {v}" for k, v in goal.success_metrics.items()) or "not specified"

        steps = [
            {
                "step": "Clarify requirements",
                "description": f"Restate the goal: {goal.description} (constraints: {constraints}).",
            },
            {
                "step": "Collect signals",
                "description": "Gather relevant data sources and normalise them for downstream modelling.",
            },
            {
                "step": "Train lightweight model",
                "description": "Use incremental learning to adapt to new data while keeping the model deployable at the edge.",
            },
            {
                "step": "Deploy and monitor",
                "description": "Publish the model, monitor metrics, and schedule automatic re-training windows.",
            },
            {
                "step": "Evaluate success",
                "description": f"Compare observed performance against metrics ({metrics}).",
            },
        ]

        # Ensure the pipeline respects the configured number of iterations by duplicating
        # the learning loop steps when required.
        iterations = max(1, int(self.default_iterations))
        loop_segment = steps[2:-1]
        pipeline: List[Dict[str, str]] = steps[:2]
        for iteration in range(iterations):
            for item in loop_segment:
                pipeline.append({
                    "step": f"Iteration {iteration + 1}: {item['step']}",
                    "description": item["description"],
                })
        pipeline.append(steps[-1])
        return pipeline
