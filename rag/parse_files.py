# This script contains functions to fetch and parse external document files.

from langchain_core.documents import Document
import requests
import os

zap_dev_doc_url = "https://api.github.com/repos/project-chip/zap/contents/docs"
zap_user_doc_directory = "./zap-docs/zap-user-docs"

# fetch the contents of all markdown files under a given Github repo URL
def get_markdown_files_from_url(repo_url):
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
    return get_markdown_files_from_url(zap_dev_doc_url)

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
