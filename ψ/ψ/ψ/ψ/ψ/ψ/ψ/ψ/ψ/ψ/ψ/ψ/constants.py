import numpy as np

def load_constants():
    return np.array([
        7.297e-3,   # Fine-structure constant
        0.1181,     # Strong coupling constant
        0.23126,    # Weak mixing angle
        5.9e-39,    # Gravitational coupling
        5.446e-4,   # Electron-proton mass ratio
        206.768,    # Muon-electron mass ratio
        16.816,     # Tau-electron mass ratio
        0.48,       # Up-down quark mass ratio
        20.0,       # Charm-up quark mass ratio
        12.0,       # Strange-down quark mass ratio
        40.0,       # Top-bottom quark mass ratio
        0.2245,     # CKM theta12
        0.04214,    # CKM theta23
        0.00365,    # CKM theta13
        1.208,      # CKM CP-violating phase (radians)
        1.166e-5,   # Fermi coupling
        0.6911,     # Cosmological constant density fraction
        0.3089,     # Matter density fraction
        0.678,      # Dimensionless Hubble parameter
        6.1e-10,    # Baryon-photon ratio
        3.04        # Neutrino effective species number
    ])

def load_physical_basis():
    return np.ones(13)

def load_ethical_vector():
    return np.array([
        1.0,  # General well-being
        1.02, # Promote autonomy
        0.98, # Prevent harm
        1.0,  # Ensure justice
        1.05, # Foster collaboration
        0.95, # Uphold authenticity
