# Sets API keys.

import requests
import os
from langchain_core.embeddings import Embeddings
from dotenv import load_dotenv
import rag.config

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Error: OPENAI_API_KEY is not set. Please configure it in your environment.")

base_url = "https://genai-search-prod-litellm.silabs.net"
models_url = f"{base_url}/models"
model_details_url = f"{base_url}/model_group/info"
embedding_url = f"{base_url}/embeddings"
chat_url = f"{base_url}/chat/completions"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {OPENAI_API_KEY}",
    "content-type": "application/json"
}


def get_models_info():
    response = requests.get(models_url, headers=headers)
    return response.json().get("data", [])


def get_model_details():
    response = requests.get(model_details_url, headers=headers)
    return response.json().get("data", [])


def get_list_of_chat_model_names():
    model_details = get_model_details()
    return [model["model_group"] for model in model_details if model["mode"] == "chat"]


def get_llm_response(message, timeout=10):
    data = {
        "model": rag.config.LLM_MODEL,
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    input_length = len(message)
    large_input_threshold = 10000

    hasException = False
    answer = ""

    try: 
        response = requests.post(chat_url, json=data, headers=headers, timeout=timeout)

        if response.status_code == 200:
            answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        elif response.status_code == 429:
            hasException = True
            answer = "❌ API Rate limit hit. Try again in 24h."
        else:
            hasException = True
            answer = f"Failed to get llm response: {response.status_code} - {response.text}"
    except requests.exceptions.Timeout:
        hasException = True
        messages = ["❌ Connection to the LLM timed out."]
        if input_length > large_input_threshold:
            messages.append("💡 Timeout could be due to either network issues or large input size.")
            messages.append("❗️ Input message size is too large. Try using an LLM with a larger context window.")
        messages.append("🔌 Connection issues may cause timeouts. Please ensure you're connected to the Silabs VPN.")

        answer = "  \n".join(messages)
    
    return answer, hasException


def get_embeddings(texts):
    data = {
        "model": rag.config.EMBEDDING_MODEL,
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


class LiteLLMEmbeddings(Embeddings):
    def embed_documents(self, texts):
        return get_embeddings(texts)

    def embed_query(self, text):
        return get_embeddings([text])[0]