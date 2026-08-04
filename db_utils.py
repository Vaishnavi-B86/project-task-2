import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

DB_PATH = "ecommerce.db"

def get_sqlalchemy_engine(db_path=DB_PATH):
    return create_engine(f"sqlite:///{db_path}")

def execute_parameterized_query(query_str, params=None, db_path=DB_PATH):
    """Safely executes a query with parameters to prevent SQL injection."""
    engine = get_sqlalchemy_engine(db_path)
    with engine.connect() as connection:
        df = pd.read_sql(text(query_str), connection, params=params)
    return df