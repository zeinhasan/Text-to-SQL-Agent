import os
from dotenv import load_dotenv
import google.generativeai as genai

# Pastikan .env di-root terbaca
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Konfigurasi Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_gemini_response(prompt: str, model="gemini-2.5-flash") -> str:
    try:
        model = genai.GenerativeModel(model)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return "Maaf, terjadi kesalahan saat memproses permintaan."
    