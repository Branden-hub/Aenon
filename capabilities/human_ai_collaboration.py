from core.aenon import CapabilityBase

class HumanAICollaboration(CapabilityBase):
    def __init__(self, config):
        super().__init__(config)
        self.feedback_log = []

    def record_feedback(self, feedback: str, context: dict):
        self.feedback_log.append((feedback, context))
        # Also store in memory
        if self.aenon.memory:
            self.aenon.memory.store(
                context="human_feedback",
                content={"feedback": feedback, "context": context},
                metadata={"type": "feedback"}
            )

    def integrate_feedback(self):
        # Process the feedback to improve the system
        # This is a placeholder for a more complex process
        print("Integrating human feedback...")
