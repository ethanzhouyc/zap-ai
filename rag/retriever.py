# retrieve the most relevant documents from Qdrant vector store using vector search.

from rag.qdrant_db import client
from rag.embeddings import embed_text
from rag.parse_zap_docs import ZAP_DOC_COLLECTION_NAME
from rag.parse_matter_xmls import MATTER_XML_COLLECTION_NAME
import os


def query_collection(question, collection_name, limit):
    query_vector = embed_text(question)  # Convert question to embedding

    # Perform similarity search using `query_points()` with correct parameter
    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=limit,
        with_payload=True,
        with_vectors=True,
    ).points

    return [
        {
            "source": point.payload.get("source", "Unknown"),
            "text": point.payload.get("text", "No content"),
            "score": point.score,
            "collection": collection_name
        }
        for point in results
    ]


def filter_retrieved_docs(retrieved_docs, threshold=0.65, same_top_n=5):
    retrieved_docs.sort(key=lambda x: x["score"], reverse=True)
    
    # Get the collection of the top N results
    top_results = retrieved_docs[:same_top_n]
    top_collections = {res['collection'] for res in top_results}

    # If all top N are from the same collection, filter out the others
    if len(top_collections) == 1:
        dominant_collection = next(iter(top_collections))
        filtered = [res for res in retrieved_docs if res['collection'] == dominant_collection]
    else:
        filtered = retrieved_docs

    # Remove documents below similarity threshold
    filtered_results = [res for res in filtered if res['score'] >= threshold]

    return filtered_results


def retrieve(question):
    """Retrieve the most relevant documents from Qdrant using vector search."""
    zap_results = query_collection(question, ZAP_DOC_COLLECTION_NAME, limit=5)
    matter_results = query_collection(question, MATTER_XML_COLLECTION_NAME, limit=8)

    # Combine and sort by score descending
    all_results = zap_results + matter_results

    write_retrieval_logs(question, all_results)
    
    filtered = filter_retrieved_docs(all_results, threshold=0.65, same_top_n=5)

    # Extract unique sources from the filtered results
    sources = list(dict.fromkeys(res['source'] for res in filtered))

    retrieved_docs = [
        f"Source: {res['source']}\nText: {res['text']}" for res in filtered
    ]

    return retrieved_docs, sources


def write_retrieval_logs(question, retrieved_docs):
    log_file_name = "retrieval_log.txt"
    log_path = os.path.join(os.path.dirname(__file__), "log", log_file_name)
    retrieved_docs.sort(key=lambda x: x["score"], reverse=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"🔍 Question: {question}\n\n")
        for i, res in enumerate(retrieved_docs):
            f.write(f"[{i+1}] Collection: {res['collection']} | Source: {res['source']} | Score: {res['score']:.4f}\n")
            f.write("-------- Document Content --------\n")
            f.write(f"Source: {res['source']}\nText: {res['text']}\n")
            f.write("----------------------------------\n\n")