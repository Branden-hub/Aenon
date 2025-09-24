"""Core orchestration logic for the Aenon agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class GoalDescriptor:
    """Describe a goal that the agent should attempt to satisfy."""

    domain: str
    description: str
    constraints: List[str] = field(default_factory=list)
    success_metrics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "description": self.description,
            "constraints": list(self.constraints),
            "success_metrics": dict(self.success_metrics),
            "metadata": dict(self.metadata),
        }


@dataclass
class CapabilityResponse:
    """Structured response from a capability module."""

    capability: str
    summary: str
    actions: List[Dict[str, Any]] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "capability": self.capability,
            "summary": self.summary,
            "actions": list(self.actions),
            "insights": list(self.insights),
            "data": dict(self.data),
        }


@dataclass
class ExecutionReport:
    """Aggregate report returned after a goal has been processed."""

    goal: GoalDescriptor
    responses: List[CapabilityResponse] = field(default_factory=list)
    memory_reference: Optional[str] = None

    @property
    def summary(self) -> str:
        if not self.responses:
            return "No capabilities produced a response."
        return " ".join(response.summary for response in self.responses)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal.to_dict(),
            "responses": [response.to_dict() for response in self.responses],
            "memory_reference": self.memory_reference,
            "summary": self.summary,
        }


class CapabilityBase:
    """Base class that all capability modules inherit from."""

    description: str | None = None

    def __init__(self, config: Dict[str, Any] | None):
        self.config = config or {}
        self.aenon: Optional[Aenon] = None

    # Hooks -----------------------------------------------------------------
    def attach(self, aenon: "Aenon") -> None:
        """Attach the capability to an :class:`Aenon` instance."""

        self.aenon = aenon

    # ------------------------------------------------------------------
    def applies(self, goal: GoalDescriptor) -> bool:
        """Return ``True`` when the capability can contribute to ``goal``."""

        return True

    def execute(self, goal: GoalDescriptor) -> Optional[CapabilityResponse]:
        """Execute the capability for ``goal``.

        Sub-classes should return a :class:`CapabilityResponse`.  Returning
        ``None`` allows a capability to opt out even when :meth:`applies`
        returned ``True``.
        """

        raise NotImplementedError

    # Helper utilities -------------------------------------------------
    def describe(self) -> str:
        """Human readable description of the capability."""

        doc = (self.__doc__ or "").strip()
        if doc:
            return doc
        if self.description:
            return self.description
        return self.__class__.__name__


class Aenon:
    """Coordinator class that wires capabilities, memory and actuators."""

    def __init__(self, config: Dict[str, Any] | None = None):
        self.config = config or {}
        self.capabilities: Dict[str, CapabilityBase] = {}
        self.actuators: Dict[str, Any] = {}
        self.memory = None  # Will be set via ``set_memory``

    # Registration -----------------------------------------------------
    def register_capability(self, name: str, capability: CapabilityBase) -> None:
        capability.attach(self)
        self.capabilities[name] = capability

    def register_actuator(self, name: str, actuator: Any) -> None:
        self.actuators[name] = actuator

    def get_capability(self, name: str) -> Optional[CapabilityBase]:
        return self.capabilities.get(name)

    def list_capabilities(self) -> Iterable[str]:
        return self.capabilities.keys()

    def describe_capabilities(self) -> Dict[str, str]:
        return {name: capability.describe() for name, capability in self.capabilities.items()}

    # Memory -----------------------------------------------------------
    def set_memory(self, memory_system: Any) -> None:
        self.memory = memory_system

    # Execution --------------------------------------------------------
    def execute_goal(self, goal: GoalDescriptor | Dict[str, Any]) -> ExecutionReport:
        if isinstance(goal, dict):
            goal = GoalDescriptor(**goal)
        if not goal.description:
            raise ValueError("Goal description cannot be empty")

        memory_ref = None
        if self.memory:
            memory_ref = self.memory.store(
                context="goal",
                content=goal.to_dict(),
                metadata={"type": "goal", "domain": goal.domain},
            )

        responses: List[CapabilityResponse] = []
        for name, capability in self.capabilities.items():
            if not capability.applies(goal):
                continue
            response = capability.execute(goal)
            if not response:
                continue
            responses.append(response)
            for action in response.actions:
                self._dispatch_action(action)

        report = ExecutionReport(goal=goal, responses=responses, memory_reference=memory_ref)

        if self.memory:
            self.memory.store(
                context="execution_report",
                content=report.to_dict(),
                metadata={"type": "report", "domain": goal.domain},
            )

        return report

    # ------------------------------------------------------------------
    def _dispatch_action(self, action: Dict[str, Any]) -> None:
        actuator_name = action.get("actuator")
        if not actuator_name:
            return
        actuator = self.actuators.get(actuator_name)
        if not actuator:
            return
        result = actuator.execute(action)
        if self.memory:
            self.memory.store(
                context="actuator_event",
                content={"action": action, "result": result},
                metadata={"type": "actuator", "actuator": actuator_name},
            )
