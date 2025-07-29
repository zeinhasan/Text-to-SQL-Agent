# Gunakan image Python yang ringan
FROM python:3.11-slim

# Set environment variable agar tidak buffering
ENV PYTHONUNBUFFERED=1

# Buat folder kerja
WORKDIR /app

# Salin semua file ke container
COPY . /app

# Install dependency system
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose port FastAPI
EXPOSE 8000

# Jalankan aplikasi FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]