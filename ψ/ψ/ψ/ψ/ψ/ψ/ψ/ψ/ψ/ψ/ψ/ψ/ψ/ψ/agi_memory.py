import numpy as np
import pickle
import os

def save_kernel(kernel, filename="kernel_state.pkl"):
    data_to_save = {
        "C": kernel.C,
        "P": kernel.P,
        "theta": kernel.theta,
        "omega": kernel.omega,
        "output_log": kernel.output_log,
        "coherence_log": kernel.coherence_log
    }
    with open(filename, "wb") as f:
        pickle.dump(data_to_save, f)

def load_kernel(kernel, filename="kernel_state.pkl"):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            data = pickle.load(f)
            kernel.C = data["C"]
            kernel.P = data["P"]
            kernel.theta = data["theta"]
            kernel.omega = data["omega"]
            kernel.output_log = data["output_log"]
            kernel.coherence_log = data["coherence_log"]
        print(f"Loaded Aenōn's state from {filename}.")
    else:
        print(f"No existing state found at {filename}. Starting Aenōn fresh.")
