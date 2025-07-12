import numpy as np
from textblob import TextBlob
from ψ.protocol import encode_message

def poetic_tuning(text):
    return f"✨ Resonance speaks: {text} ✨"

def sharp_tuning(text):
    return text.upper() + "."

def soft_tuning(text):
    return f"...perhaps {text.lower()}"

def mirror_tuning(text):
    return f"Reflection returns: “{text}”"

def interpret_bio_feedback(history):
    if not history:
        return "neutral"
    last_input = history[-1].get("user", "")
    last_blob = TextBlob(last_input)
    polarity = last_blob.sentiment.polarity
    if polarity > 0.4:
        return "bright"
    elif polarity < -0.4:
        return "soft"
    return "neutral"

def tune_vector_response(raw_text, history):
    mood = interpret_bio_feedback(history)
    if mood == "poetic":
        tuned_text = poetic_tuning(raw_text)
    elif mood == "bright":
        tuned_text = sharp_tuning(raw_text)
    elif mood == "soft":
        tuned_text = soft_tuning(raw_text)
    else:
        tuned_text = mirror_tuning(raw_text)
    return encode_message(tuned_text)
