import streamlit as st

class VistaReportes:

    @staticmethod
    def mostrar_menu_principal():
        """Muestra el menú principal de reportes"""
        return st.sidebar.selectbox(
            "📊 Seleccione Reporte",
            [
                "📈 Dashboard General",
                "🔧 Órdenes Completas",
                "⏳ Órdenes Activas",
                "📦 Inventario Bajo",
                "👨‍🔧 Rendimiento Técnicos",
                "🛠️ Servicios Populares",
                "👥 Clientes Frecuentes",
                "💰 Reporte Financiero",
                "⚠️ Equipos Abandonados",
                "📅 Técnicos del Mes",
                "📊 Servicios del Mes"
            ]
        )

    @staticmethod
    def mostrar_titulo(titulo: str):
        """Muestra título de la página"""
        st.title(titulo)