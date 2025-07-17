import os
from langchain_core.runnables import RunnableLambda
from pydantic.types import SecretStr
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Annotated
from pydantic import BaseModel, Field
from services.db_connection import db
from dotenv import load_dotenv

class State(TypedDict):
    question: str
    query: str
    result: str
    answer:str
            
load_dotenv()

GROQ_API_KEY= os.getenv("GROQ_API_KEY")
GROQ_MODEL=os.getenv("GROQ_MODEL")
print(GROQ_API_KEY,GROQ_MODEL )
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


def write_query(state: State):
    prompt = query_prompt_template.invoke(
        {
            "dialect":db.dialect,
            "top_k": 10,
            "table_info": db.get_table_info(),
            "input": state["question"], 
        }
    )

    llm_with_structured_output = llm.with_structured_output(OutputQueryModel)
    result_obj = llm_with_structured_output.invoke(prompt)
    print("\n\nthis is the result: ", result_obj)
    query = result_obj.query if hasattr(result_obj, "query") else result_obj.get("query", "") #type:ignore
    return {
        "question": state["question"],
        "query": query,
        "result": "",
        "answer": ""
    }

def execute_query(state: State):
    print(f"this is the query : {state['query']}")
    result = db.run(state["query"])
    return {
        "question": state["question"],
        "query": state["query"],
        "result": result,
        "answer": ""
    }


def generate_answer(state: State):
    prompt = (
        "Given the following user question, corresponding SQL query, "
        "and SQL result, answer the user question.\n\n"
        f'Question: {state["question"]}\n'
        f'SQL Query: {state["query"]}\n'
        f'SQL Result: {state["result"]}'
    )
    response = llm.invoke(prompt)
    return {
        "question": state["question"],
        "query": state["query"],
        "result": state["result"],
        "answer": response.content
    }



if __name__ == "__main__":  
    chain = RunnableLambda(write_query) | RunnableLambda(execute_query) | RunnableLambda(generate_answer)

    question = "List the top 5 most popular products in the store by number of sales."
    results = chain.invoke({
        "question": question,
        "query": "",
        "result": "",
        "answer": ""
    })
    print(results)