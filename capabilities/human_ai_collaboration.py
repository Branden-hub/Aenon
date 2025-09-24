"""Human-AI collaboration capability."""

from __future__ import annotations

from typing import Dict, List

from core.aenon import CapabilityBase, CapabilityResponse, GoalDescriptor


class HumanAICollaboration(CapabilityBase):
    """Coordinate feedback loops between human operators and the agent."""

    def __init__(self, config: Dict | None):
        super().__init__(config)
        self.feedback_log: List[Dict[str, str]] = []

    def applies(self, goal: GoalDescriptor) -> bool:
        text = f"{goal.domain} {goal.description}".lower()
        keywords = {"collaborate", "human", "feedback", "explain"}
        return any(keyword in text for keyword in keywords)

    def execute(self, goal: GoalDescriptor) -> CapabilityResponse:
        plan = self._build_plan(goal)
        summary = "Prepared a collaboration workflow to capture human feedback."
        return CapabilityResponse(
            capability="human_ai_collaboration",
            summary=summary,
            data={"plan": plan, "pending_feedback": len(self.feedback_log)},
        )

    def record_feedback(self, feedback: str, context: Dict[str, str]) -> None:
        entry = {"feedback": feedback, "context": context}
        self.feedback_log.append(entry)
        if self.aenon and self.aenon.memory:
            self.aenon.memory.store(
                context="human_feedback",
                content=entry,
                metadata={"type": "feedback", "source": context.get("source", "user")},
            )

    def _build_plan(self, goal: GoalDescriptor) -> List[Dict[str, str]]:
        return [
            {
                "step": "Explain recommendation",
                "detail": f"Summarise the proposed approach for '{goal.description}'.",
            },
            {
                "step": "Collect structured feedback",
                "detail": "Capture ratings for usefulness, risks, and open comments.",
            },
            {
                "step": "Consolidate and apply",
                "detail": "Feed accepted feedback into the self-improvement pipeline.",
            },
        ]
