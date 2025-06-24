# zap-ai
A Retrieval-Augmented Generation (RAG)-based AI assistant for ZAP, enabling users to ask detailed questions on ZAP documentation and Matter XMLs.

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
Then open `.env` and replace the placeholder with your own Silabs LiteLLM API key.

### 4. Run the Application

You can run the application in two ways:
- **From the command line:**
  ```
  python run-cli.py
  ```
- **From the Web UI:**
  ```
  streamlit run app.py
  ```