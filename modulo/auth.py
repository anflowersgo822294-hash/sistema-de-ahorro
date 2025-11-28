# modulo/auth.py
import streamlit as st
from modulo.db import run_query

# Supone una tabla 'usuarios' con columnas: id, username, password_hash, rol ('miembro'|'promotora'), id_miembro?, id_promotora?
# Adapta a tu realidad si ya tienes otra forma de login.

def login_form():
    st.sidebar.header("Acceso")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        # Ejemplo simple sin hash (usa hash en producción)
        rows = run_query(
            "SELECT * FROM usuarios WHERE username=%s AND password_hash=%s",
            (username, password)
        )
        if rows:
            user = rows[0]
            st.session_state["auth"] = {
                "username": user["username"],
                "rol": user["rol"],
                "id_miembro": user.get("id_miembro"),
                "id_promotora": user.get("id_promotora")
            }
            st.sidebar.success(f"Bienvenida/o, {user['username']}")
        else:
            st.sidebar.error("Usuario o contraseña incorrectos")

def require_role(roles):
    auth = st.session_state.get("auth")
    return auth and auth.get("rol") in roles

def current_user():
    return st.session_state.get("auth")
