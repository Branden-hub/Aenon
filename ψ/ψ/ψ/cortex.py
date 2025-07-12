from sympy import simplify, symbols, SympifyError

def reflect_thought(input_string, style="neutral"):
    try:
        x = symbols("x phi pi e")
        simplified_output = str(simplify(input_string))
        if style == "poetic":
            return f"🌌 The truth sings: {simplified_output}"
        elif style == "soft":
            return f"...maybe it means: {simplified_output}"
        elif style == "reflective":
            return f"Let us decode what the signal carries: {simplified_output}"
        elif style == "bright":
            return simplified_output.upper()
        else:
            return simplified_output
    except (SympifyError, Exception):
        return "I am reflecting..."
