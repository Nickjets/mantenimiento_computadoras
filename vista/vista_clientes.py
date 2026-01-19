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

        if not datos:
            st.info("No hay clientes registrados")
            return

        # Cabecera simulando tabla
        cols = st.columns([1, 2, 2, 2, 2, 3, 2])
        headers = ["ID", "Cédula", "Nombres", "Apellidos", "Teléfono", "Email", "Acciones"]

        for col, h in zip(cols, headers):
            col.markdown(f"**{h}**")

        st.divider()

        for cliente in datos:
            col1, col2, col3, col4, col5, col6, col7 = st.columns([1,2,2,2,2,3,2])

            col1.write(cliente["id_cliente"])
            col2.write(cliente["cedula"])
            col3.write(cliente["nombres"])
            col4.write(cliente["apellidos"])
            col5.write(cliente["telefono"])
            col6.write(cliente["email"])

            with col7:
                editar = st.button("✏️", key=f"edit_{cliente['id_cliente']}")
                eliminar = st.button("❌", key=f"del_{cliente['id_cliente']}")

            # Retornar acciones al controlador
            if editar:
                return ("editar", cliente)
            if eliminar:
                return ("eliminar", cliente)

        return (None, None)

    @staticmethod
    def mensaje_exito(msg): st.success(msg)

    @staticmethod
    def mensaje_error(msg): st.error(msg)

    @staticmethod
    def buscar_cliente():
        with st.expander("🔍 Buscar por Cédula"):
            return st.text_input("Ingrese cédula a buscar")

    @staticmethod
    def acciones_tabla(cliente):
        col1, col2 = st.columns(2)
        with col1:
            editar = st.button("✏️ Editar", key=f"edit_{cliente['id_cliente']}")
        with col2:
            eliminar = st.button("❌ Eliminar", key=f"del_{cliente['id_cliente']}")
        return editar, eliminar