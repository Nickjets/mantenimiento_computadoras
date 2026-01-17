import streamlit as st
from controlador.cliente_controlador import ClienteControlador
from controlador.equipo_controlador import EquipoControlador
from controlador.orden_controlador import OrdenControlador
from controlador.respuestos_controlador import RepuestoControlador
from controlador.reporte_controlador import ReporteControlador


st.set_page_config(page_title="CompuMercado", layout="wide")
st.sidebar.title("🔧 CompuMercado")

menu = st.sidebar.radio("Módulos", ["Clientes", "Equipos", "Órdenes", "Bodega", "Gerencia"])
if menu == "Clientes":
    app = ClienteControlador()
    app.ejecutar()

elif menu == "Equipos":
    app = EquipoControlador()
    app.ejecutar()

elif menu == "Órdenes":
    app = OrdenControlador()
    app.ejecutar()

elif menu == "Bodega":
    app = RepuestoControlador()
    app.ejecutar()

elif menu == "Gerencia":
    app = ReporteControlador()
    app.ejecutar()