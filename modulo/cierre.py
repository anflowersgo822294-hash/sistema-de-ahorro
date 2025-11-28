import streamlit as st
from datetime import date
from modulo.db import run_query

def interfaz_cierre():
    st.header("Cierre de Ciclo")

    # Fondo total del grupo (ejemplo: suma de Monto_actual)
    try:
        utilidades = run_query("SELECT SUM(Monto_actual) AS fondo FROM ahorro")
        fondo_total = utilidades[0]["fondo"] or 0
    except Exception as e:
        st.error(f"No se pudo calcular el fondo total: {e}")
        return

    # Ahorros individuales para distribución proporcional
    try:
        ahorros = run_query("SELECT id_miembro, Total_de_ahorro FROM ahorro")
        total_ahorro = sum([a["Total_de_ahorro"] or 0 for a in ahorros])
    except Exception as e:
        st.error(f"No se pudieron cargar los ahorros: {e}")
        return

    st.subheader("Distribución proporcional")
    if total_ahorro == 0:
        st.warning("No hay ahorros registrados para distribuir.")
    else:
        for a in ahorros:
            proporcion = (a["Total_de_ahorro"] or 0) / total_ahorro
            retiro = round(proporcion * fondo_total, 2)
            try:
                run_query("""
                    INSERT INTO cierre (id_miembro, Saldo_final, Fecha, Fondo_total_grupo, Monto_a_retirar)
                    VALUES (%s, %s, %s, %s, %s)
                """, (a["id_miembro"], a["Total_de_ahorro"] or 0, date.today(), fondo_total, retiro), fetch=False)
            except Exception as e:
                st.error(f"Error generando cierre para miembro {a['id_miembro']}: {e}")

        st.success("Acta de cierre generada")

    # Mostrar tabla de cierre
    try:
        cierre = run_query("""
            SELECT c.id_cierre, m.Nombre, c.Saldo_final, c.Fecha, c.Fondo_total_grupo, c.Monto_a_retirar
            FROM cierre c
            JOIN miembro m ON c.id_miembro = m.id_miembro
        """)
        st.dataframe(cierre)
    except Exception as e:
        st.error(f"No se pudo cargar la tabla de cierre: {e}")
