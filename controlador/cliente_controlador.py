from vista.vista_clientes import VistaClientes
from modelo.cliente import Cliente
import streamlit as st

class ClienteControlador:
    def ejecutar(self):
        VistaClientes.mostrar_titulo()

        # BUSCAR
        cedula_buscar = VistaClientes.buscar_cliente()
        if cedula_buscar:
            cliente = Cliente.buscar_por_cedula(cedula_buscar)
            if cliente:
                st.info(cliente)
            else:
                st.warning("Cliente no encontrado")

        # REGISTRO
        datos = VistaClientes.mostrar_formulario_registro()
        if datos:
            if not Cliente.validar_cedula_ec(datos["cedula"]):
                VistaClientes.mensaje_error("Cédula ecuatoriana inválida")
            elif not Cliente.validar_email(datos["email"]):
                VistaClientes.mensaje_error("Email inválido")
            else:
                Cliente(**datos).guardar()
                VistaClientes.mensaje_exito("Cliente registrado")

        # LISTADO
        clientes = Cliente.listar_todos()
        #acciones
        accion, cliente_sel = VistaClientes.mostrar_tabla(clientes)
        if accion == "eliminar":
            Cliente.eliminar(cliente_sel["id_cliente"])
            VistaClientes.mensaje_exito("Cliente eliminado")
            st.rerun()
        if accion == "editar":
            st.session_state["cliente_editar"] = cliente_sel

        if "cliente_editar" in st.session_state:
            c = st.session_state["cliente_editar"]

            with st.expander("✏️ Editar Cliente", expanded=True):
                with st.form("form_editar_cliente"):
                    c["cedula"] = st.text_input("Cédula", c["cedula"])
                    c["nombres"] = st.text_input("Nombres", c["nombres"])
                    c["apellidos"] = st.text_input("Apellidos", c["apellidos"])
                    c["telefono"] = st.text_input("Teléfono", c["telefono"])
                    c["email"] = st.text_input("Email", c["email"])
                    c["direccion"] = st.text_input("Dirección", c["direccion"])

                    if st.form_submit_button("Actualizar"):
                        if not Cliente.validar_cedula_ec(c["cedula"]):
                            VistaClientes.mensaje_error("Cédula inválida")
                        elif not Cliente.validar_email(c["email"]):
                            VistaClientes.mensaje_error("Email inválido")
                        else:
                            Cliente(**c).actualizar()
                            del st.session_state["cliente_editar"]
                            VistaClientes.mensaje_exito("Cliente actualizado")
                            st.rerun()
