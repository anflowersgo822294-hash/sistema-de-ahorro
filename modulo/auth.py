import streamlit as st
from modulo.db import run_query

def login_form():
    st.sidebar.header("Acceso")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")

    if st.sidebar.button("Ingresar"):
        try:
            user = validar_usuario(username, password)
        except Exception as e:
            st.error(f"No se pudo validar el usuario. Revisa la conexión a BD. Detalle: {e}")
            return

        if user:
            st.session_state["usuario"] = user
            st.success(f"Bienvenido {user['Usuario']}")
        else:
            st.error("Usuario o contraseña incorrectos")

def validar_usuario(username, password):
    rows = run_query(
        "SELECT * FROM socios WHERE Usuario=%s AND Contra=%s",
        (username, password)
    )
    return rows[0] if rows else None

def current_user():
    return st.session_state.get("usuario")
