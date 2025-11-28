import streamlit as st
from modulo.auth import login_form, current_user, require_role
from modulo import miembro, promotora, grupo, ahorro, cierre_ciclo
from modulo.db import get_conn, run_query
def main():
    st.set_page_config(page_title="Sistema de Ahorro", layout="wide")

    # Mostrar formulario de login
    login_form()

    # Verificar si el usuario está autenticado
    user = current_user()
    if not user:
        st.info("Inicia sesión para acceder a los módulos.")
        return

    rol = user["rol"]
    st.sidebar.markdown(f"**Rol:** {rol.capitalize()}")

    # Menú dinámico según rol
    if rol == "miembro":
        menu = st.sidebar.radio("Menú", ["Miembro", "Ahorro", "Grupos (solo lectura)"])
        if menu == "Miembro":
            miembro.ui()
        elif menu == "Ahorro":
            ahorro.ui()
        elif menu == "Grupos (solo lectura)":
            grupo.ui()

    elif rol == "promotora":
        menu = st.sidebar.radio("Menú", ["Promotora", "Grupos", "Ahorro", "Cierre de ciclo"])
        if menu == "Promotora":
            promotora.ui()
        elif menu == "Grupos":
            grupo.ui()
        elif menu == "Ahorro":
            ahorro.ui()
        elif menu == "Cierre de ciclo":
            cierre_ciclo.ui()

if __name__ == "__main__":
    main()

    
