from modelo.tecnico import Tecnico
from vista.vista_tecnico import VistaTecnico
import streamlit as st

class TecnicoControlador:

    def ejecutar(self):
        VistaTecnico.titulo()

        datos = VistaTecnico.formulario()
        if datos:
            Tecnico(**datos).guardar()
            st.success("Técnico registrado")
            st.rerun()

        tecnicos = Tecnico.listar_todos()
        eliminar = VistaTecnico.tabla(tecnicos)

        if eliminar:
            resultado = Tecnico.eliminar(eliminar["id_tecnico"])
            if resultado:
                st.success("Técnico eliminado")
                st.rerun()
            else:
                st.error("⚠️ No se puede eliminar este técnico porque está asignado a órdenes de servicio")