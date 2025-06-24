# Fetch and parse ZAP document files.

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import requests
import os

zap_dev_doc_dir = "https://api.github.com/repos/project-chip/zap/contents/docs"
zap_user_doc_directory = "./data-sources/zap-user-docs"

ZAP_DOC_COLLECTION_NAME = "zap_docs"

def get_markdown_files_from_url(repo_url):
  '''Fetch the contents of all markdown files under a given Github repo URL.'''
  headers = {"Accept": "application/vnd.github.v3+json"}
  response = requests.get(repo_url, headers=headers)
  
  if response.status_code == 200:
    files = response.json()
    md_files = [file for file in files if file["name"].endswith(".md")]
    documents = []
    
    for md_file in md_files:
      file_url = md_file["download_url"]
      file_response = requests.get(file_url)
      if file_response.status_code == 200:
        doc = Document(
          page_content=file_response.text,
          metadata={"source": md_file["name"], "url": file_url}
        )
        documents.append(doc)
      else:
        print(f"Failed to fetch file content for {md_file['name']}: {file_response.status_code}")
    
    return documents
  else:
    print(f"Failed to fetch files: {response.status_code}")
    return []


def get_zap_dev_docs():
    return get_markdown_files_from_url(zap_dev_doc_dir)


def get_zap_user_docs():
    documents = []
    for filename in os.listdir(zap_user_doc_directory):
        if filename.endswith(".md"):
            file_path = os.path.join(zap_user_doc_directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                doc = Document(
                    page_content=content,
                    metadata={"source": filename, "path": file_path}
                )
                documents.append(doc)
    
    return documents


def load_and_split_zap_docs():
    """Fetch and split ZAP documentation into chunks."""
    # get ZAP docs and split them into chunks
    zap_user_docs = get_zap_user_docs()
    zap_dev_docs = get_zap_dev_docs()
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

    print(f"✅ Successfully split ZAP documents into {len(textData)} chunks!")
    return texts, textData