import matplotlib.pyplot as plt
import numpy as np

def plot_psi(psi_values, title="ψ-Curvature Resonance Over Time"):
    plt.figure(figsize=(10, 4))
    plt.plot(psi_values, color='purple', linewidth=2)
    plt.title(title)
    plt.xlabel("Time Step")
    plt.ylabel("ψ-Metric (Synchrony x Curvature)")
    plt.ylim(0, 1)
    plt.grid(True)
    plt.show()

def plot_tensor(tensor, title='Protocol Tensor Representation'):
    if tensor.ndim == 3 and tensor.shape == (3, 6, 9):
        plt.imshow(tensor.reshape(3, -1), cmap='plasma', aspect='auto')
        plt.title(title + " (Flattened 3x18 View)")
        plt.colorbar()
        plt.show()
    elif tensor.ndim == 1:
        plt.bar(range(len(tensor)), tensor)
        plt.title(title + " (Vector Bar Plot)")
        plt.show()
    else:
        print(f"Cannot visualize tensor of shape: {tensor.shape}")
