# modulo/grupo.py
import streamlit as st
from modulo.db import run_query, run_action
from modulo.auth import require_role

def ui():
    st.header("Módulo de grupos")
    # Acceso: ambas, pero edición solo promotora
    grupos = run_query("SELECT * FROM grupo ORDER BY id_grupo DESC")
    st.dataframe(grupos, use_container_width=True)

    if require_role(["promotora"]):
        st.subheader("Crear/editar grupo")
        id_promotora = st.number_input("ID promotora", min_value=1, step=1)
        nombre = st.text_input("Nombre")
        fecha_inicial = st.text_input("Fecha inicial (YYYY-MM-DD)")
        if st.button("Crear grupo"):
            run_action("INSERT INTO grupo (id_promotora, `Nombre`, `Fecha inicial`, id_cierre, id_prestamo) VALUES (%s,%s,%s,%s,%s)",
                       (id_promotora, nombre, fecha_inicial, 0, 0))
            st.success("Grupo creado.")
