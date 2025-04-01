from qdrant_client import QdrantClient

VECTOR_STORE_DIR = "qdrant_data"
client = QdrantClient(path=VECTOR_STORE_DIR)