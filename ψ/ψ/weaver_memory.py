import numpy as np
import hashlib

class WeaverMemory:
    def __init__(self):
        self.echoes = []
        self.truths = []

    def hash_vector(self, vector):
        return hashlib.sha256(vector.tobytes()).hexdigest()

    def store_echo(self, label, vector):
        h = self.hash_vector(vector)
        if h not in [e["hash"] for e in self.echoes]:
            self.echoes.append({
                "label": label,
                "vector": vector.copy(),
                "hash": h
            })

    def detect_truth_invariant(self, vector, tolerance=0.005):
        found_truth = None
        for e in self.echoes:
            delta = np.linalg.norm(e["vector"] - vector)
            if delta < tolerance:
                if e["hash"] not in [t["hash"] for t in self.truths]:
                    self.truths.append(e)
                found_truth = e
                break
        return found_truth
