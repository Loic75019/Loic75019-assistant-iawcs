# retriever/index_manager.py
import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class PDFRetriever:
    def __init__(self, file_path):
        self.file_path = file_path
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.vectordb = None

    def build_index(self, docs):
        self.vectordb = FAISS.from_documents(docs, self.embeddings)

    def get_context(self, query, k=4):
        return self.vectordb.similarity_search(query, k=k)
