# modulo/cierre_ciclo.py
import streamlit as st
import pandas as pd
from datetime import date
from modulo.db import run_query, run_action
from modulo.auth import require_role

def ui():
    st.header("Cierre de ciclo")
    # Solo promotora puede ejecutar el cierre
    if not require_role(["promotora"]):
        st.info("Acceso reservado a promotoras para ejecutar cierres.")
        return

    id_grupo = st.number_input("ID grupo a cerrar", min_value=1, step=1)
    fecha_cierre = st.date_input("Fecha de cierre", value=date.today())

    if st.button("Validar y cerrar ciclo"):
        # 1) Validar préstamos liquidados
        prestamos = run_query("SELECT * FROM prestamos WHERE id_grupo=%s", (id_grupo,))
        if not prestamos:
            st.warning("No hay préstamos registrados. Si no hubo préstamos, se puede cerrar.")
        else:
            pendientes = [p for p in prestamos if p.get("estado") != "liquidado"]
            if pendientes:
                st.error("El cierre no se habilita: hay préstamos pendientes de liquidación.")
                return

        # 2) Calcular utilidades (intereses + multas + otros ingresos)
        total_intereses = 0.0
        total_multas = 0.0
        for p in prestamos:
            total_intereses += float(p.get("interes", 0) or 0)
            total_multas += float(p.get("multa", 0) or 0)
        otros = run_query("SELECT * FROM ingresos_otros WHERE id_grupo=%s", (id_grupo,))
        total_otros = sum([float(x.get("monto", 0) or 0) for x in otros])
        utilidades = total_intereses + total_multas + total_otros

        # 3) Ahorro por miembro y ahorro total del grupo
        ahorros = run_query("""
            SELECT m.id_miembro, SUM(CAST(a.`Total_de_ahorro` AS DECIMAL(10,2))) AS ahorro_individual
            FROM miembro m
            LEFT JOIN ahorro a ON a.id_miembro = m.id_miembro
            WHERE m.id_grupo=%s
            GROUP BY m.id_miembro
        """, (id_grupo,))
        df = pd.DataFrame(ahorros)
        if df.empty:
            st.error("No hay ahorros registrados para el grupo.")
            return
        df["ahorro_individual"] = pd.to_numeric(df["ahorro_individual"], errors="coerce").fillna(0.0)
        ahorro_total = df["ahorro_individual"].sum()

        # 4) Distribución proporcional de utilidades según ahorro individual
        # proporción = ahorro_individual / ahorro_total
        df["proporcion"] = df["ahorro_individual"] / (ahorro_total if ahorro_total > 0 else 1)
        df["utilidad_asignada"] = df["proporcion"] * utilidades

        # 5) Fondo total del grupo (ahorro_total + utilidades)
        fondo_total = ahorro_total + utilidades

        # 6) Registrar cierre por miembro en la tabla 'cierre de ciclo'
        for _, row in df.iterrows():
            saldo_final = row["ahorro_individual"] + row["utilidad_asignada"]
            monto_a_retirar = saldo_final  # si el retiro en cierre es la liquidación completa
            run_action("""
                INSERT INTO `cierre de ciclo` (id_miembro, `Saldo final`, `Fecha`, `Fondo total del grupo`, `Monto a retirar`)
                VALUES (%s, %s, %s, %s, %s)
            """, (int(row["id_miembro"]), str(round(saldo_final,2)), str(fecha_cierre), str(round(fondo_total,2)), str(round(monto_a_retirar,2))))

        st.success("Ciclo cerrado y distribución registrada.")

        # 7) Acta de cierre (resumen)
        st.markdown("### Acta de Cierre (automática)")
        st.write(f"- Grupo: {id_grupo}")
        st.write(f"- Fecha de cierre: {fecha_cierre}")
        st.write(f"- Préstamos: {len(prestamos)} (todos liquidados)")
        st.write(f"- Intereses: {total_intereses:.2f}")
        st.write(f"- Multas: {total_multas:.2f}")
        st.write(f"- Otros ingresos: {total_otros:.2f}")
        st.write(f"- Utilidades del grupo: {utilidades:.2f}")
        st.write(f"- Ahorro total del grupo: {ahorro_total:.2f}")
        st.write(f"- Fondo total (ahorro + utilidades): {fondo_total:.2f}")

        # Descargar acta como texto
        acta = f"""ACTA DE CIERRE
Grupo: {id_grupo}
Fecha: {fecha_cierre}
Préstamos: {len(prestamos)} (liquidados)
Intereses: {total_intereses:.2f}
Multas: {total_multas:.2f}
Otros ingresos: {total_otros:.2f}
Utilidades del grupo: {utilidades:.2f}
Ahorro total del grupo: {ahorro_total:.2f}
Fondo total: {fondo_total:.2f}
Distribución proporcional de utilidades según ahorro individual.
"""
        st.download_button("Descargar acta", acta.encode("utf-8"), file_name=f"acta_cierre_grupo_{id_grupo}.txt", mime="text/plain")
