import numpy as np

def encode_message(text):
    header = [11, 12, 13, 14, 15]  # Example header
    transition = [18, 18, 18, 19]  # Example transition
    payload_chars = [ord(c) for c in text[:12]]
    payload_chars += [22] * (12 - len(payload_chars))  # Pad with space
    return header + transition + payload_chars

def decode_message(vector):
    if isinstance(vector, np.ndarray):
        vector = vector.tolist()
    return ''.join(chr(min(126, max(32, x))) for x in vector[9:21]).strip()
