from modelo.catalogo_servicio import CatalogoServicio
from vista.vista_catalogo_servicio import VistaCatalogoServicio
import streamlit as st

class CatalogoServicoControlador:

    def ejecutar(self):
        VistaCatalogoServicio.titulo()

        datos = VistaCatalogoServicio.formulario()
        if datos:
            CatalogoServicio(**datos).guardar()
            st.success("Servicio registrado")
            st.rerun()

        servicios = CatalogoServicio.listar_todos()
        eliminar = VistaCatalogoServicio.tabla(servicios)

        if eliminar:
            resultado = CatalogoServicio.eliminar(eliminar["id_servicio"])
            if resultado:
                st.success("Servicio eliminado")
                st.rerun()
            else:
                st.error("⚠️ No se puede eliminar este servicio porque está siendo usado en órdenes de servicio")