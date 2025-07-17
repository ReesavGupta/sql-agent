import os
from langchain_core.runnables import RunnableLambda
from typing_extensions import TypedDict
from services.db_connection import db
from services.llm import llm
from services.vectorstore import index_or_load_vectorstore
from services.query import write_query, execute_query, generate_answer

def main():
    index_or_load_vectorstore(db)
    chain = RunnableLambda(lambda state: write_query(state, db)) \
        | RunnableLambda(lambda state: execute_query(state, db)) \
        | RunnableLambda(generate_answer)

    question = "For each product category, what is the average product description length?"
    results = chain.invoke({
        "question": question,
        "query": "",
        "result": "",
        "answer": "",
        "page": 1,
        "page_size": 10
    })

    print("\n" + "="*60)
    print(" Final results ".center(60, "="))
    print("="*60)
    print(f"Question:\n{results['question']}\n")
    print(f"SQL Query:\n{results['query']}\n")
    print(f"SQL Result:\n{results['result']}\n")
    print(f"LLM Answer:\n{results['answer']}\n")
    print("="*60)

if __name__ == "__main__":
    main()