import streamlit as st
from datetime import date
from modulo.db import run_query

def interfaz_cierre():
    st.header("Cierre de Ciclo")

    try:
        utilidades = run_query("SELECT SUM(Monto_actual) AS fondo FROM ahorro")
        fondo_total = utilidades[0]["fondo"] or 0
    except Exception as e:
        st.error(f"No se pudo calcular el fondo total: {e}")
        return

    try:
        ahorros = run_query("SELECT id_miembro, Total_de_ahorro FROM ahorro")
        total_ahorro = sum([a["Total_de_ahorro"] or 0 for a in ahorros])
    except Exception as e:
        st.error(f"No se pudieron cargar los ahorros: {e}")
        return

    if total_ahorro == 0:
        st.warning("No hay ahorros registrados para distribuir.")
    else:
        total_retiro = 0
        miembros_afectados = 0

        for a in ahorros:
            proporcion = (a["Total_de_ahorro"] or 0) / total_ahorro
            retiro = round(proporcion * fondo_total, 2)
            total_retiro += retiro
            miembros_afectados += 1
            try:
                run_query("""
                    INSERT INTO cierre_de_ciclo (
                        id_miembro, `Saldo final`, Fecha,
                        `Fondo total del grupo`, `Monto a retirar`
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    a["id_miembro"],
                    a["Total_de_ahorro"] or 0,
                    date.today(),
                    fondo_total,
                    retiro
                ), fetch=False)
            except Exception as e:
                st.error(f"Error generando cierre para miembro {a['id_miembro']}: {e}")

        st.success("Acta de cierre generada")

        # Mostrar tabla de cierre
        try:
            cierre = run_query("""
                SELECT c.id_cierre, m.Nombre, c.`Saldo final`, c.Fecha,
                       c.`Fondo total del grupo`, c.`Monto a retirar`
                FROM cierre_de_ciclo c
                JOIN miembro m ON c.id_miembro = m.id_miembro
            """)
            st.dataframe(cierre)

            # Cálculos agregados
            st.subheader("Resumen del cierre")
            st.metric("Fondo total disponible", f"${fondo_total:,.2f}")
            st.metric("Total de ahorro acumulado", f"${total_ahorro:,.2f}")
            st.metric("Total distribuido en retiros", f"${total_retiro:,.2f}")
            st.metric("Miembros incluidos en el cierre", miembros_afectados)
            promedio_retiro = total_retiro / miembros_afectados if miembros_afectados else 0
            st.metric("Promedio de retiro por miembro", f"${promedio_retiro:,.2f}")

        except Exception as e:
            st.error(f"No se pudo cargar la tabla de cierre: {e}")
