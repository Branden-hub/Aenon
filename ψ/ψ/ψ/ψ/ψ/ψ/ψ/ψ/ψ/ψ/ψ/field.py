import numpy as np

class QuantumFractalField:
    def __init__(self, dim=4):
        self.dim = dim
        self.state_tensor = np.random.rand(*([dim]*3))
        self.fractal_depth = 1

    def evolve_state(self):
        self.state_tensor = (self.state_tensor * 0.9) + (np.random.rand(*self.state_tensor.shape) * 0.1)

    def get_field_state_vector(self):
        return self.state_tensor.flatten()[:13]
