import streamlit as st
from modulo.auth import login_form, current_user
from modulo.miembro import interfaz_miembro
from modulo.promotora import interfaz_promotora
from modulo.ahorro import interfaz_ahorro
from modulo.cierre import interfaz_cierre

def main():
    login_form()
    user = current_user()
    if user:
        if user["rol"] == "miembro":
            interfaz_miembro(user)
        elif user["rol"] == "promotora":
            interfaz_promotora(user)

        st.sidebar.subheader("Opciones comunes")
        if st.sidebar.button("Ver Ahorros"):
            interfaz_ahorro()
        if user["rol"] == "promotora" and st.sidebar.button("Cierre de Ciclo"):
            interfaz_cierre()

if __name__ == "__main__":
    main()
