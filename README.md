# zap-ai
A Retrieval-Augmented Generation (RAG)-based AI assistant for ZAP, enabling users to ask detailed questions on ZAP documentation, template generation, and Matter specifications.

## Setup Instructions

### 1. Create and start a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Set Up the API Key in `.env`
Run the following command to create a `.env` file:
```
cp .env.example .env
```
Then open `.env` and replace the placeholder with your own API key.

### 4. Run the Application
```
python rag/main.py
```

### 5. First-Time Setup FAQ
- During setup, installing the local embedding model requires turning off the Silabs VPN.

- Model download and document indexing may take a while to complete.

- When asking questions, the app uses a Silabs-hosted LLM, so ensure you are connected to the Silabs VPN.