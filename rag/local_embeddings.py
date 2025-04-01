# This script downloads and sets up local embedding models.

from sentence_transformers import SentenceTransformer
import os
from huggingface_hub import snapshot_download
from requests.exceptions import SSLError
import urllib3.exceptions

EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
LOCAL_MODEL_DIR = "./local_models/bge-large-en-v1.5"

def download_local_embedding_if_not_exist(model, local_dir):
    if not os.path.exists(local_dir) or not os.listdir(local_dir):
        print(f"📥 Downloading embedding model '{model}' to '{local_dir}'...")
        try:
            snapshot_download(
                repo_id=model,
                local_dir=local_dir,
                local_dir_use_symlinks=False
            )
            print("✅ Download complete.")
        except (SSLError, urllib3.exceptions.SSLError) as e:
            print("❌ Failed to download model due to SSL certificate issue.")
            print("🔒 This may be caused by your VPN or network security (e.g., Silabs VPN).")
            print("👉 Try disconnecting from the VPN.")
            print("🚫 Exiting program.")
            exit(1)
    else:
        print(f"✅ Embedding model already downloaded at '{local_dir}'.")

download_local_embedding_if_not_exist(EMBEDDING_MODEL, LOCAL_MODEL_DIR)

embedding_model = SentenceTransformer(LOCAL_MODEL_DIR)
embedding_dim = embedding_model.get_sentence_embedding_dimension()

# Uncomment below to use the paid embedding service via Silabs API for production
# embedding_function = api_services.LiteLLMEmbeddings()
