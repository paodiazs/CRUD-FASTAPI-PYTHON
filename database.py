import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # 👈 carga el .env

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
