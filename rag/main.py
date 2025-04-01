# The main script to build a RAG-based AI model based on fetched documentation data.

from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import Distance, VectorParams, PointStruct

import parse_files
import api_services
from local_embeddings import embedding_model, embedding_dim
from set_qdrant_client import client


def prepare_documents():
    """Fetch and split ZAP documentation into chunks."""
    # get ZAP docs and split them into chunks
    zap_user_docs = parse_files.get_zap_user_docs()
    zap_dev_docs = parse_files.get_zap_dev_docs()
    zap_docs = zap_user_docs + zap_dev_docs

    print(f"📂 Number of files in zap_user_docs: {len(zap_user_docs)}")
    print(f"📂 Number of files in zap_dev_docs: {len(zap_dev_docs)}")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splitted_documents = text_splitter.split_documents(zap_docs)

    texts = [doc.page_content for doc in splitted_documents]

    textData = [
        {"source": doc.metadata.get("source", ""), "text": doc.page_content}
        for doc in splitted_documents
    ]

    print(f"✅ Successfully split documents into {len(textData)} chunks!")
    return texts, textData


def create_and_store_embeddings():
    # Check if the collection exists
    if not client.collection_exists("zap_docs"):
        client.create_collection(
            collection_name="zap_docs",
            vectors_config=VectorParams(size=embedding_dim, distance=Distance.COSINE)
        )

        print("🔄 Preparing documents for embedding...")
        texts, textData = prepare_documents()

        print("🧠 Generating embeddings for the documents...")
        embeddings = embedding_model.encode(texts).tolist()

        print("📦 Preparing data points for Qdrant...")
        points = [PointStruct(id=i, vector=embeddings[i], payload=textData[i]) for i in range(len(textData))]

        print("🚀 Inserting data points into Qdrant...")
        client.upsert(collection_name="zap_docs", points=points)
        print(f"✅ Successfully added {len(texts)} documents to Qdrant!")
    else:
        print("✅ Vector store already exists. Skipping embedding process.")


def generatePrompt(question, context):
    return f"""
        You are an intelligent AI assistant specializing in question-answering. 
        Use ONLY the retrieved context to answer the question. Do NOT make up information.

        **Instructions:**
        1. **Analyze** the retrieved context to determine if it directly answers the question.
        2. **If the context provides a direct answer, summarize it clearly and concisely.**
        3. **If the context does not contain a direct answer, respond with:** "I don't know." **Do NOT attempt to infer or provide unrelated information.**
        4. **Avoid speculation, additional explanations, or making connections not explicitly present in the context.**
        5. **Ensure clarity, accuracy, and conciseness.** Do not add unnecessary information.

        **Question:** {question}

        **Retrieved Context:** 
        {context}

        **Final Answer:**
    """


def retrieve(question):
    """Retrieve the most relevant documents from Qdrant using vector search."""
    query_vector = embedding_model.encode(question)  # Convert question to embedding

    # Perform similarity search using `query_points()` with correct parameter
    search_results = client.query_points(
        collection_name="zap_docs",
        query=query_vector,
        limit=5,
        with_payload=True,
        with_vectors=True,
    ).points

    # Extract text content from payload
    retrieved_docs = [
        f"Source: {point.payload.get('source', 'Unknown')}\n Text: {point.payload.get('text', 'No content')}"
        for point in search_results
    ]

    source_docs = [point.payload.get('source', 'Unknown') for point in search_results]
    docs_score = [point.score for point in search_results]

    # Uncomment below to print the retrieved documents and their scores
    # for source, score in zip(source_docs, docs_score):
    #     print(f"Source: {source}, Score: {score}")

    # Get the source of the document with the highest score
    top_answer_source = source_docs[docs_score.index(max(docs_score))]

    # if all docs have low similarity score, return empty list so the model will answer "I don't know."
    if all(score < 0.65 for score in docs_score):
        return [], ''

    return retrieved_docs, top_answer_source


def generate(question, context_docs, top_answer_source):
    """Generates an answer using retrieved context from Qdrant."""
    context = "\n\n".join(context_docs)
    prompt = generatePrompt(question, context)

    # Call the LLM API to generate an answer
    response = api_services.get_llm_response(prompt, timeout=10)
    answer = response.get("choices", [{}])[0].get("message", {}).get("content", "No answer generated.")

    # Format the final response with the answer and source if the answer is not "I don't know."
    if answer.strip().lower() == "i don't know.":
        final_response = f"💡 Answer: {answer}"
    else:
        final_response = f"📖 **Source:** {top_answer_source}\n\n💡 Answer: {answer}"

    return final_response


# # =========================
# # Test the RAG system
# # =========================

test_queries = [
    "What is the architecture of frontend in ZAP?",
    "How to run ZAP in VSCode?",
    "What attributes are in the Level Control Cluster in Matter?",
    "My unit tests failed. What are some common reasons for this?",
    "What ZAP functions is responsible for inserting cluster data from XML into database? Give me details of the functions if you find any",
    "What is matter device type feature page?",
    "How to use custom XMLs in ZAP?",
    "How to add a cluster extension in Matter? Give me an example.",
    "What is the difference between adding an attribute in Matter and Zigbee in custom XMLs?",
    "What is the purpose of life?"
]

# Comment out the line below to run predefined test queries
test_queries = []

create_and_store_embeddings()

for test_query in test_queries:
    context_docs, top_answer_source = retrieve(test_query)
    answer = generate(test_query, context_docs, )
    print(f"\n🔍 Question: {test_query}")
    print(f"💡 Answer:\n{answer}\n")

while True:
    user_question = input("🔍 Enter your question (or type 'exit' to quit): \n")
    if user_question.lower() == 'exit':
        break
    context_docs, top_answer_source = retrieve(user_question)
    answer = generate(user_question, context_docs, top_answer_source)

    print(f"\n\n{answer}\n\n")