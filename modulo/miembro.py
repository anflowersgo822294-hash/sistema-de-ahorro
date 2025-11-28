# modulo/miembro.py
import streamlit as st
from modulo.db import run_query, run_action
from modulo.auth import current_user, require_role

def ui():
    st.header("Módulo de miembro")
    if not require_role(["miembro"]):
        st.info("Acceso reservado a miembros.")
        return

    user = current_user()
    id_miembro = user.get("id_miembro")

    # Perfil y grupo
    datos = run_query("SELECT * FROM miembro WHERE id_miembro=%s", (id_miembro,))
    if not datos:
        st.error("No se encontró tu registro de miembro.")
        return
    m = datos[0]
    st.subheader("Mi perfil")
    st.write(f"Nombre: {m['Nombre']}")
    st.write(f"DUI: {m.get('DUI','')}")
    st.write(f"Teléfono: {m.get('Telefono','')}")
    st.write(f"Dirección: {m.get('Dirección','')}")
    st.write(f"Rol en grupo: {m.get('Rol_en_grupo','')}")
    id_grupo = m["id_grupo"]

    # Registrar ahorro propio
    st.subheader("Registrar ahorro")
    monto_actual = st.number_input("Monto actual", min_value=0.01, step=0.01)
    retiro = st.number_input("Retiro", min_value=0.0, step=0.01)
    saldo_min_inicial = st.number_input("Saldo mínimo inicial", min_value=0.0, step=0.01)
    fecha_actualizacion = st.date_input("Fecha de actualización")

    if st.button("Guardar ahorro"):
        total_de_ahorro = monto_actual - retiro
        # Tus columnas son VARCHAR; insertamos como texto
        run_action(
            "INSERT INTO ahorro (`Monto actual`,`Fecha de actualización`,id_miembro,`Retiro`,`Saldo_min_inicial`,`Total_de_ahorro`) VALUES (%s,%s,%s,%s,%s,%s)",
            (str(monto_actual), str(fecha_actualizacion), id_miembro, str(retiro), str(saldo_min_inicial), str(total_de_ahorro))
        )
        st.success("Ahorro registrado.")

    # Visualizar últimos ahorros propios
    st.subheader("Mis ahorros")
    ahorros = run_query("SELECT * FROM ahorro WHERE id_miembro=%s ORDER BY id_ahorro DESC LIMIT 10", (id_miembro,))
    st.dataframe(ahorros, use_container_width=True)

    # Visualizar cierre del ciclo (solo lectura)
    st.subheader("Cierre de ciclo de mi grupo")
    cierres = run_query("""
        SELECT cc.*
        FROM `cierre de ciclo` cc
        WHERE cc.id_miembro=%s
        ORDER BY cc.id_cierre DESC
        """, (id_miembro,))
    if cierres:
        st.dataframe(cierres, use_container_width=True)
    else:
        st.info("Aún no hay cierre de ciclo registrado para tu grupo.")
