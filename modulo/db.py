import streamlit as st
import mysql.connector

def get_conn():
    return mysql.connector.connect(
        host=st.secrets["db"]["host"],
        port=st.secrets["db"]["port"],
        user=st.secrets["db"]["user"],
        password=st.secrets["db"]["password"],
        database=st.secrets["db"]["database"]
    )

def run_query(query, params=None):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows
