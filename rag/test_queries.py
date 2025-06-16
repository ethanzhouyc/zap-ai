# Test queries for the RAG system

from retriever import retrieve
from llm_inference import generate

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

def run_test_queries():
    print('Running test queries...')
    for test_query in test_queries:
        context_docs, _ = retrieve(test_query)
        answer = generate(test_query, context_docs, )
        print(f"\n🔍 Question: {test_query}")
        print(f"💡 Answer:\n{answer}\n")