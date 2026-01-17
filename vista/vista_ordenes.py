import streamlit as st
import datetime

class VistaOrdenes:

    def __init__(self):
        self.st = st

    def mostrar_titulo(self):
        st.title("🛠️ Gestión de Órdenes de Servicio")

    def mostrar_formulario_creacion(self, mapa_equipos, mapa_tecnicos):

        st.subheader("📝 Ingresar Equipo a Taller")
        with st.form("form_nueva_orden"):
            col1, col2 = st.columns(2)
            with col1:
                key_equipo = st.selectbox("Seleccione Equipo", options=mapa_equipos.keys())
                fecha = st.date_input("Fecha Estimada de Entrega", min_value=datetime.date.today())

            with col2:
                key_tecnico = st.selectbox("Asignar Técnico", options=mapa_tecnicos.keys())
                prioridad = st.selectbox("Prioridad", ["Normal", "Alta", "Urgente"])

            problema = st.text_area("Descripción de la Falla / Problema Reportado")

            if st.form_submit_button("Generar Orden de Servicio"):
                return {
                    "key_equipo": key_equipo,
                    "key_tecnico": key_tecnico,
                    "fecha": fecha,
                    "problema": problema
                }
        return None

    def mostrar_bandeja_gestion(self, lista_ordenes):

        st.subheader("📋 Bandeja de Trabajo (Técnicos)")

        # 1. Tabla de visualización
        if not lista_ordenes:
            st.info("No hay órdenes activas en este momento.")
            return None

        st.dataframe(lista_ordenes, use_container_width=True)
        st.markdown("---")

        # 2. Panel de Actualización
        st.write("⚙️ **Actualizar Estado de Orden**")

        with st.container(border=True):
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                opciones_visuales = {
                    f"#{o['id_orden']} - {o['modelo']} ({o['estado']})": o['id_orden']
                    for o in lista_ordenes
                }
                if not opciones_visuales:
                    st.warning("No hay órdenes para gestionar.")
                    return None

                seleccion = st.selectbox("Seleccionar Orden", options=opciones_visuales.keys())

            with c2:
                nuevo_estado = st.selectbox("Nuevo Estado",
                                            ["Diagnóstico", "En Reparación", "Esperando Repuesto", "Listo para Retiro", "Entregado"])

            with c3:
                st.write("")
                st.write("")
                if st.button("Actualizar"):
                    id_real = opciones_visuales[seleccion]
                    return {"id_orden": id_real, "nuevo_estado": nuevo_estado}
        return None

    def exito(self, msg): st.success(msg)
    def error(self, msg): st.error(msg)