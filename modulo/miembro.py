import streamlit as st
from datetime import date
from modulo.db import run_query

def interfaz_miembro(user):
    st.header("Panel de Miembro")

    monto = st.number_input("¿Cuánto deseas ahorrar?", min_value=0.0, step=1.0)
    if st.button("Registrar ahorro"):
        run_query("""
            INSERT INTO ahorro (Monto_actual, Fecha_actualizacion, id_miembro, Resto, Saldo_min_inicial, Total_de_ahorro)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (monto, date.today(), user["id_miembro"], monto, 5.00, monto))
        st.success("Ahorro registrado correctamente")

    st.subheader("Mis ahorros")
    datos = run_query("SELECT * FROM ahorro WHERE id_miembro=%s", (user["id_miembro"],))
    st.dataframe(datos)

    st.subheader("Mi cierre de ciclo")
    cierre = run_query("SELECT * FROM cierre WHERE id_miembro=%s", (user["id_miembro"],))
    st.dataframe(cierre)
