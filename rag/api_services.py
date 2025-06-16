# Sets API keys.

import requests
import os
from langchain_core.embeddings import Embeddings
from dotenv import load_dotenv

load_dotenv()

# Set the LLM and embedding models here
# LLM_MODEL = "llama3.1:8b"
LLM_MODEL = "gpt-4o"
# LLM_MODEL = "gemma3:27b"
EMBEDDING_MODEL = "text-embedding-3-large"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY is not set. Please configure it in your environment.")

models_url = "https://genai-search-prod-litellm.silabs.net/models"
embedding_url = "https://genai-search-prod-litellm.silabs.net/embeddings"
chat_url = "https://genai-search-prod-litellm.silabs.net/chat/completions"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {OPENAI_API_KEY}",
    "content-type": "application/json"
}

def get_models():
    response = requests.get(models_url, headers=headers)
    return response.json()

def get_llm_response(message, timeout=10):
    data = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    try: 
        response = requests.post(chat_url, json=data, headers=headers, timeout=timeout)

        if response.status_code == 429:
            raise Exception("Rate limit hit. Try again in 24h.")
        elif response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get llm response: {response.status_code} - {response.text}")
    except requests.exceptions.Timeout:
        print("❌ Connection to the LLM timed out.")
        print("👉 Please connect to the Silabs VPN and try again.")
        print("🚫 Exiting program.")
        exit(1)

def get_embeddings(texts):
    data = {
        "model": EMBEDDING_MODEL,
        "input": texts
    }
    response = requests.post(embedding_url, json=data, headers=headers)
    
    if response.status_code == 429:
        raise Exception("Rate limit hit. Try again in 24h.")
    elif response.status_code == 200:
        embeddings = response.json().get("data")
        return [item["embedding"] for item in embeddings]
    else:
        raise Exception(f"Failed to get embeddings: {response.status_code} - {response.text}")


def get_models_info():
    cost_api_url = "https://genai-search-prod-litellm.silabs.net/model_group/info"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {OPENAI_API_KEY}"
    }

    response = requests.get(cost_api_url, headers=headers)
    return response.json()

class LiteLLMEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return get_embeddings(texts)

    def embed_query(self, text):
        return get_embeddings([text])[0]

# code for testing API services
# print(api_services.get_models())
# print(api_services.get_embeddings(["What is the purpose of life?", "What is the meaning of life?"]))
# print(api_services.get_model_response("What is the purpose of life?"))
# print(api_services.get_models_info())