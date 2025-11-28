import streamlit as st

# Simulación de login básico con roles
USUARIOS = {
    "alex": {"password": "1234", "rol": "miembro", "id_miembro": 1},
    "maria": {"password": "abcd", "rol": "promotora", "id_promotora": 1},
}

def login():
    st.sidebar.header("Acceso")
    usuario = st.sidebar.text_input("Usuario")
    contrasena = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usuario in USUARIOS and USUARIOS[usuario]["password"] == contrasena:
            st.session_state["user"] = USUARIOS[usuario]
            st.success(f"Bienvenida {usuario}")
        else:
            st.error("Usuario o contraseña incorrectos")

def require_role(roles):
    """
    Verifica si el usuario tiene alguno de los roles permitidos.
    Ejemplo: require_role(["promotora"])
    """
    user = st.session_state.get("user")
    if not user:
        st.warning("Debes iniciar sesión.")
        return False
    return user["rol"] in roles
