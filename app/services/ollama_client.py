import requests

OLLAMA_URL = "http://ollama:11434/api/chat"
MODEL_NAME = "tinyllama"

def query_ollama(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        # Expecting: {"message": {"role": "assistant", "content": "..."}}
        return response.json()["message"]["content"].strip()

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error from Ollama: {e} | Response: {e.response.text}")
        return "Sorry, the model couldn't generate a response."

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return "An unexpected error occurred while querying the model."
