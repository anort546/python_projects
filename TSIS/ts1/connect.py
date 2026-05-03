import psycopg2
from config import DB_CONFIG

def get_connection():
    # open a new connection using settings from config.py
    conn = psycopg2.connect(**DB_CONFIG)
    return conn
