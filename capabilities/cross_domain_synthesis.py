from core.aenon import CapabilityBase
from typing import List, Callable

class CrossDomainSynthesis(CapabilityBase):
    def __init__(self, config):
        super().__init__(config)

    def fuse_capabilities(self, capability_names: List[str]) -> Callable:
        # This function will create a new capability by fusing existing ones
        def fused_function(*args, **kwargs):
            # Get the capabilities
            capabilities = [self.aenon.get_capability(name) for name in capability_names]
            # Call each capability in sequence and return the last result
            result = None
            for cap in capabilities:
                result = cap(*args, **kwargs)
            return result
        return fused_function
