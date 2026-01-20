from modelo.repuesto import Repuesto
from vista.vista_repuesto import VistaRepuesto
import streamlit as st

class RepuestoControlador:

    def ejecutar(self):
        VistaRepuesto.titulo()

        datos = VistaRepuesto.formulario()
        if datos:
            Repuesto(**datos).guardar()
            st.success("Repuesto registrado")
            st.rerun()

        repuestos = Repuesto.listar_todos()
        eliminar = VistaRepuesto.tabla(repuestos)

        if eliminar:
            resultado = Repuesto.eliminar(eliminar["id_repuesto"])
            if resultado:
                st.success("Repuesto eliminado")
                st.rerun()
            else:
                st.error("⚠️ No se puede eliminar este repuesto porque está siendo usado en órdenes de servicio")