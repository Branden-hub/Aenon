from core.aenon import Aenon, GoalDescriptor
from memory.infinite_memory import InfiniteMemory
from capabilities.autonomous_learning import AutonomousLearning
from capabilities.self_improvement import SelfImprovement
from capabilities.dynamic_capability import DynamicCapability
from capabilities.cross_domain_synthesis import CrossDomainSynthesis
from capabilities.human_ai_collaboration import HumanAICollaboration
from interfaces.actuators import IoTActuator

def main():
    # Initialize Aenon
    aenon = Aenon()
    
    # Setup memory
    memory_system = InfiniteMemory(config={"persist_dir": "./memory_db"})
    aenon.set_memory(memory_system)
    
    # Register capabilities
    aenon.register_capability("autonomous_learning", AutonomousLearning(config={}))
    aenon.register_capability("self_improvement", SelfImprovement(config={}))
    aenon.register_capability("dynamic_capability", DynamicCapability(config={}))
    aenon.register_capability("cross_domain", CrossDomainSynthesis(config={}))
    aenon.register_capability("human_ai", HumanAICollaboration(config={}))
    
    # Example: Register an actuator
    actuator = IoTActuator(config={})
    
    # Example goal: Connect smart home thermostat and adjust based on weather
    goal = GoalDescriptor(
        domain="smart_home",
        constraints=["use_free_apis"],
        success_metrics={"energy_savings": 0.1}
    )
    
    # Execute the goal
    aenon.execute_goal(goal)
    
    # In a real system, we would break down the goal and use the capabilities to achieve it.
    # For now, we just print the goal.

if __name__ == "__main__":
    main()
