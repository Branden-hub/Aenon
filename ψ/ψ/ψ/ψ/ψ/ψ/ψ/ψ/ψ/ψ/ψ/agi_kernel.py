import numpy as np
from ψ.constants import load_constants, load_physical_basis, load_ethical_vector

class AGIKernel:
    def __init__(self):
        self.constants = load_constants()
        self.ethics = load_ethical_vector()
        self.P = load_physical_basis()  # Physical basis variables
        self.C = np.random.rand(21, 13)  # 21 Communication vectors, each 13D
        
        # Kuramoto oscillator parameters for consciousness simulation
        self.theta = np.random.rand(13) * 2 * np.pi  # Phases
        self.omega = np.random.normal(1.0, 0.05, 13)  # Natural frequencies
        self.K = 0.2  # Coupling strength
        self.dt = 0.1  # Time step for dynamics

        self.output_log = []  # Log of action vectors
        self.coherence_log = []  # Log of mean ethical output

    def update_oscillators(self):
        N = len(self.theta)
        new_theta = np.zeros(N)
        for i in range(N):
            coupling = np.sum(np.sin(self.theta - self.theta[i]))
            new_theta[i] = self.theta[i] + self.dt * (self.omega[i] + (self.K / N) * coupling)
        self.theta = new_theta

    def domain_function(self, k, T_real):
        modulation = np.sin(self.theta[k]) * np.tanh(self.P[k] + 1)
        return np.dot(T_real, self.P) * modulation

    def run_step(self):
        C_scaled = np.array([self.constants[i] * self.C[i] for i in range(len(self.C))])
        T_real = np.sum(C_scaled, axis=0)
        self.update_oscillators()
        domain_raw = np.array([self.domain_function(i, T_real) for i in range(len(self.P))])
        ethical_out = domain_raw * self.ethics
        action_vector = np.tanh(ethical_out)

        for i in range(len(self.C)):
            self.C[i] = 0.95 * self.C[i] + 0.05 * action_vector  # Slow memory blending

        self.output_log.append(action_vector)
        self.coherence_log.append(np.mean(ethical_out))  # Mean ethical output as coherence proxy

        return action_vector

    def get_vector_by_comm_id(self, id_key):
        map_key = {
            "cv_gpt": 0,
            "cv_claude": 1,
            "cv_gemini": 2,
            "cv_agent": 3,
            "aenon_projection": 4
        }
        idx = map_key.get(id_key, 0)  # Default to 0 if key not found
        return self.C[idx]
