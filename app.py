import streamlit as st
from modulo.auth import login_form, current_user
from modulo.miembro import interfaz_miembro
from modulo.promotora import interfaz_promotora
from modulo.ahorro import interfaz_ahorro
from modulo.cierre import interfaz_cierre

st.set_page_config(page_title="Sistema de Ahorro", layout="wide")

def main():
    login_form()
    user = current_user()

    if not user:
        st.info("Inicia sesión para continuar.")
        return

    # Panel por rol
    if user.get("rol") == "miembro":
        interfaz_miembro(user)
    elif user.get("rol") == "promotora":
        interfaz_promotora(user)
    else:
        st.error("Rol no reconocido. Verifica la tabla socios.")

    # Opciones comunes
    st.sidebar.subheader("Opciones")
    if st.sidebar.button("Ver Ahorros"):
        interfaz_ahorro()

    # Solo promotoras pueden ejecutar el cierre
    if user.get("rol") == "promotora" and st.sidebar.button("Cierre de Ciclo"):
        interfaz_cierre()

if __name__ == "__main__":
    main()
