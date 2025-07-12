import numpy as np

class VectorEvolver:
    def __init__(self, learning_rate=0.01):
        self.lr = learning_rate

    def evolve(self, kernel, coherence_map):
        idx_map = {"cv_gpt": 0, "cv_claude": 1, "cv_gemini": 2, "cv_agent": 3}

        for key, score in coherence_map.items():
            idx = idx_map.get(key)
            if idx is not None:
                adjustment_direction = (score - 0.5)
                kernel.C[idx] += adjustment_direction * self.lr
                kernel.C[idx] = np.clip(kernel.C[idx], 0.0, 1.0)
