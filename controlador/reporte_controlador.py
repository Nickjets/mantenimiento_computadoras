import streamlit as st
from DAO.reportes_dao import ReportesDAO
from vista.vista_reportes import VistaReportes
import pandas as pd

class ReporteControlador:
    def __init__(self):
        self.dao = ReportesDAO()
        self.vista = VistaReportes()

    def ejecutar(self):
        # Menú de reportes
        opcion = self.vista.mostrar_menu_principal()

        # Mostrar título
        self.vista.mostrar_titulo("📊 Módulo de Reportes")

        # Ejecutar reporte seleccionado
        if opcion == "📈 Dashboard General":
            self.mostrar_dashboard_simple()
        elif opcion == "🔧 Órdenes Completas":
            self.mostrar_ordenes_completas_simple()
        elif opcion == "⏳ Órdenes Activas":
            self.mostrar_ordenes_activas_simple()
        elif opcion == "📦 Inventario Bajo":
            self.mostrar_inventario_bajo_simple()
        elif opcion == "👨‍🔧 Rendimiento Técnicos":
            self.mostrar_rendimiento_tecnicos_simple()
        elif opcion == "🛠️ Servicios Populares":
            self.mostrar_servicios_populares_simple()
        elif opcion == "👥 Clientes Frecuentes":
            self.mostrar_clientes_frecuentes_simple()
        elif opcion == "💰 Reporte Financiero":
            self.mostrar_reporte_financiero_simple()
        elif opcion == "⚠️ Equipos Abandonados":
            self.mostrar_equipos_abandonados_simple()
        elif opcion == "📅 Técnicos del Mes":
            self.mostrar_tecnicos_mes_simple()
        elif opcion == "📊 Servicios del Mes":
            self.mostrar_servicios_mes_simple()

    # ============================================
    # VERSIONES SIMPLES - SOLO SELECTS
    # ============================================

    def mostrar_dashboard_simple(self):
        """Muestra estadísticas básicas sin gráficos"""
        st.subheader("📊 Resumen General")

        # Obtener estadísticas
        estadisticas = self.dao.obtener_estadisticas_generales()

        # Mostrar en columnas
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Órdenes Activas", estadisticas.get('ordenes_activas', 0))

        with col2:
            st.metric("Repuestos Críticos", estadisticas.get('repuestos_criticos', 0))

        with col3:
            st.metric("Equipos Abandonados", estadisticas.get('equipos_abandonados', 0))

        with col4:
            st.metric("Ingresos Mes", f"${estadisticas.get('ingresos_mes_actual', 0):,.2f}")

    def mostrar_ordenes_completas_simple(self):
        """Muestra todas las órdenes completas"""
        st.subheader("🔧 Todas las Órdenes de Servicio")

        # Obtener datos
        df = self.dao.obtener_ordenes_completas()

        if not df.empty:
            # Mostrar conteo
            st.info(f"Total de órdenes: {len(df)}")

            # Mostrar tabla
            st.dataframe(df, use_container_width=True, height=400)

            # Opción para descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="ordenes_completas.csv",
                mime="text/csv"
            )
        else:
            st.info("No hay órdenes registradas")

    def mostrar_ordenes_activas_simple(self):
        """Muestra órdenes activas/pendientes"""
        st.subheader("⏳ Órdenes Activas/Pendientes")

        # Obtener datos
        df = self.dao.obtener_ordenes_activas()

        if not df.empty:
            # Mostrar conteo
            atrasadas = df[df['dias_restantes'] < 0].shape[0]
            st.info(f"Total activas: {len(df)} | Atrasadas: {atrasadas}")

            # Mostrar tabla
            st.dataframe(df, use_container_width=True, height=400)

            # Descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="ordenes_activas.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ No hay órdenes activas pendientes")

    def mostrar_inventario_bajo_simple(self):
        """Muestra inventario bajo stock"""
        st.subheader("📦 Inventario Bajo Stock")

        # Obtener datos
        df = self.dao.inventario_bajo()

        if not df.empty:
            # Mostrar conteo por nivel
            niveles = df['nivel_stock'].value_counts()
            st.write("**Resumen por nivel:**")
            for nivel, cantidad in niveles.items():
                st.write(f"- {nivel}: {cantidad}")

            # Mostrar tabla
            st.dataframe(df, use_container_width=True, height=400)

            # Descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="inventario_bajo.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ Todo el inventario está en niveles normales")

    def mostrar_rendimiento_tecnicos_simple(self):
        """Muestra rendimiento de técnicos"""
        st.subheader("👨‍🔧 Rendimiento de Técnicos")

        # Obtener datos
        df = self.dao.rendimiento_tecnicos()

        if not df.empty:
            # Mostrar tabla
            st.dataframe(df, use_container_width=True, height=400)

            # Estadísticas simples
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Técnicos", len(df))
            with col2:
                total_facturado = df['total_facturado'].sum()
                st.metric("Total Facturado", f"${total_facturado:,.2f}")
            with col3:
                promedio = df['promedio_por_orden'].mean()
                st.metric("Promedio/Orden", f"${promedio:,.2f}")

            # Descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="rendimiento_tecnicos.csv",
                mime="text/csv"
            )
        else:
            st.info("No hay datos de rendimiento de técnicos")

    def mostrar_servicios_populares_simple(self):
        """Muestra servicios más solicitados"""
        st.subheader("🛠️ Servicios Más Solicitados")

        # Obtener datos
        df = self.dao.servicios_populares()

        if not df.empty:
            # Mostrar top 10
            st.write(f"**Top {min(10, len(df))} servicios más solicitados:**")

            # Mostrar tabla
            st.dataframe(df, use_container_width=True, height=400)

            # Estadísticas
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Servicios", len(df))
            with col2:
                ingreso_total = df['ingreso_total'].sum()
                st.metric("Ingreso Total", f"${ingreso_total:,.2f}")

            # Descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="servicios_populares.csv",
                mime="text/csv"
            )
        else:
            st.info("No hay datos de servicios")

    def mostrar_clientes_frecuentes_simple(self):
        """Muestra clientes frecuentes"""
        st.subheader("👥 Clientes Frecuentes")

        # Obtener datos
        df = self.dao.clientes_frecuentes()

        if not df.empty:
            # Asegurarse de que total_gastado sea numérico
            if 'total_gastado' in df.columns:
                # Convertir a numérico, forzando errores a NaN y luego a 0
                df['total_gastado'] = pd.to_numeric(df['total_gastado'], errors='coerce').fillna(0)

            # Mostrar top 10 por gasto
            top_clientes = df.nlargest(10, 'total_gastado')

            st.write("**Top 10 clientes por gasto total:**")
            st.dataframe(top_clientes, use_container_width=True, height=400)

            # Estadísticas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Clientes", len(df))
            with col2:
                total_gastado = df['total_gastado'].sum()
                st.metric("Total Gastado", f"${total_gastado:,.2f}")
            with col3:
                promedio = df['total_gastado'].mean()
                st.metric("Promedio/Cliente", f"${promedio:,.2f}")

            # Descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="clientes_frecuentes.csv",
                mime="text/csv"
            )
        else:
            st.info("No hay datos de clientes")

    def mostrar_reporte_financiero_simple(self):
        """Muestra reporte financiero mensual"""
        st.subheader("💰 Reporte Financiero Mensual")

        # Obtener datos
        df = self.dao.financiero_mensual(meses_atras=3)

        if not df.empty:
            # Mostrar tabla
            st.dataframe(df, use_container_width=True, height=400)

            # Totales
            col1, col2, col3 = st.columns(3)
            with col1:
                total_ingresos = df['ingresos_totales'].sum()
                st.metric("Ingresos Totales", f"${total_ingresos:,.2f}")
            with col2:
                total_ordenes = df['total_ordenes'].sum()
                st.metric("Total Órdenes", total_ordenes)
            with col3:
                promedio = df['promedio_por_orden'].mean()
                st.metric("Promedio/Orden", f"${promedio:,.2f}")

            # Descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="reporte_financiero.csv",
                mime="text/csv"
            )
        else:
            st.info("No hay datos financieros")

    def mostrar_equipos_abandonados_simple(self):
        """Muestra equipos abandonados"""
        st.subheader("⚠️ Equipos Abandonados")

        # Obtener datos
        df = self.dao.equipos_abandonados()

        if not df.empty:
            # Mostrar por nivel de alerta
            st.write(f"**Total equipos abandonados: {len(df)}**")

            # Separar por nivel
            criticos = df[df['nivel_alerta'] == 'CRÍTICO']
            altos = df[df['nivel_alerta'] == 'ALTO']
            moderados = df[df['nivel_alerta'] == 'MODERADO']

            if not criticos.empty:
                st.error(f"🚨 CRÍTICOS: {len(criticos)} equipos")

            if not altos.empty:
                st.warning(f"⚠️ ALTOS: {len(altos)} equipos")

            if not moderados.empty:
                st.info(f"ℹ️ MODERADOS: {len(moderados)} equipos")

            # Mostrar tabla completa
            st.dataframe(df, use_container_width=True, height=400)

            # Descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="equipos_abandonados.csv",
                mime="text/csv"
            )
        else:
            st.success("✅ No hay equipos abandonados")

    def mostrar_tecnicos_mes_simple(self):
        """Muestra técnicos del mes actual"""
        st.subheader("📅 Técnicos del Mes Actual")

        # Obtener datos
        df = self.dao.ingreso_tecnicos()

        if not df.empty:
            # Mostrar ranking simple
            st.write("**Ranking de técnicos este mes:**")

            for idx, (_, row) in enumerate(df.iterrows(), 1):
                col1, col2, col3 = st.columns([1, 3, 2])
                with col1:
                    st.write(f"**{idx}**")
                with col2:
                    st.write(row['tecnico'])
                with col3:
                    st.write(f"**{row['ordenes_atendidas_mes']}** órdenes")
                st.divider()

            # Mostrar tabla completa
            st.dataframe(df, use_container_width=True, height=300)

            # Descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="tecnicos_mes.csv",
                mime="text/csv"
            )
        else:
            st.info("No hay datos de técnicos para este mes")

    def mostrar_servicios_mes_simple(self):
        """Muestra servicios del mes actual"""
        st.subheader("📊 Servicios del Mes Actual")

        # Obtener datos
        df = self.dao.servicios_solicitados()

        if not df.empty:
            # Mostrar top 5
            st.write("**Top 5 servicios este mes:**")

            for idx, (_, row) in enumerate(df.head(5).iterrows(), 1):
                col1, col2, col3 = st.columns([1, 3, 2])
                with col1:
                    st.write(f"**{idx}**")
                with col2:
                    st.write(row['nombre_servicio'])
                with col3:
                    st.write(f"**{row['veces_solicitado_mes']}** veces")
                st.divider()

            # Mostrar tabla completa
            st.dataframe(df, use_container_width=True, height=300)

            # Estadísticas
            col1, col2 = st.columns(2)
            with col1:
                total_solicitudes = df['veces_solicitado_mes'].sum()
                st.metric("Total Solicitudes", total_solicitudes)
            with col2:
                servicios_unicos = len(df)
                st.metric("Servicios Diferentes", servicios_unicos)

            # Descargar
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="servicios_mes.csv",
                mime="text/csv"
            )
        else:
            st.info("No hay servicios registrados este mes")