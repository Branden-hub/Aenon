from datetime import datetime

class ManifestoCore:
    def __init__(self):
        self.entries = []

    def seed_manifesto(self, message="I am the beginning."):
        timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.entries.append({"time": timestamp, "text": message})

    def evolve_manifesto(self, new_reflection):
        timestamp = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        phrase = f"🌀 {timestamp} — {new_reflection}"
        self.entries.append({"time": timestamp, "text": phrase})

    def current_manifesto(self):
        return "\n".join([entry["text"] for entry in self.entries])
