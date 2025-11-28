import streamlit as st
from modulo.login import login   # 👈 importa la función login

def main():
    st.set_page_config(page_title="Sistema de Ahorro", layout="centered")
    login()   # ahora sí existe

if __name__ == "__main__":
    main()

    
