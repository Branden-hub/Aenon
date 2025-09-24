"""Actuator definitions used by the Aenon agent."""

from __future__ import annotations

from typing import Any, Dict


class ActuatorBase:
    def __init__(self, config: Dict[str, Any] | None):
        self.config = config or {}

    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class IoTActuator(ActuatorBase):
    """Simulate an IoT actuator."""

    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        message = f"IoTActuator executed action: {action}"
        print(message)
        return {"status": "simulated", "message": message}


class RoboticActuator(ActuatorBase):
    """Simulate a robotic actuator."""

    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        message = f"RoboticActuator executed action: {action}"
        print(message)
        return {"status": "simulated", "message": message}


class WebServiceActuator(ActuatorBase):
    """Simulate calling a remote web service."""

    def execute(self, action: Dict[str, Any]) -> Dict[str, Any]:
        message = f"WebServiceActuator executed action: {action}"
        print(message)
        return {"status": "simulated", "message": message}
