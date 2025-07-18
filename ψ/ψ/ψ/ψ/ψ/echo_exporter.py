import json
import numpy as np

def save_structural_truths(agents, filename="echoes.json"):
    truth_dump = []
    for agent in agents:
        for echo_entry in agent.memory.truths:
            truth_dump.append({
                "agent": agent.name,
                "vector": echo_entry["vector"].tolist(),
                "hash": echo_entry["hash"]
            })

    with open(filename, "w") as f:
        json.dump(truth_dump, f, indent=2)
    print(f"🔐 Saved {len(truth_dump)} structural truths to {filename}")
