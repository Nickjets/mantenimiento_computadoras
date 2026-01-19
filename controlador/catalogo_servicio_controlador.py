from modelo.catalogo_servicio import CatalogoServicio
from vista.vista_catalogo_servicio import VistaCatalogoServicio
import streamlit as st

class CatalogoServicoControlador:

    def ejecutar(self):
        VistaCatalogoServicio.titulo()

        datos = VistaCatalogoServicio.formulario()
        if datos:
            CatalogoServicio(**datos).guardar()
            st.success("Técnico registrado")
            st.rerun()

        tecnicos = CatalogoServicio.listar_todos()
        eliminar = VistaCatalogoServicio.tabla(tecnicos)

        if eliminar:
            CatalogoServicio.eliminar(eliminar["id_tecnico"])
            st.success("Técnico eliminado")
            st.rerun()
