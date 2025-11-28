import streamlit as st
from modulo.db import run_query

def interfaz_promotora(user):
    st.header("Panel de Promotora")

    st.subheader("Miembros supervisados")
    miembros = run_query("""
        SELECT m.* FROM miembro m
        JOIN grupo g ON m.id_grupo = g.id_grupo
        WHERE g.Distrito = (SELECT Distrito FROM promotora WHERE id_promotora=%s)
    """, (user["id_promotora"],))
    st.dataframe(miembros)

    st.subheader("Ahorros registrados")
    ahorros = run_query("""
        SELECT a.*, m.Nombre FROM ahorro a
        JOIN miembro m ON a.id_miembro = m.id_miembro
    """)
    st.dataframe(ahorros)

    st.subheader("Cierres de ciclo")
    cierres = run_query("""
        SELECT c.*, m.Nombre FROM cierre c
        JOIN miembro m ON c.id_miembro = m.id_miembro
    """)
    st.dataframe(cierres)

    st.subheader("Descargar reporte")
    st.download_button("Descargar", "Contenido del reporte", file_name="reporte_consolidado.txt")
