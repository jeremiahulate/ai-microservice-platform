import requests

OLLAMA_URL = "http://ollama:11434/api/generate"
MODEL_NAME = "llama3.2:3b"

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are a helpful AI assistant. Answer the user's question using only the context below.

If the answer is not in the context, say:
"I could not find that information in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:
"""
    
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    data = response.json()

    return data.get("response", "").strip()
    