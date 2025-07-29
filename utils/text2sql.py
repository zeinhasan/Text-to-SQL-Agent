from utils.db import get_schema_description
from utils.gemini import get_gemini_response
import re

def generate_sql_from_question(user_question: str) -> str:
    schema = get_schema_description()

    prompt = f"""
    Kamu adalah asisten SQL. Berdasarkan struktur database di bawah ini, buatkan SQL dari pertanyaan user.

    Schema:
    {schema}

    Pertanyaan:
    {user_question}

    Jawaban: hanya query SQL, tanpa ```sql atau blok markdown.
    """

    raw_sql = get_gemini_response(prompt)

    # Hapus ```sql atau blok markdown lain
    cleaned_sql = re.sub(r"```(?:sql)?|```", "", raw_sql).strip()
    return cleaned_sql
