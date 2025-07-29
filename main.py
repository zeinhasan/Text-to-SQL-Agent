from fastapi import FastAPI
from pydantic import BaseModel
from utils.text2sql import generate_sql_from_question
from utils.db import get_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask(request: QuestionRequest):
    sql_query = generate_sql_from_question(request.question)

    try:
        engine = get_engine()
        with engine.connect() as connection:
            # Menggunakan text() untuk memastikan query dijalankan sebagai SQL
            result_proxy = connection.execute(text(sql_query))
            # Mengambil semua hasil dan mengubahnya menjadi list of dicts
            result = [dict(row._mapping) for row in result_proxy.fetchall()]
        
        return {"sql": sql_query, "result": result}
    except SQLAlchemyError as e:
        return {"sql": sql_query, "error": str(e)}
    except Exception as e:
        # Menangkap kesalahan umum lainnya
        return {"sql": sql_query, "error": f"Terjadi kesalahan yang tidak terduga: {str(e)}"}