# Downloads and sets up local embedding models.

from sentence_transformers import SentenceTransformer
from qdrant_client.models import Distance, VectorParams, PointStruct
from huggingface_hub import snapshot_download
from requests.exceptions import SSLError
import os
import urllib3.exceptions

from rag.qdrant_db import client
from rag.parse_zap_docs import load_and_split_zap_docs, ZAP_DOC_COLLECTION_NAME
from rag.parse_matter_xmls import load_and_split_matter_xmls, MATTER_XML_COLLECTION_NAME


EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
LOCAL_MODEL_DIR = "./local_models/bge-large-en-v1.5"

embedding_model = None


def download_local_embedding_if_not_exist(model, local_dir):
    if not os.path.exists(local_dir) or not os.listdir(local_dir):
        print(f"📥 Downloading embedding model '{model}' to '{local_dir}'...")
        try:
            snapshot_download(
                repo_id=model,
                local_dir=local_dir,
                local_dir_use_symlinks=False
            )
            print("✅ Embedding model download complete.")
        except (SSLError, urllib3.exceptions.SSLError) as e:
            print("❌ Failed to download model due to SSL certificate issue.")
            print("🔒 This may be caused by your VPN or network security (e.g., Silabs VPN).")
            print("👉 Try disconnecting from the VPN.")
            print("🚫 Exiting program.")
            exit(1)
    else:
        print(f"✅ Embedding model already downloaded at '{local_dir}'.")


def initialize_embedding_model():
    global embedding_model

    # to use Silabs LiteLLM embeddings, uncomment the following line and update related function calls
    # embedding_model = api_services.LiteLLMEmbeddings()

    if embedding_model is None:
        download_local_embedding_if_not_exist(EMBEDDING_MODEL, LOCAL_MODEL_DIR)
        embedding_model = SentenceTransformer(LOCAL_MODEL_DIR)


def create_and_store_embeddings(collection_name, parse_docs_fn):
    initialize_embedding_model()
    embedding_dim = embedding_model.get_sentence_embedding_dimension()

    embedding_exists = False

    # Check if the collection and embedding data exist
    if client.collection_exists(collection_name):
        count_result = client.count(collection_name=collection_name, exact=True)
        if count_result.count > 0:
            embedding_exists = True
    else:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE)
        )

    if not embedding_exists:
        print("🔄 Preparing documents for embedding...")
        texts, textData = parse_docs_fn()

        # 🔍 Write chunks to log/text-chunks.txt
        log_path = os.path.join(os.path.dirname(__file__), "log", "text-chunks.txt")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            for i, text in enumerate(texts):
                f.write(f"[{i+1}]\n{text}\n\n")

        print("🧠 Generating embeddings for the documents...")
        embeddings = embedding_model.encode(texts).tolist()

        print("📦 Preparing data points for Qdrant...")
        points = [
            PointStruct(id=i, vector=embeddings[i], payload=textData[i])
            for i in range(len(textData))
        ]

        print("🚀 Inserting data points into Qdrant...")
        client.upsert(collection_name=collection_name, points=points)
        print(f"✅ Successfully added {len(texts)} documents to Qdrant!")
    else:
        print(f"✅ Vector store '{collection_name}' already exists. Skipping embedding process.")


def embed_documents():
    create_and_store_embeddings(ZAP_DOC_COLLECTION_NAME, load_and_split_zap_docs)
    create_and_store_embeddings(MATTER_XML_COLLECTION_NAME, load_and_split_matter_xmls)


def embed_text(text):
    initialize_embedding_model()
    return embedding_model.encode(text)