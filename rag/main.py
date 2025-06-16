# The main script to build a RAG-based AI model based on fetched documentation data.

from embeddings import embed_documents
from retriever import retrieve
from llm_inference import generate
from test_queries import run_test_queries


def interactive_loop():
    """Run the interactive Q&A loop."""
    while True:
        user_question = input("🔍 Enter your question (or type 'exit' to quit): \n")
        if user_question.lower() == 'exit':
            break

        if user_question.lower() == 'test':
            run_test_queries()
            continue

        context_docs, sources = retrieve(user_question)
        answer = generate(user_question, context_docs, sources)

        print(f"\n\n{answer}\n\n")


def main():
    """Main entry point for the RAG-based AI system."""
    embed_documents()
    interactive_loop()


if __name__ == "__main__":
    main()
