import streamlit as st
from modulo.db import run_query

def interfaz_ahorro():
    st.header("Resumen general de ahorros")
    datos = run_query("""
        SELECT a.id_ahorro, m.Nombre, a.Monto_actual, a.Fecha_actualizacion, a.Total_de_ahorro
        FROM ahorro a
        JOIN miembro m ON a.id_miembro = m.id_miembro
    """)
    st.dataframe(datos)
