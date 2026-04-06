import requests
import json

def callOLLAMA(user_message):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "phi3",
        "prompt": user_message,
        "stream": False
    }
    try:
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=120
        )
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response from AI.").strip()
        else:
            return f"⚠️ Server Error: Status {response.status_code}"
    except Exception as e:
        return f"❌ Connection Error: Ensure Ollama is running. ({str(e)})"