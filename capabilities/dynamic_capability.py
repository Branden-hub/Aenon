"""Dynamic capability generation for the Aenon agent."""

from __future__ import annotations

import importlib.util
import os
from typing import Any, Dict, List, Type

from core.aenon import CapabilityBase, CapabilityResponse, GoalDescriptor


class DynamicCapability(CapabilityBase):
    """Allow the agent to propose and load new capabilities at runtime."""

    def __init__(self, config: Dict | None):
        super().__init__(config)
        self.capability_dir = self.config.get("capability_dir", "./generated_capabilities")
        os.makedirs(self.capability_dir, exist_ok=True)
        self.generated_capabilities: Dict[str, str] = {}

    def applies(self, goal: GoalDescriptor) -> bool:
        text = f"{goal.domain} {goal.description}".lower()
        keywords = {"extend", "capability", "plugin", "integration"}
        return any(keyword in text for keyword in keywords)

    def execute(self, goal: GoalDescriptor) -> CapabilityResponse:
        proposal = self._build_proposal(goal)
        summary = "Outlined a strategy for extending the agent with domain specific plugins."
        return CapabilityResponse(
            capability="dynamic_capability",
            summary=summary,
            data={
                "proposal": proposal,
                "available_capabilities": list(self.generated_capabilities.keys()),
            },
        )

    # ------------------------------------------------------------------
    def generate_capability(self, capability_code: str, capability_name: str) -> Type[Any]:
        """Persist and import a capability implementation."""

        file_path = os.path.join(self.capability_dir, f"{capability_name}.py")
        with open(file_path, "w", encoding="utf-8") as handle:
            handle.write(capability_code)

        spec = importlib.util.spec_from_file_location(capability_name, file_path)
        if not spec or not spec.loader:
            raise ImportError(f"Unable to load capability {capability_name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[arg-type]

        capability_class = getattr(module, capability_name)
        self.generated_capabilities[capability_name] = file_path
        return capability_class

    def _build_proposal(self, goal: GoalDescriptor) -> List[Dict[str, str]]:
        constraints = ", ".join(goal.constraints) if goal.constraints else "none"
        return [
            {
                "step": "Extract requirements",
                "detail": f"Capture reusable behaviours from the goal description (constraints: {constraints}).",
            },
            {
                "step": "Draft capability skeleton",
                "detail": "Create a Python template that implements the CapabilityBase interface.",
            },
            {
                "step": "Evaluate and register",
                "detail": "Load the generated module, run smoke tests, and register it with the agent.",
            },
        ]
