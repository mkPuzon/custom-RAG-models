'''test_db_conn.py

A script to test if a psql database 1) exists 2) has expected tabels and 3) has expected data.

Dec 2025
'''
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text

load_dotenv() # loads credentials from .env
DB_URL = os.getenv("DATABASE_URL")

def test_db_connection():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            print(f"[Successs] Connected to the database.")
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            if not tables:
                print(f"[WARNING] Database contains no tables.")
                return
            
            print(f"\n{'Table Name':<20} | {'Row Count':<10}")
            print("-" * 35)
            for table in tables:
                count_query = text(f"SELECT COUNT(*) FROM {table}")
                result = conn.execute(count_query).scalar()
                print(f"{table:<20} | {result:<10}")
    except Exception as e:
        print(f"[Error] Connection failed. Error details: {e}")


if __name__ == "__main__":
    test_db_connection()