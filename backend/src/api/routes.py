from fastapi import APIRouter
from pydantic import BaseModel
from services.db_connection import db
from services.vectorstore import index_or_load_vectorstore
from services.query import write_query, execute_query, generate_answer

router = APIRouter()

class QueryRequest(BaseModel):
    question: str
    page: int = 1
    page_size: int = 10

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    # Ensure vectorstore is loaded
    index_or_load_vectorstore(db)
    # Run the pipeline
    state = {
        "question": request.question,
        "query": "",
        "result": "",
        "answer": "",
        "page": request.page,
        "page_size": request.page_size
    }
    state = write_query(state, db)
    state = execute_query(state, db)
    state = generate_answer(state)
    return state 