import streamlit as st

class VistaEquipos:

    def __init__(self):
        # Permitimos que el controlador acceda a funciones de Streamlit si es necesario
        self.st = st

    def mostrar_titulo(self):
        st.header("💻 Gestión de Equipos")

    def mostrar_formulario_registro(self, lista_nombres_clientes):
        """
        Dibuja el formulario de registro.
        :param lista_nombres_clientes: Lista simple ["Juan Perez", "Maria Lopez"]
        :return: Diccionario con los datos ingresados O None si no se pulsó guardar.
        """
        with st.expander("➕ Ingresar Nuevo Equipo al Taller", expanded=True):
            with st.form("form_equipo"):
                # El selectbox se llena con la lista que le manda el Controlador
                cliente_seleccionado = st.selectbox("Propietario (Cliente)", options=lista_nombres_clientes)

                col1, col2 = st.columns(2)
                with col1:
                    tipo = st.selectbox("Tipo de Equipo", ["Laptop", "PC Escritorio", "All-in-One", "Impresora", "Servidor", "Otro"])
                    marca = st.text_input("Marca (Ej: Dell, HP)")
                with col2:
                    modelo = st.text_input("Modelo")
                    serie = st.text_input("Número de Serie / Service Tag")

                observaciones = st.text_area("Estado Físico (Rayones, golpes, cargador incluido...)", height=80)

                submitted = st.form_submit_button("Guardar Equipo")

                if submitted:
                    # Empaquetamos los datos y se los devolvemos al Controlador
                    return {
                        "cliente_nombre": cliente_seleccionado,
                        "tipo": tipo,
                        "marca": marca,
                        "modelo": modelo,
                        "serie": serie,
                        "observaciones": observaciones
                    }
        return None

    def mostrar_tabla_inventario(self, datos_equipos):
        """
        Muestra la tabla de equipos.
        :param datos_equipos: Lista de diccionarios o DataFrame.
        """
        st.subheader("📋 Inventario de Equipos en Taller")

        if not datos_equipos:
            st.info("No hay equipos registrados aún.")
        else:
            # use_container_width hace que la tabla ocupe todo el ancho
            st.dataframe(datos_equipos, use_container_width=True)

    def mostrar_exito(self, mensaje):
        st.success(mensaje)

    def mostrar_error(self, mensaje):
        st.error(mensaje)