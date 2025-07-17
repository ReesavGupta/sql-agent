from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import pickle
import re

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = None  # Will be initialized after indexing

def index_or_load_vectorstore(db):
    global vectorstore
    if os.path.exists("faiss_index.pkl"):
        with open("faiss_index.pkl", "rb") as f:
            vectorstore = pickle.load(f)
        print("Loaded existing FAISS vector store.")
    else:
        table_info = db.get_table_info()
        table_docs = re.split(r'CREATE TABLE', table_info)
        table_docs = ["CREATE TABLE" + doc for doc in table_docs if doc.strip()]
        vectorstore = FAISS.from_texts(
            texts=table_docs,
            embedding=embeddings
        )
        with open("faiss_index.pkl", "wb") as f:
            pickle.dump(vectorstore, f)
        print(f"Indexed {len(table_docs)} tables into FAISS vector store.")
    return vectorstore

def get_relevant_schema(user_question, top_k=3):
    global vectorstore
    if vectorstore is None:
        raise ValueError("Vectorstore not initialized. Call index_or_load_vectorstore() first.")
    results = vectorstore.similarity_search(user_question, k=top_k)
    return "\n".join([doc.page_content for doc in results]) 