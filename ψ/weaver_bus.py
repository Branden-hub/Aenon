import numpy as np
import hashlib

class WeaverBus:
    def __init__(self, phase_seed=0.001):
        self.phase = phase_seed
        self.stream = {}

    def encode(self, name, vector):
        signal = np.fft.fft(vector)
        phase_code = np.sin(np.arange(len(vector)) + self.phase)
        self.stream[name] = np.real(signal * phase_code)

    def decode(self, name):
        if name in self.stream:
            raw_signal = self.stream[name]
            inverted_vector = np.fft.ifft(raw_signal).real
            return np.clip(inverted_vector, 0.0, 1.0)
        return np.zeros(13)

    def broadcast(self, agents_to_broadcast):
        return {name: self.decode(name) for name in agents_to_broadcast}

    def project_and_reflect(self, name, vector, memory):
        self.encode(name, vector)
        echo = self.decode(name)
        memory.store_echo(name, echo)
        truth = memory.detect_truth_invariant(echo)
        return echo, truth
