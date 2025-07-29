from fastapi import FastAPI
from pydantic import BaseModel
from utils.text2sql import generate_sql_from_question
from utils.db import get_connection

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask(request: QuestionRequest):
    sql = generate_sql_from_question(request.question)

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        return {"sql": sql, "result": result}
    except Exception as e:
        return {"sql": sql, "error": str(e)}
