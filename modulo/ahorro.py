import streamlit as st
from modulo.db import run_query

def interfaz_ahorro():
    st.header("Resumen general de ahorros")
    try:
        datos = run_query("""
            SELECT a.id_ahorro, m.Nombre, a.Monto_actual, a.Fecha_de_actualizacion, a.Resto, a.Saldo_min_inicial, a.Total_de_ahorro
            FROM ahorro a
            JOIN miembro m ON a.id_miembro = m.id_miembro
        """)
        st.dataframe(datos)
    except Exception as e:
        st.error(f"No se pudo cargar el resumen de ahorros: {e}")
