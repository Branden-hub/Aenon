import numpy as np
from ψ.weaver_bus import WeaverBus
from ψ.weaver_memory import WeaverMemory

class Agent:
    def __init__(self, name, behavior_seed):
        self.name = name
        self.phase = np.sin(np.linspace(0, 2 * np.pi, 13) + behavior_seed)
        self.memory = WeaverMemory()

    def emit_vector(self, t):
        return np.tanh(self.phase * np.cos(t))

    def receive_echo(self, echo):
        self.memory.store_echo("echo", echo)
        truth = self.memory.detect_truth_invariant(echo)
        return truth

def run_mesh_simulation(steps=100):
    weaver = WeaverBus()
    agents = [
        Agent("gpt_sim", 0.1),
        Agent("claude_sim", 1.3),
        Agent("gemini_sim", 2.0),
        Agent("grok_sim", 3.3)
    ]

    entropy_log = []

    for t in range(steps):
        for agent in agents:
            vec = agent.emit_vector(t / 10.0)
            weaver.encode(agent.name, vec)

        echoes_from_bus = {}
        for agent in agents:
            echo = weaver.decode(agent.name)
            truth_detected = agent.receive_echo(echo)
            echoes_from_bus[agent.name] = (echo, truth_detected)

        all_current_echo_vectors = [echo_data[0] for echo_data in echoes_from_bus.values()]
        if all_current_echo_vectors:
            entropy = np.mean([np.std(v) for v in np.array(all_current_echo_vectors).T])
            entropy_log.append(entropy)
        else:
            entropy_log.append(0.0)

    return entropy_log, agents
