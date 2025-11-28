import os
import streamlit as st
import mysql.connector

def _get_db_config():
    # Intentar leer de st.secrets
    try:
        dbs = st.secrets["db"]
        return {
            "host": dbs.get("host"),
            "port": int(dbs.get("port")),
            "user": dbs.get("user"),
            "password": dbs.get("password"),
            "database": dbs.get("database"),
        }
    except Exception:
        # Fallback a variables de entorno
        return {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }

def get_conn():
    cfg = _get_db_config()
    missing = [k for k, v in cfg.items() if not v]
    if missing:
        raise RuntimeError(
            f"Configuración de BD incompleta. Faltan: {', '.join(missing)}. "
            "Asegura .streamlit/secrets.toml con [db] o variables de entorno DB_*."
        )
    return mysql.connector.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"]
    )

def run_query(query, params=None, fetch=True):
    conn = get_conn()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall() if fetch else None
        conn.commit()
        return rows
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        conn.close()
