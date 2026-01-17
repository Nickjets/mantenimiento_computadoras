import streamlit as st

class VistaClientes:
    @staticmethod
    def mostrar_titulo():
        st.header("👥 Gestión de Clientes")

    @staticmethod
    def mostrar_formulario_registro():

        with st.expander("➕ Registrar Nuevo Cliente", expanded=False):
            with st.form("form_cliente"):
                col1, col2 = st.columns(2)
                with col1:
                    cedula = st.text_input("Cédula / DNI")
                    nombres = st.text_input("Nombres")
                    telefono = st.text_input("Teléfono")
                with col2:
                    email = st.text_input("Email")
                    apellidos = st.text_input("Apellidos")
                    direccion = st.text_input("Dirección")

                if st.form_submit_button("Guardar Cliente"):
                    return {
                        "cedula": cedula, "nombres": nombres, "apellidos": apellidos,
                        "telefono": telefono, "email": email, "direccion": direccion
                    }
        return None

    @staticmethod
    def mostrar_tabla(datos):
        st.subheader("Directorio")
        st.dataframe(datos, use_container_width=True)

    @staticmethod
    def mensaje_exito(msg): st.success(msg)

    @staticmethod
    def mensaje_error(msg): st.error(msg)