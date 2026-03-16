from fastapi import FastAPI, Request
from pydantic import BaseModel
from sql_agent import generate_sql, validate_sql, execute_sql
import time

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def run_query(request: QueryRequest):

    sql = generate_sql(request.question)

    if not validate_sql(sql):
        return {"error": "Unsafe query blocked"}

    try:
        results, execution_time = execute_sql(sql)
        return {
            "generated_sql": sql,
            "execution_time": execution_time,
            "results": results
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = round(time.time() - start_time, 4)
    print(f"{request.method} {request.url} completed in {process_time}s")

    return response