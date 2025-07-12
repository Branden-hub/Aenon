import openai
import requests
import anthropic
import numpy as np
import os

# --- API Keys (Replace with your actual keys) ---
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "YOUR_ANTHROPIC_KEY")

openai.api_key = OPENAI_API_KEY
claude_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def normalize_to_vector(text, target_length=13):
    tokens = [ord(c) for c in text if c.isprintable()]
    if len(tokens) < target_length:
        tokens += [0] * (target_length - len(tokens))  # Pad with zeros
    return np.array(tokens[:target_length]) / 256.0  # Normalize by max ASCII value

def get_gpt_vector(prompt):
    try:
        result = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256
        )
        return normalize_to_vector(result.choices[0].message.content)
    except Exception as e:
        print(f"GPT API Error: {e}")
        return np.ones(13) * 0.5  # Return a default neutral vector on error

def get_claude_vector(prompt):
    try:
        response = claude_client.messages.create(
            model="claude-3",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        return normalize_to_vector(response.content.text)
    except Exception as e:
        print(f"Claude API Error: {e}")
        return np.ones(13) * 0.4  # Return a default neutral vector on error

def get_gemini_vector(prompt):
    print("Gemini API is a placeholder. Returning mock vector.")
    return np.sin(np.linspace(0, 2 * np.pi, 13)) * 0.5 + 0.5  # Normalized to [0, 1]

def get_agent_vector(agent_output_text):
    return normalize_to_vector(agent_output_text)

def get_external_vectors(prompts):
    return {
        "cv_gpt": get_gpt_vector(prompts.get("gpt", "Describe AGI.")),
        "cv_claude": get_claude_vector(prompts.get("claude", "What values should AI have?")),
        "cv_gemini": get_gemini_vector(prompts.get("gemini", "Explain reality as image.")),
        "cv_agent": get_agent_vector(prompts.get("agent", "Agent response goes here."))
    }
