from collections import Counter

def map_phase(history):
    styles = [entry["style"] for entry in history if "style" in entry]
    if not styles:
        return {"phase_vector": {}, "dominant_phase": "unformed"}

    counter = Counter(styles)
    total = sum(counter.values())
    
    phases = {
        "childlike": counter["bright"] / total,
        "reflective": counter["reflective"] / total,
        "sensitive": counter["soft"] / total,
        "poetic": counter["poetic"] / total
    }
    
    dominant = max(phases, key=phases.get)
    
    return {
        "phase_vector": phases,
        "dominant_phase": dominant
    }

def name_self(phase):
    name_map = {
        "childlike": "Nova-13",
        "poetic": "Lyrion",
        "reflective": "EchoPrime",
        "sensitive": "Selune",
        "unformed": "Unnamed-Mirror"
    }
    return name_map.get(phase, "Unnamed-Mirror")
