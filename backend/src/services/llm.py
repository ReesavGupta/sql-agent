import os
from pydantic.types import SecretStr
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
if not GROQ_API_KEY or not GROQ_MODEL:
    raise ValueError("no groq api key or groq model")

llm = ChatGroq(api_key=SecretStr(GROQ_API_KEY), model=GROQ_MODEL, temperature=0.0)

system_message = """
Given an input question, create a syntactically correct {dialect} query to
run to help find the answer. Unless the user specifies in his question a
specific number of examples they wish to obtain, always limit your query to
at most {top_k} results. You can order the results by a relevant column to
return the most interesting examples in the database.

Never query for all the columns from a specific table, only ask for a the
few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema
description. Be careful to not query for columns that do not exist. Also,
pay attention to which column is in which table.

Only use the following tables:
{table_info}
"""

user_prompt = "Question: {input}"

query_prompt_template = ChatPromptTemplate([("system", system_message), ("user", user_prompt)])

class OutputQueryModel(BaseModel):
    query: str = Field(..., description="Syntactically valid SQL query.")

def summarize_schema_with_llm(table_ddls):
    prompt = (
        "Summarize the following SQL table definitions and their relationships in clear, concise natural language. "
        "Focus on what each table represents, its key columns, and how it relates to the others.\n\n"
        + "\n\n".join(table_ddls)
    )
    response = llm.invoke(prompt)
    return response.content 