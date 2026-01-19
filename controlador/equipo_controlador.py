from modelo.equipo import equipo
from modelo.cliente import Cliente
from vista.vista_equipos import VistaEquipos
import streamlit as st

class EquipoControlador:

    def ejecutar(self):
        VistaEquipos.mostrar_titulo()

        # 🔹 CLIENTES PARA EL SELECT
        clientes = Cliente.listar_todos()
        lista_clientes = [
            {
                "id_cliente": c["id_cliente"],
                "nombre": f"{c['nombres']} {c['apellidos']}"
            }
            for c in clientes
        ]

        # 🔹 REGISTRO
        datos = VistaEquipos.mostrar_formulario_registro(lista_clientes)
        if datos:
            equipo(**datos).guardar()
            VistaEquipos.mensaje_exito("Equipo registrado")
            st.rerun()

        # 🔹 LISTADO
        equipos = equipo.listar_todos()
        accion, equipo_sel = VistaEquipos.mostrar_tabla(equipos)

        if accion == "eliminar":
            equipo.eliminar(equipo_sel["id_equipo"])
            VistaEquipos.mensaje_exito("Equipo eliminado")
            st.rerun()