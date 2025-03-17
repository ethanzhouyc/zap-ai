# The main script to build a RAG-based AI model based on fetched documentation data.

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# free embedding service for development
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.prompts import PromptTemplate

import parse_files
import api_services
from local_embeddings import download_local_embedding_if_not_exist

# get ZAP docs and split them into chunks
markdown_files = parse_files.get_test_zap_dev_docs()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splitted_documents = text_splitter.split_documents(markdown_files)
texts = [doc.page_content for doc in splitted_documents]
metadatas = [{"source": doc.metadata.get("source", "")} for doc in splitted_documents]

# =========================
# Embedding configuration
# =========================

EMBEDDING_MODEL = "BAAI/bge-small-en"
LOCAL_MODEL_DIR = "./local_models/bge-small-en"

# Free, local embedding model for testing and development
download_local_embedding_if_not_exist(EMBEDDING_MODEL, LOCAL_MODEL_DIR)
embedding_function = HuggingFaceEmbeddings(model_name=LOCAL_MODEL_DIR)

# Uncomment below to use the paid embedding service via Silabs API for production
# embedding_function = api_services.LiteLLMEmbeddings()

# =========================

# load vector stores from database
# if empty, create embeddings from documents and store them in vector stores
VECTOR_STORE_DIR = "./vectorstore"
vector_store = Chroma(
    persist_directory=VECTOR_STORE_DIR,
    embedding_function=embedding_function
)

stored_docs = vector_store.get(include=["documents"]).get("documents", [])
if len(stored_docs) == 0:
    print("Embedding and adding documents...")
    vector_store.add_texts(texts=texts, metadatas=metadatas)
    print(f"✅ Successfully added {len(texts)} documents to the vector store.")
else:
    print(f"✅ Loaded existing vector store from database with {len(stored_docs)} records.")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say that you don't know. Keep the answer concise, clear, and professional.
    Context: {context}
    Question: {question}
    Answer:
    """,
)

def retrieve(question):
    return vector_store.similarity_search(question)

def generate(question, context_docs):
    context = "\n\n".join(doc.page_content for doc in context_docs)
    prompt_text = prompt.invoke({
        "question": question,
        "context": context
    }).to_string()
    response = api_services.get_llm_response(prompt_text)
    return response.get("choices", [{}])[0].get("message", {}).get("content", "No answer generated.")


# =========================
# Test the RAG system
# =========================

test_queries = [
    "What types of notifications can ZAP generate?",
    "What do I need to do before running ZAP?",
    "What attributes are in the Level Control Cluster"
]

for test_query in test_queries:
    context_docs = retrieve(test_query)
    answer = generate(test_query, context_docs)

    print(f"\n🔍 Question: {test_query}")
    print(f"💡 Answer:\n{answer}")
    # print(f"\n📄 Retrieved Context:\n")
    # for i, doc in enumerate(context_docs, 1):
    #     print(f"--- Document {i} ---\n{doc.page_content[:500]}\nSource: {doc.metadata.get('source')}\n")
