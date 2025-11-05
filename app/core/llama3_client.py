import os
import httpx

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://ollama:11434")
LLAMA3_MODEL = os.environ.get("LLAMA3_MODEL", "llama3")

async def run_llama3(prompt, task="summarize", max_tokens=200):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OLLAMA_BASE_URL}/v1/chat/completions",
            json={
                "model": LLAMA3_MODEL,
                "messages": [
                    {"role": "system", "content": f"Task: {task}"},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "stream": False
            },
            timeout=600
        )
        response.raise_for_status()
        content = response.json()
        return content['choices'][0]['message']['content']

import requests

def generate_summary_with_ollama(prompt: str, model: str = "llama3") -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt}
        )
        print(response)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return(e)