import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()

def get_engine():
    """
    Membuat dan mengembalikan SQLAlchemy engine berdasarkan variabel lingkungan.
    """
    db_system = os.getenv("DB_SYSTEM", "mysql").lower()
    
    if db_system == "mysql":
        db_uri = (
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}"
        )
    elif db_system == "pgsql":
        db_uri = (
            f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"
        )
    elif db_system == "mssql":
        db_uri = (
            f"mssql+pyodbc://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '1433')}/{os.getenv('DB_NAME')}"
            f"?driver=ODBC+Driver+17+for+SQL+Server"
        )
    elif db_system == "bigquery":
        # Untuk BigQuery, kita menggunakan path ke file kredensial JSON
        # Pastikan GOOGLE_APPLICATION_CREDENTIALS diatur di lingkungan Anda
        project_id = os.getenv("BQ_PROJECT_ID")
        dataset_id = os.getenv("BQ_DATASET_ID")
        db_uri = f"bigquery://{project_id}/{dataset_id}"
    else:
        raise ValueError(f"Sistem database '{db_system}' tidak didukung.")

    return create_engine(db_uri)

def get_schema_description():
    """
    Menghasilkan deskripsi skema untuk database yang dikonfigurasi.
    """
    engine = get_engine()
    inspector = inspect(engine)
    schema = ""
    
    # Dapatkan nama-nama tabel
    tables = inspector.get_table_names()
    
    for table_name in tables:
        schema += f"\nTable `{table_name}`:\n"
        columns = inspector.get_columns(table_name)
        for column in columns:
            # Menggunakan repr(column['type']) untuk mendapatkan representasi string dari tipe data
            schema += f" - {column['name']} ({repr(column['type'])})\n"
            
    return schema