import streamlit as st
import pandas as pd

class VistaReportes:

    def mostrar_titulo(self):
        st.title("📊 Dashboard Gerencial")
        st.markdown("Resultados financieros y operativos del taller.")

    def mostrar_graficos_principales(self, datos_ingresos, datos_servicios):

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("💰 Ingresos por Técnico")
            # Convertimos el diccionario a DataFrame para que Streamlit lo entienda
            df_ingresos = pd.DataFrame(datos_ingresos)
            st.bar_chart(df_ingresos, x="Técnico", y="Total ($)", color="#4CAF50")

        with col2:
            st.subheader("🏆 Servicios Más Vendidos")
            df_servicios = pd.DataFrame(datos_servicios)
            # Gráfico de área para variar
            st.area_chart(df_servicios, x="Servicio", y="Cantidad", color="#2196F3")

    def mostrar_tabla_alertas(self, equipos_abandonados):
        st.divider()
        st.subheader("⚠️ Alerta: Equipos 'Abandonados'")
        st.caption("Equipos que llevan más de 30 días en el taller sin ser retirados.")

        if equipos_abandonados:
            st.dataframe(equipos_abandonados, use_container_width=True)
            st.warning(f"Hay {len(equipos_abandonados)} equipos ocupando espacio innecesariamente.")
        else:
            st.success("¡Excelente! No hay equipos abandonados.")