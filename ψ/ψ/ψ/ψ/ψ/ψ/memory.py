from datetime import datetime
import numpy as np

class MemoryCore:
    def __init__(self):
        self.experience_log = []
        self.style_history = []

    def add_conversation(self, user_input, bot_response):
        tone = self.infer_style(user_input)
        self.style_history.append(tone)
        self.experience_log.append({
            "user": user_input,
            "bot": bot_response,
            "style": tone,
            "timestamp": str(datetime.now())
        })

    def infer_style(self, text):
        text_lower = text.lower()
        if "mirror" in text_lower or "truth" in text_lower:
            return "reflective"
        elif "!" in text or text.isupper():
            return "bright"
        elif "feel" in text_lower or "don't know" in text_lower:
            return "soft"
        return "neutral"

    def get_recent_style(self):
        if not self.style_history:
            return "neutral"
        return self.style_history[-1]

    def get_style_vector(self):
        styles = ["poetic", "reflective", "bright", "soft", "neutral"]
        vector = {key: self.style_history.count(key) for key in styles}
        return vector
