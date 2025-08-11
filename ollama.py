import requests
import json

def callOLLAMA(user_message: str, host: str = "http://localhost:11434", model: str = "phi3", timeout: int = 120):
    """
    Call the local Ollama server generate endpoint.
    Returns a string response (bot reply).
    """
    url = f"{host}/api/generate"
    payload = {
        "model": model,
        "prompt": user_message,
        "stream": False
    }

    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload), timeout=timeout)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Return a friendly message if the server is down or unreachable
        return f"Error: could not reach Ollama server ({e}). Please ensure Ollama is running locally."

    try:
        result = response.json()
        # adapt to the exact JSON structure returned by your Ollama instance
        # replace 'response' with the correct key if different
        bot_response = result.get("response") or result.get("text") or result.get("output") or ""
        if isinstance(bot_response, list):
            bot_response = " ".join(bot_response)
        return bot_response.strip() or "Sorry, I couldn't generate a response."
    except ValueError:
        return "Error: received invalid JSON from Ollama."
