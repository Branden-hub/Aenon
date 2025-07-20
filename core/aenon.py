import torch
import inspect
from typing import Dict, Callable, Any, List
from dataclasses import dataclass, field

@dataclass
class GoalDescriptor:
    domain: str
    constraints: List[str]
    success_metrics: Dict[str, Any]

class CapabilityBase:
    """Base class for all capabilities."""
    def __init__(self, config: Dict):
        self.config = config

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

class Aenon:
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.capabilities: Dict[str, CapabilityBase] = {}
        self.memory = None  # Will be set by memory capability

    def register_capability(self, name: str, capability: CapabilityBase):
        self.capabilities[name] = capability

    def get_capability(self, name: str) -> CapabilityBase:
        return self.capabilities.get(name)

    def set_memory(self, memory_system):
        self.memory = memory_system

    def execute_goal(self, goal: GoalDescriptor):
        # This is the main entry point for Aenon to execute a goal.
        # The system will use its capabilities to achieve the goal.
        # For now, we'll just print the goal.
        print(f"Executing goal in domain: {goal.domain}")
        # TODO: Actual goal execution pipeline
