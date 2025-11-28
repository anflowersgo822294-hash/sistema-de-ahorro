import streamlit as st
from datetime import date
from modulo.db import run_query

def interfaz_cierre():
    st.header("Cierre de Ciclo")

    utilidades = run_query("SELECT SUM(Monto_actual) AS fondo FROM ahorro")
    fondo_total = utilidades[0]["fondo"]

    ahorros = run_query("SELECT id_miembro, Total_de_ahorro FROM ahorro")
    total_ahorro = sum([a["Total_de_ahorro"] for a in ahorros])

    st.subheader("Distribución proporcional")
    for a in ahorros:
        proporcion = a["Total_de_ahorro"] / total_ahorro if total_ahorro else 0
        retiro = round(proporcion * fondo_total, 2)
        run_query("""
            INSERT INTO cierre (id_miembro, Saldo_final, Fecha, Fondo_total_grupo, Monto_a_retirar)
            VALUES (%s, %s, %s, %s, %s)
        """, (a["id_miembro"], a["Total_de_ahorro"], date.today(), fondo_total, retiro))

    st.success("Acta de cierre generada")

    cierre = run_query("""
        SELECT c.id_cierre, m.Nombre, c.Saldo_final, c.Fecha, c.Fondo_total_grupo, c.Monto_a_retirar
        FROM cierre c
        JOIN miembro m ON c.id_miembro = m.id_miembro
    """)
    st.dataframe(cierre)
