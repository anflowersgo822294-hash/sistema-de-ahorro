import streamlit as st
from datetime import date
from modulo.db import run_query

def interfaz_miembro(user):
    st.header("Panel de Miembro")

    # Registrar ahorro
    monto = st.number_input("¿Cuánto deseas ahorrar?", min_value=0.0, step=1.0)
    if st.button("Registrar ahorro"):
        try:
            run_query("""
                INSERT INTO ahorro (
                    Monto_actual, Fecha_de_actualizacion, id_miembro, 
                    Resto, Saldo_min_inicial, Total_de_ahorro
                )
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                monto,
                date.today(),
                user.get("id_miembro"),
                monto,
                5.00,
                monto
            ), fetch=False)
            st.success("Ahorro registrado correctamente")
        except Exception as e:
            st.error(f"No se pudo registrar el ahorro: {e}")

    # Tabla de ahorros del miembro
    st.subheader("Mis ahorros")
    try:
        datos = run_query("""
            SELECT Monto_actual, Fecha_de_actualizacion, Total_de_ahorro, Resto, Saldo_min_inicial
            FROM ahorro
            WHERE id_miembro=%s
        """, (user.get("id_miembro"),))
        st.dataframe(datos)
    except Exception as e:
        st.error(f"No se pudieron cargar tus ahorros: {e}")

    # Tabla de cierre de ciclo del miembro
    st.subheader("Mi cierre de ciclo")
    try:
        cierre = run_query("""
            SELECT Saldo_final, Fecha, Fondo_total_grupo, Monto_a_retirar
            FROM cierre_de_ciclo
            WHERE id_miembro=%s
        """, (user.get("id_miembro"),))
        st.dataframe(cierre)
    except Exception as e:
        st.error(f"No se pudo cargar tu cierre de ciclo: {e}")
