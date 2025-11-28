# modulo/db.py
import mysql.connector
import streamlit as st

def get_conn():
    return mysql.connector.connect(
        host=st.secrets["db"]["host"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        database=st.secrets["db"]["database"]
    )

def run_query(query, params=None, dict_cursor=True):
    conn = get_conn()
    cursor = conn.cursor(dictionary=dict_cursor)
    cursor.execute(query, params or ())
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def run_action(query, params=None):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    cursor.close()
    conn.close()
