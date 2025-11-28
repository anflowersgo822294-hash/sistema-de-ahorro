import streamlit as st
from modulo.db import run_query
from modulo.auth import require_role

def ui():
    st.header("Módulo de grupos")

    # Mostrar todos los grupos
    try:
        grupos = run_query("SELECT * FROM grupo ORDER BY id_grupo DESC")
        st.dataframe(grupos, use_container_width=True)
    except Exception as e:
        st.error(f"No se pudieron cargar los grupos: {e}")

    # Solo las promotoras pueden crear/editar grupos
    if require_role(["promotora"]):
        st.subheader("Crear grupo")

        id_promotora = st.number_input("ID promotora", min_value=1, step=1)
        nombre = st.text_input("Nombre del grupo")
        fecha_inicial = st.date_input("Fecha inicial")  # más seguro que text_input

        if st.button("Crear grupo"):
            try:
                run_query("""
                    INSERT INTO grupo (id_promotora, Nombre, `Fecha inicial`, id_cierre, id_prestamo)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_promotora, nombre, fecha_inicial, 0, 0), fetch=False)
                st.success("Grupo creado correctamente.")
            except Exception as e:
                st.error(f"Error creando grupo: {e}")
