import matplotlib.pyplot as plt
import numpy as np

class CoherenceTracker:
    def __init__(self):
        self.history = {"cv_gpt": [], "cv_claude": [], "cv_gemini": [], "cv_agent": []}

    def log(self, scores: dict):
        for key in self.history:
            self.history[key].append(scores.get(key, 0.0))

    def plot(self, filename="coherence_plot.png"):
        plt.figure(figsize=(10, 5))
        for key, values in self.history.items():
            plt.plot(values, label=key.replace("cv_", "").upper())
        
        plt.title("External AI Coherence Over Time (Aenōn's Mirror)")
        plt.xlabel("Cognition Cycle")
        plt.ylabel("Alignment Coherence (Cosine Similarity)")
        plt.ylim(-1, 1)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
