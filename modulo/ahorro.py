import streamlit as st
from modulo.db import run_query

def interfaz_ahorro():
    st.header("Resumen general de ahorros")
    try:
        datos = run_query("""
            SELECT 
                a.id_ahorro, 
                m.Nombre, 
                a.Monto_actual, 
                a.Fecha_de_actualización, 
                a.Saldo_min_inicial, 
                a.Total_de_ahorro,
                a.Retiro
            FROM ahorro a
            JOIN miembro m ON a.id_miembro = m.id_miembro
        """)
        
        if datos:
            st.dataframe(datos, use_container_width=True)

            # Cálculos agregados
            total_ahorro = sum([row["Total_de_ahorro"] or 0 for row in datos])
            total_retiro = sum([row["Retiro"] or 0 for row in datos])
            promedio_ahorro = total_ahorro / len(datos) if datos else 0

            st.subheader("Resumen de cálculos")
            st.metric("Total general de ahorro", f"${total_ahorro:,.2f}")
            st.metric("Total retirado", f"${total_retiro:,.2f}")
            st.metric("Promedio de ahorro por miembro", f"${promedio_ahorro:,.2f}")
        else:
            st.warning("No hay registros de ahorro disponibles.")
    except Exception as e:
        st.error(f"No se pudo cargar el resumen de ahorros: {e}")
