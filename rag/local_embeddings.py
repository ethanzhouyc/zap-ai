# This script downloads and sets up local embedding models.

import os
from huggingface_hub import snapshot_download

def download_local_embedding_if_not_exist(model, local_dir):
    if not os.path.exists(local_dir) or not os.listdir(local_dir):
        print(f"📥 Downloading embedding model '{model}' to '{local_dir}'...")
        snapshot_download(
            repo_id=model,
            local_dir=local_dir,
            local_dir_use_symlinks=False
        )
        print("✅ Download complete.")
    else:
        print(f"✅ Embedding model already downloaded at '{local_dir}'.")
