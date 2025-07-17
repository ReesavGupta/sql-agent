import re
from .llm import llm, query_prompt_template, OutputQueryModel, summarize_schema_with_llm
from .vectorstore import get_relevant_schema

schema_info_cache = None  # In-memory cache for schema info
query_result_cache = {}   # In-memory cache for query results

def get_schema_info(db):
    global schema_info_cache
    if schema_info_cache is None:
        schema_info_cache = db.get_table_info()
    return schema_info_cache

def write_query(state, db):
    # Use semantic search to get relevant schema
    relevant_schema = get_relevant_schema(state["question"])
    # Extract relevant table names
    relevant_table_names = set()
    for match in re.finditer(r'CREATE TABLE\s+([\w_]+)', relevant_schema, re.IGNORECASE):
        relevant_table_names.add(match.group(1))
    # Get all table docs from the cached schema info
    table_info = get_schema_info(db)
    table_docs = re.split(r'CREATE TABLE', table_info)
    table_docs = ["CREATE TABLE" + doc for doc in table_docs if doc.strip()]
    # Filter only relevant table docs
    relevant_table_docs = []
    for doc in table_docs:
        match = re.match(r'CREATE TABLE\s+([\w_]+)', doc, re.IGNORECASE)
        if match and match.group(1) in relevant_table_names:
            relevant_table_docs.append(doc)
    # Summarize relevant tables and relationships using LLM
    schema_summary = summarize_schema_with_llm(relevant_table_docs)
    # Calculate pagination
    page = state.get("page", 1) or 1
    page_size = state.get("page_size", 10) or 10
    offset = (page - 1) * page_size
    # Use the summary in the prompt, and add pagination instructions
    schema_summary_str = str(schema_summary) if not isinstance(schema_summary, str) else schema_summary
    prompt = query_prompt_template.invoke(
        {
            "dialect":db.dialect,
            "top_k": page_size,
            "table_info": schema_summary_str + f"\n\nReturn only {page_size} results starting from row {offset} (use LIMIT {page_size} OFFSET {offset} in your SQL query).",
            "input": state["question"], 
        }
    )

    llm_with_structured_output = llm.with_structured_output(OutputQueryModel)
    result_obj = llm_with_structured_output.invoke(prompt)
    query = result_obj.query if hasattr(result_obj, "query") else result_obj.get("query", "") #type:ignore
    # Post-process SQL to ensure LIMIT/OFFSET are present
    query = enforce_limit_offset(query, page_size, offset)
    return {
        "question": state["question"],
        "query": query,
        "result": "",
        "answer": "",
        "page": page,
        "page_size": page_size
    }

def enforce_limit_offset(query: str, page_size: int, offset: int) -> str:
    # Remove any trailing semicolon
    query = query.rstrip().rstrip(';')
    # Check if LIMIT is present
    limit_pattern = re.compile(r'\bLIMIT\b', re.IGNORECASE)
    offset_pattern = re.compile(r'\bOFFSET\b', re.IGNORECASE)
    if not limit_pattern.search(query):
        # Add LIMIT and OFFSET
        query += f" LIMIT {page_size} OFFSET {offset}"
    elif not offset_pattern.search(query):
        # Add OFFSET if LIMIT is present but OFFSET is not
        query += f" OFFSET {offset}"
    return query

def execute_query(state, db):
    print(f"this is the query : {state['query']}")
    # Use in-memory cache for query results
    cache_key = state["query"]
    if cache_key in query_result_cache:
        result = query_result_cache[cache_key]
        print("[CACHE HIT] Returning cached result.")
    else:
        result = db.run(state["query"])
        query_result_cache[cache_key] = result
        print("[CACHE MISS] Query executed and result cached.")
    return {
        "question": state["question"],
        "query": state["query"],
        "result": result,
        "answer": ""
    }

def generate_answer(state):
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