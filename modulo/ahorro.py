# modulo/ahorro.py
import streamlit as st
import pandas as pd
from modulo.db import run_query, run_action
from modulo.auth import require_role, current_user

def ui():
    st.header("Módulo de ahorros")

    if require_role(["miembro"]):
        st.subheader("Registrar mi ahorro")
        user = current_user()
        id_miembro = user.get("id_miembro")
        monto_actual = st.number_input("Monto actual", min_value=0.01, step=0.01)
        retiro = st.number_input("Retiro", min_value=0.0, step=0.01)
        saldo_min_inicial = st.number_input("Saldo mínimo inicial", min_value=0.0, step=0.01)
        fecha_actualizacion = st.date_input("Fecha de actualización")
        if st.button("Guardar"):
            total = monto_actual - retiro
            run_action(
                "INSERT INTO ahorro (`Monto actual`,`Fecha de actualización`,id_miembro,`Retiro`,`Saldo_min_inicial`,`Total_de_ahorro`) VALUES (%s,%s,%s,%s,%s,%s)",
                (str(monto_actual), str(fecha_actualizacion), id_miembro, str(retiro), str(saldo_min_inicial), str(total))
            )
            st.success("Ahorro registrado.")

    st.subheader("Consulta de ahorros")
    filtro_id_miembro = st.text_input("ID miembro (opcional)")
    if st.button("Buscar"):
        if filtro_id_miembro.strip():
            rows = run_query("SELECT * FROM ahorro WHERE id_miembro=%s ORDER BY id_ahorro DESC", (int(filtro_id_miembro),))
        else:
            rows = run_query("SELECT * FROM ahorro ORDER BY id_ahorro DESC")
        st.dataframe(rows, use_container_width=True)

    if require_role(["promotora"]):
        st.subheader("Editar ahorro (promotora)")
        id_ahorro = st.number_input("ID ahorro a editar", min_value=1, step=1)
        nuevo_monto = st.number_input("Nuevo monto actual", min_value=0.0, step=0.01)
        nuevo_retiro = st.number_input("Nuevo retiro", min_value=0.0, step=0.01)
        nueva_fecha = st.text_input("Nueva fecha (YYYY-MM-DD)")
        if st.button("Actualizar"):
            total = nuevo_monto - nuevo_retiro
            run_action(
                "UPDATE ahorro SET `Monto actual`=%s, `Fecha de actualización`=%s, `Retiro`=%s, `Total_de_ahorro`=%s WHERE id_ahorro=%s",
                (str(nuevo_monto), nueva_fecha, str(nuevo_retiro), str(total), id_ahorro)
            )
            st.success("Ahorro actualizado.")
