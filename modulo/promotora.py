# modulo/promotora.py
import streamlit as st
import pandas as pd
from modulo.db import run_query, run_action
from modulo.auth import current_user, require_role

def ui():
    st.header("Módulo de promotora")
    if not require_role(["promotora"]):
        st.info("Acceso reservado a promotoras.")
        return

    user = current_user()
    id_promotora = user.get("id_promotora")

    # Datos de promotora
    p = run_query("SELECT * FROM promotora WHERE id_promotora=%s", (id_promotora,))
    if not p:
        st.error("No se encontró tu registro de promotora.")
        return
    promotora = p[0]
    st.write(f"Nombre: {promotora['Nombre']}")
    st.write(f"Distrito: {promotora.get('Distrito','')}")

    # Grupos bajo seguimiento (por id_promotora)
    st.subheader("Grupos bajo seguimiento")
    grupos = run_query("SELECT * FROM grupo WHERE id_promotora=%s", (id_promotora,))
    st.dataframe(grupos, use_container_width=True)

    # Selección de grupo para consolidación
    ids = [g["id_grupo"] for g in grupos]
    id_grupo = st.selectbox("Selecciona un grupo", ids) if ids else None

    if id_grupo:
        st.markdown("### Miembros del grupo")
        miembros = run_query("SELECT * FROM miembro WHERE id_grupo=%s", (id_grupo,))
        st.dataframe(miembros, use_container_width=True)

        st.markdown("### Ahorros del grupo")
        ahorros = run_query("""
            SELECT a.*
            FROM ahorro a
            JOIN miembro m ON m.id_miembro = a.id_miembro
            WHERE m.id_grupo=%s
        """, (id_grupo,))
        st.dataframe(ahorros, use_container_width=True)

        # Ediciones simples sobre datos de grupo (ejemplo: nombre y fecha inicial)
        st.markdown("### Editar datos del grupo")
        grow = run_query("SELECT * FROM grupo WHERE id_grupo=%s", (id_grupo,))[0]
        nuevo_nombre = st.text_input("Nombre del grupo", value=grow["Nombre"])
        nueva_fecha_inicial = st.text_input("Fecha inicial (YYYY-MM-DD)", value=grow["Fecha inicial"])
        if st.button("Guardar cambios de grupo"):
            run_action("UPDATE grupo SET `Nombre`=%s, `Fecha inicial`=%s WHERE id_grupo=%s",
                       (nuevo_nombre, nueva_fecha_inicial, id_grupo))
            st.success("Cambios guardados.")

        # Reporte consolidado y descarga
        st.markdown("### Consolidado y descarga")
        df_ahorros = pd.DataFrame(ahorros)
        total_grupo = 0.0
        if not df_ahorros.empty and "Total_de_ahorro" in df_ahorros.columns:
            # convertir texto a número
            df_ahorros["Total_de_ahorro_num"] = pd.to_numeric(df_ahorros["Total_de_ahorro"], errors="coerce").fillna(0.0)
            total_grupo = df_ahorros["Total_de_ahorro_num"].sum()
        st.write(f"Fondo total estimado del grupo: {total_grupo:.2f}")

        csv = df_ahorros.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar ahorros (CSV)", csv, file_name=f"ahorros_grupo_{id_grupo}.csv", mime="text/csv")
