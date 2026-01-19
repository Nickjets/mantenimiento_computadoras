from modelo.repuesto import Repuesto
from vista.vista_repuesto import VistaRepuesto
import streamlit as st

class RepuestoControlador:

    def ejecutar(self):
        VistaRepuesto.titulo()

        datos = VistaRepuesto.formulario()
        if datos:
            Repuesto(**datos).guardar()
            st.success("Técnico registrado")
            st.rerun()

        tecnicos = Repuesto.listar_todos()
        eliminar = VistaRepuesto.tabla(tecnicos)

        if eliminar:
            Repuesto.eliminar(eliminar["id_tecnico"])
            st.success("Técnico eliminado")
            st.rerun()
