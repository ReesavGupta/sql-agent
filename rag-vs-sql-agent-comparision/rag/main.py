"""
Minimal RAG system for e-commerce customer support queries.
"""
import json
from typing import List
import numpy as np

# Placeholder imports for vector store and LLM
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from pydantic.types import SecretStr
import os
import sqlite3
from dotenv import load_dotenv
load_dotenv()
import re
# --- CONFIG ---
VECTOR_STORE_PATH = "path/to/your/faiss_index"
CONTEXTS_PATH = "path/to/your/contexts.json"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Set this in your environment
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")  # Default to a common Groq model
MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 3

# Remove the check from here
# if not GROQ_API_KEY:
#     raise ValueError("GROQ_API_KEY environment variable not set.")

def load_vector_store():
    # Load contexts (if needed for reference)
    with open(CONTEXTS_PATH, "r", encoding="utf-8") as f:
        contexts = json.load(f)
    # Load FAISS index with LangChain
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    db = FAISS.load_local(VECTOR_STORE_PATH, embeddings)
    return db

def get_db_schema_info(sqlite_path: str, sample_rows: int = 0):
    """
    Connects to the SQLite database and extracts schema info (table names, columns, and optionally sample rows).
    """
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    schema_info = {}
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        # Get columns for each table
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [f"{col[1]} ({col[2]})" for col in cursor.fetchall()]
        table_info = {"columns": columns}
        # Optionally get sample rows
        if sample_rows > 0:
            cursor.execute(f"SELECT * FROM {table} LIMIT {sample_rows};")
            rows = cursor.fetchall()
            table_info["sample_rows"] = rows
        schema_info[table] = table_info
    conn.close()
    return schema_info

def format_table_schema(table_name, table_info):
    doc = f"Table: {table_name}\nColumns: {', '.join(table_info['columns'])}"
    if 'sample_rows' in table_info:
        doc += f"\nSample Rows:\n"
        for row in table_info['sample_rows']:
            doc += f"  {row}\n"
    return doc

def query_schema_vectorstore(query, k=2):
    """Load the schema vector store and retrieve relevant tables for a query."""
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vectorstore = FAISS.load_local(
        "rag-vs-sql-agent-comparision/rag/schema_faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    results = retriever.get_relevant_documents(query)
    return results

def answer_with_schema_rag(query: str, k: int = 2):
    """Retrieve relevant schema docs and use Groq LLM to answer the question."""
    # Retrieve relevant schema docs
    retrieved_docs = query_schema_vectorstore(query, k=k)
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    # Compose prompt
    prompt = f"""
You are a database assistant. Use the following database schema information to answer the user's question.

Schema Info:
{context}

Question: {query}
Answer:
"""
    # Use Groq LLM to answer
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable not set.")
    llm = ChatGroq(api_key=SecretStr(str(GROQ_API_KEY)), model=GROQ_MODEL, temperature=0.2)
    response = llm.invoke(prompt)
    answer = getattr(response, 'content', str(response))
    return answer.strip()

def run_sql_from_rag_output(output_path, db_path, results_path):
    # Read the SQL query from rag-output.txt
    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Extract the SQL query (between ```sql and ```) if present
    match = re.search(r"```sql\s*(.*?)```", content, re.DOTALL)
    if match:
        sql_query = match.group(1).strip()
    else:
        # Fallback: try to find a SELECT statement
        select_match = re.search(r"(SELECT[\s\S]+?;)", content, re.IGNORECASE)
        if select_match:
            sql_query = select_match.group(1).strip()
        else:
            print("No SQL query found in rag-output.txt")
            return
    print(f"Running SQL query:\n{sql_query}\n")
    # Run the query on the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    # Write results to rag-sql-results.txt
    with open(results_path, "w", encoding="utf-8") as f:
        f.write("\t".join(columns) + "\n")
        for row in rows:
            f.write("\t".join(str(x) for x in row) + "\n")
    print(f"Results written to {results_path}")

def main():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY environment variable not set.")
    # Load sample queries
    with open("../../data/sample_queries.json", "r", encoding="utf-8") as f:
        queries = json.load(f)
    # Load vector store and retriever
    db = load_vector_store()
    retriever = db.as_retriever(search_kwargs={"k": TOP_K})
    # Set up Groq LLM
    llm = ChatGroq(api_key=SecretStr(str(GROQ_API_KEY)), model=GROQ_MODEL, temperature=0.2)
    # Set up RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    # Run RAG for each query
    for q in queries:
        print(f"\nQuery: {q}")
        answer = qa_chain.run(q)
        print(f"Answer: {answer}")

# Set your question here
QUESTION =   "Which customers have not placed any orders?"

# Example usage: print schema info from the e-commerce SQLite DB
if __name__ == "__main__":
    # You can still run schema extraction and vector store creation if needed
    SQLITE_PATH = "rag-vs-sql-agent-comparision/e-commerce-data/olist.sqlite/olist.sqlite"
    schema = get_db_schema_info(SQLITE_PATH, sample_rows=2)
    print(json.dumps(schema, indent=2))

    # Step 2: Create a new vector store from schema info (split by table)
    docs = []
    for table, info in schema.items():
        doc = format_table_schema(table, info)
        docs.append(doc)

    # Create embeddings and FAISS vector store
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
    vectorstore = FAISS.from_texts(docs, embedding=embeddings)
    # Save the new vector store
    vectorstore.save_local("rag-vs-sql-agent-comparision/rag/schema_faiss_index")
    print("Schema vector store created and saved at rag-vs-sql-agent-comparision/rag/schema_faiss_index")

    # Run the RAG pipeline for a single question
    print(f"\nRAG answering: {QUESTION}\n")
    try:
        answer = answer_with_schema_rag(QUESTION, k=2)
        print(f"\nFinal Answer:\n{answer}")
        with open("rag-vs-sql-agent-comparision/rag/rag-output.txt", "a", encoding="utf-8") as f:
            f.write(f"Question: {QUESTION}\n")
            f.write(f"Answer: {answer}\n")
            f.write("\n" + "="*40 + "\n\n")

        # --- NEW: Extract SQL and execute immediately ---
        def extract_sql_query(answer_text):
            match = re.search(r"```sql\s*(.*?)```", answer_text, re.DOTALL)
            if match:
                return match.group(1).strip()
            select_match = re.search(r"(SELECT[\s\S]+?;)", answer_text, re.IGNORECASE)
            if select_match:
                return select_match.group(1).strip()
            return None

        def execute_and_save_sql(sql_query, db_path, results_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            try:
                cursor.execute(sql_query)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
            except Exception as e:
                rows = []
                columns = [f"SQL Error: {e}"]
            conn.close()
            with open(results_path, "w", encoding="utf-8") as f:
                f.write("\t".join(columns) + "\n")
                for row in rows:
                    f.write("\t".join(str(x) for x in row) + "\n")

        sql_query = extract_sql_query(answer)
        if sql_query:
            execute_and_save_sql(
                sql_query,
                SQLITE_PATH,
                "rag-vs-sql-agent-comparision/rag/rag-sql-results.txt"
            )
            # --- NEW: Append SQL results to rag-output.txt ---
            with open("rag-vs-sql-agent-comparision/rag/rag-sql-results.txt", "r", encoding="utf-8") as sql_f:
                sql_results = sql_f.read()
            with open("rag-vs-sql-agent-comparision/rag/rag-output.txt", "a", encoding="utf-8") as f:
                f.write("SQL Results (first 50 rows):\n")
                f.write(sql_results)
                f.write("\n" + "-"*40 + "\n\n")
            # --- END NEW ---
        else:
            print("No SQL query found in the LLM answer.")
        # --- END NEW ---
    except Exception as e:
        print(f"\nRAG Answer Error: {e}")
        with open("rag-vs-sql-agent-comparision/rag/rag-output.txt", "a", encoding="utf-8") as f:
            f.write(f"Error: {e}")
