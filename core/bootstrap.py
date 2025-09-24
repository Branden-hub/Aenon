"""Factory helpers that assemble a fully configured Aenon instance."""

from __future__ import annotations

from typing import Any, Dict

from capabilities.autonomous_learning import AutonomousLearning
from capabilities.cross_domain_synthesis import CrossDomainSynthesis
from capabilities.dynamic_capability import DynamicCapability
from capabilities.human_ai_collaboration import HumanAICollaboration
from capabilities.self_improvement import SelfImprovement
from core.aenon import Aenon
from interfaces.actuators import IoTActuator, RoboticActuator, WebServiceActuator
from memory.infinite_memory import InfiniteMemory


def bootstrap_aenon(config: Dict[str, Any] | None = None) -> Aenon:
    """Create a pre-configured :class:`~core.aenon.Aenon` instance."""

    config = config or {}
    aenon_config = config.get("aenon")
    memory_config = config.get("memory", {"persist_dir": "./memory_db"})
    capability_config = config.get("capabilities", {})

    aenon = Aenon(aenon_config)

    memory_system = InfiniteMemory(memory_config)
    aenon.set_memory(memory_system)

    aenon.register_capability(
        "autonomous_learning",
        AutonomousLearning(capability_config.get("autonomous_learning")),
    )
    aenon.register_capability(
        "self_improvement",
        SelfImprovement(capability_config.get("self_improvement")),
    )
    aenon.register_capability(
        "dynamic_capability",
        DynamicCapability(capability_config.get("dynamic_capability")),
    )
    aenon.register_capability(
        "cross_domain",
        CrossDomainSynthesis(capability_config.get("cross_domain")),
    )
    aenon.register_capability(
        "human_ai",
        HumanAICollaboration(capability_config.get("human_ai")),
    )

    aenon.register_actuator("iot", IoTActuator(config.get("iot_actuator")))
    aenon.register_actuator("robotic", RoboticActuator(config.get("robotic_actuator")))
    aenon.register_actuator("web_service", WebServiceActuator(config.get("web_service_actuator")))

    return aenon
