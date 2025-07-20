class ActuatorBase:
    def __init__(self, config):
        self.config = config

    def execute(self, action: dict):
        raise NotImplementedError

class IoTActuator(ActuatorBase):
    def execute(self, action: dict):
        # Example: {"device": "thermostat", "command": "set_temperature", "value": 72}
        # We would use an IoT API to send the command
        print(f"IoTActuator: Executing {action}")

class RoboticActuator(ActuatorBase):
    def execute(self, action: dict):
        # Example: {"robot": "arm", "command": "grab", "position": [0.5, 0.2, 0.1]}
        # We would use ROS or similar to send the command
        print(f"RoboticActuator: Executing {action}")

class WebServiceActuator(ActuatorBase):
    def execute(self, action: dict):
        # Example: {"service": "calendar", "command": "create_event", "details": {...}}
        # We would call a web API
        print(f"WebServiceActuator: Executing {action}")
