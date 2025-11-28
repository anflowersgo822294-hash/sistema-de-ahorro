import streamlit as st
from modulo.db import run_query

def interfaz_promotora(user):
    st.header("Panel de Promotora")

    st.subheader("Miembros supervisados")
    miembros = run_query("""
        SELECT m.*
        FROM miembro m
        JOIN grupo g ON m.id_grupo = g.id_grupo
        WHERE g.Distrito = (SELECT Distrito FROM promotora WHERE id_promotora=%s)
    """, (user.get("id_promotora"),))
    st.dataframe(miembros)

    st.subheader("Ahorros registrados")
    ahorros = run_query("""
        SELECT a.id_ahorro, m.Nombre, a.Monto_actual, a.Fecha_de_actualización,
               a.Retiro, a.Saldo_min_inicial, a.Total_de_ahorro
        FROM ahorro a
        JOIN miembro m ON a.id_miembro = m.id_miembro
    """)
    st.dataframe(ahorros)

    st.subheader("Cierres de ciclo")
    cierres = run_query("""
        SELECT c.id_cierre, m.Nombre, c.`Saldo final`, c.Fecha,
               c.`Fondo total del grupo`, c.`Monto a retirar`
        FROM cierre_de_ciclo c
        JOIN miembro m ON c.id_miembro = m.id_miembro
    """)
    st.dataframe(cierres)
