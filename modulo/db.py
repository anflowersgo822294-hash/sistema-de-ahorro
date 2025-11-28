import os
import streamlit as st
import mysql.connector

def _get_db_config():
    """
    Obtiene la configuración de la base de datos.
    Primero intenta leer de st.secrets["db"], si no existe usa variables de entorno.
    """
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
        # Fallback a variables de entorno
        return {
            "host": os.getenv("DB_HOST"),
            "port": int(os.getenv("DB_PORT", "3306")),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "database": os.getenv("DB_NAME"),
        }

def get_conn():
    """
    Crea y devuelve una conexión a la base de datos MySQL.
    Lanza un error si falta alguna configuración.
    """
    cfg = _get_db_config()
    missing = [k for k, v in cfg.items() if not v]
    if missing:
        raise RuntimeError(
            f"Configuración de BD incompleta. Faltan: {', '.join(missing)}. "
            "Asegura .streamlit/secrets.toml con [db] o variables de entorno DB_*."
        )
    try:
        return mysql.connector.connect(
            host=cfg["host"],
            port=cfg["port"],
            user=cfg["user"],
            password=cfg["password"],
            database=cfg["database"]
        )
    except mysql.connector.Error as e:
        raise RuntimeError(f"Error de conexión a la BD: {e}")

def run_query(query, params=None, fetch=True):
    """
    Ejecuta una consulta SQL.
    - query: sentencia SQL
    - params: parámetros opcionales
    - fetch=True: devuelve resultados (SELECT)
    - fetch=False: solo ejecuta (INSERT, UPDATE, DELETE)
    """
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        rows = cursor.fetchall() if fetch else None
        conn.commit()
        return rows
    except mysql.connector.Error as e:
        raise RuntimeError(f"Error ejecutando consulta: {e}")
    finally:
        cursor.close()
        conn.close()
