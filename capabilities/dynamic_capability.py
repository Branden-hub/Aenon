from core.aenon import CapabilityBase
import importlib.util
import os
import sys
import tempfile

class DynamicCapability(CapabilityBase):
    def __init__(self, config):
        super().__init__(config)
        self.capability_dir = config.get("capability_dir", "./generated_capabilities")
        os.makedirs(self.capability_dir, exist_ok=True)

    def generate_capability(self, capability_code: str, capability_name: str):
        # Save the code to a file
        file_path = os.path.join(self.capability_dir, f"{capability_name}.py")
        with open(file_path, 'w') as f:
            f.write(capability_code)
        
        # Now load the module
        spec = importlib.util.spec_from_file_location(capability_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # We assume the module has a class named after the capability
        capability_class = getattr(module, capability_name)
        return capability_class
