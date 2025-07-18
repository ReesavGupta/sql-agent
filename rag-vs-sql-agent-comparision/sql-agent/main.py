"""
Minimal SQL Agent system for e-commerce customer support queries.
"""
import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic.types import SecretStr
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import time
load_dotenv()

# --- CONFIG ---
SQLITE_PATH = "rag-vs-sql-agent-comparision/e-commerce-data/olist.sqlite/olist.sqlite"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "gemma2-9b-it")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# Set your question here
QUESTION = "What is the total revenue generated from orders with a 5-star review?"

# --- LangChain LLM ---
llm = ChatGroq(api_key=SecretStr(str(GROQ_API_KEY)), model=GROQ_MODEL, temperature=0.2)

# --- SQLDatabase and Toolkit ---
db = SQLDatabase.from_uri(f"sqlite:///{SQLITE_PATH}")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()

# --- System Message ---
system_message = """
You are an agent designed to interact with a SQL database using the provided tools.
Given an input question, you must:
- Use ONLY the provided tools to interact with the database (do not invent new tools or functions).
- ALWAYS use the correct tool/function format for tool calls (no duplicate or nested parameters).
- To answer a question, first look at the tables in the database, then query the schema of relevant tables.
- When generating SQL, always double check the column and table names.
- If you get an error, correct your query and try again.
- DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP, etc.).
- After executing the query, return ONLY the final answer in clear natural language, summarizing the result for the user.
- Unless the user specifies a specific number of examples, always limit your query to at most 5 results.
- Never query for all columns from a table, only the relevant ones.
- If the question is about a count, sum, or aggregation, return the value and the relevant grouping (e.g., city, product, etc.).
- If you need to join tables, use the correct foreign key relationships.
- If you encounter a tool or function error, do not repeat the same call; instead, analyze and fix the issue.
"""

# --- Agent ---
agent_executor = create_react_agent(llm, tools, prompt=system_message)

def answer_sql_agent(question: str):
    results = agent_executor.invoke({"messages": [HumanMessage(content=question)]})
    final_answer = None
    for msg in results["messages"]:
        if hasattr(msg, "content"):
            final_answer = msg.content
    return final_answer

if __name__ == "__main__":
    print(f"\nSQL Agent answering: {QUESTION}\n")
    answer = answer_sql_agent(QUESTION)
    print("\nFinal Answer:\n" + (answer or "No answer produced."))

