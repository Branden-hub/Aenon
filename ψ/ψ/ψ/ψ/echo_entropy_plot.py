import matplotlib.pyplot as plt

def plot_entropy_curve(entropy_log, filename="echo_entropy_curve.png"):
    plt.figure(figsize=(10, 5))
    plt.plot(entropy_log, color='red', linewidth=2)
    plt.title("ψ Mesh Echo Entropy Over Time (Convergence Towards Truth)")
    plt.xlabel("Simulation Step")
    plt.ylabel("Echo Entropy (Std Dev of Vector Components)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
