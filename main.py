import streamlit as st
from controlador.cliente_controlador import ClienteControlador
from controlador.equipo_controlador import EquipoControlador
from controlador.orden_controlador import OrdenControlador
from controlador.repuesto_controlador import RepuestoControlador
from controlador.reporte_controlador import ReporteControlador

import db_config
import time

# Configuración de la página
st.set_page_config(page_title="CompuMercado", layout="wide")

# Función para verificar conexión a BD
def verificar_conexion_bd():
    """Verifica la conexión a la base de datos"""
    try:
        # Intenta obtener una conexión
        connection = db_config.db_config.get_connection()

        # Crea un cursor y ejecuta una consulta simple
        cursor = connection.cursor()
        cursor.execute("SELECT 1")  # Consulta simple para PostgreSQL
        cursor.fetchone()

        # Cierra cursor y conexión
        cursor.close()
        connection.close()

        return True, "✅ Conexión a base de datos establecida correctamente"
    except Exception as e:
        return False, f"❌ Error de conexión: {str(e)}"

# Inicialización con verificación de conexión
st.sidebar.title("🔧 CompuMercado")

# Mostrar estado de conexión en el sidebar
with st.sidebar:
    st.subheader("Estado del Sistema")

    # Verificar conexión
    conexion_ok, mensaje = verificar_conexion_bd()

    if conexion_ok:
        st.success(mensaje)
    else:
        st.error(mensaje)
        st.warning("⚠️ Algunas funciones pueden no estar disponibles")

# Menú principal
menu = st.sidebar.radio("Módulos", ["Clientes", "Equipos", "Órdenes", "Repuestos", "Gerencia", ])

# Solo mostrar la aplicación si la conexión es exitosa
if conexion_ok:
    if menu == "Clientes":
        app = ClienteControlador()
        app.ejecutar()

    elif menu == "Equipos":
        app = EquipoControlador()
        app.ejecutar()

    elif menu == "Órdenes":
        app = OrdenControlador()
        app.ejecutar()

    elif menu == "Repuestos":
        app = RepuestoControlador()
        app.ejecutar()

    elif menu == "Gerencia":
        app = ReporteControlador()
        app.ejecutar()
else:
    # Mostrar mensaje de error y opciones de solución
    st.error("No se pudo conectar a la base de datos")

    with st.expander("🔧 Solución de problemas"):
        st.markdown("""
        ### Verifica lo siguiente:
        1. **PostgreSQL está ejecutándose**
        2. **Credenciales correctas** en el archivo `.env`
        3. **Base de datos existe**: `CompuServicio`
        4. **Puerto correcto**: 5432 (por defecto)
        
        ### Archivo `.env` debería contener:
        ```
        DB_HOST=localhost
        DB_USER=postgres
        DB_PASSWORD=tu_contraseña
        DB_NAME=CompuServicio
        DB_PORT=5432
        ```
        """)

        # Botón para reintentar conexión
        if st.button("🔄 Reintentar conexión"):
            st.rerun()