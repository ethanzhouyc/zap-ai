# startup script for the Streamlit app

import streamlit as st
from rag.generator import process_query
from rag.api_services import get_list_of_chat_model_names
from rag.config import DEFAULT_LLM_MODEL
import torch

torch.classes.__path__ = [] # suppress warnings which is a bug

st.title("🚀 ZAP Copilot")

st.sidebar.header("⚙️ Configuration")

LLM_MODELS = get_list_of_chat_model_names()

llm_model = st.sidebar.selectbox(
    "🤖 Select an LLM model",
    LLM_MODELS,
    index=LLM_MODELS.index(DEFAULT_LLM_MODEL),
    key="llm_model"
)

# Input box for user query
query = st.text_input("Ask a question:")

# Button to trigger response
if st.button("Submit"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving answer..."):
            answer = process_query(query, llm_model, web_mode=True)
        st.success("Done!")
        st.markdown(f"**Answer:**\n\n{answer}")