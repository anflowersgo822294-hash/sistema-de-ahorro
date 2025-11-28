import streamlit as st
from modulo.db import run_query

def interfaz_promotora(user):
    st.header("Panel de Promotora")

    st.subheader("Miembros supervisados")
    try:
        miembros = run_query("""
            SELECT m.* 
            FROM miembro m
            JOIN grupo g ON m.id_grupo = g.id_grupo
            WHERE g.Distrito = (SELECT Distrito FROM promotora WHERE id_promotora=%s)
        """, (user.get("id_promotora"),))
        st.dataframe(miembros)
    except Exception as e:
        st.error(f"No se pudieron cargar los miembros: {e}")

    st.subheader("Ahorros registrados")
    try:
        ahorros = run_query("""
            SELECT a.id_ahorro, m.Nombre, a.Monto_actual, a.Fecha_de_actualizacion, 
                   a.Resto, a.Saldo_min_inicial, a.Total_de_ahorro
            FROM ahorro a
            JOIN miembro m ON a.id_miembro = m.id_miembro
        """)
        st.dataframe(ahorros)
    except Exception as e:
        st.error(f"No se pudieron cargar los ahorros: {e}")

    st.subheader("Cierres de ciclo")
    try:
        cierres = run_query("""
            SELECT c.id_cierre, m.Nombre, c.Saldo_final, c.Fecha, 
                   c.Fondo_total_grupo, c.Monto_a_retirar
            FROM cierre_de_ciclo c
            JOIN miembro m ON c.id_miembro = m.id_miembro
        """)
        st.dataframe(cierres)
    except Exception as e:
        st.error(f"No se pudieron cargar los cierres: {e}")

    st.subheader("Descargar reporte")
    st.download_button("Descargar", "Reporte consolidado (demo)", file_name="reporte_consolidado.txt")
