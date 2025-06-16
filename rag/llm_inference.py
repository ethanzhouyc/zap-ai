from api_services import get_llm_response

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


def format_sources(sources):
    """Format source list for display in the final answer."""
    if not sources:
        return ""

    top = sources[0]
    others = sources[1:]

    source_info = f"📖 **Top Source:** {top}"
    if others:
        source_info += f"\n📄 **Other Sources:** {', '.join(others)}"
    return source_info


def generate(question, context_docs, sources):
    """Generates an answer using retrieved context from Qdrant."""
    context = "\n\n".join(context_docs)
    prompt = generatePrompt(question, context)

    # Call the LLM API to generate an answer
    response = get_llm_response(prompt, timeout=10)
    answer = response.get("choices", [{}])[0].get("message", {}).get("content", "No answer generated.")

    # Format the final response with the answer and source if the answer is not "I don't know."
    if answer.strip().lower() == "i don't know.":
        return f"💡 Answer: {answer}"
    else:
        source_info = format_sources(sources)
        return f"{source_info}\n\n💡 Answer: {answer}"
