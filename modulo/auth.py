import streamlit as st
from modulo.db import run_query

def login_form():
    st.sidebar.header("Acceso")
    usuario = st.sidebar.text_input("Usuario")
    contrasena = st.sidebar.text_input("Contraseña", type="password")

    if st.sidebar.button("Ingresar"):
        try:
            # Validar contra la tabla socios
            resultado = run_query(
                "SELECT * FROM socios WHERE Usuario=%s AND Contra=%s",
                (usuario, contrasena)
            )
            if resultado:
                user = resultado[0]
                # Guardar datos en la sesión
                st.session_state["user"] = {
                    "usuario": user["Usuario"],
                    "rol": user["rol"],
                    "id_miembro": user.get("id_miembro"),
                    "id_promotora": user.get("id_promotora"),
                    "id_socios": user["id_socios"]
                }
                st.success(f"Bienvenido {usuario}")
            else:
                st.error("Usuario o contraseña incorrectos")
        except Exception as e:
            st.error(f"Error en el login: {e}")

def current_user():
    """Devuelve el usuario actual logueado desde la sesión"""
    return st.session_state.get("user")
