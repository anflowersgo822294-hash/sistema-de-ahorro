import os
import streamlit as st
import mysql.connector

def _get_db_config():
    try:
        dbs = st.secrets["db"]
        return {
            "host": dbs.get("host"),
            "port": int(dbs.get("port", 3306)),
            "user": dbs.get("user"),
            "password": dbs.get("password"),
            "database": dbs.get("database"),
        }
    except Exception:
        return {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }

def get_conn():
    cfg = _get_db_config()
    return mysql.connector.connect(**cfg)

def run_query(query, params=None, fetch=True):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        rows = cursor.fetchall() if fetch else None
        conn.commit()
        return rows
    finally:
        cursor.close()
        conn.close()
