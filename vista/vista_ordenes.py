import streamlit as st
import datetime
import pandas as pd

class VistaOrdenes:

    def __init__(self):
        self.st = st

    # ------------------------------
    # TITULO
    # ------------------------------
    def mostrar_titulo(self):
        st.title("🛠️ Gestión de Órdenes de Servicio")

    # ------------------------------
    # FORMULARIO CABECERA ORDEN
    # ------------------------------
    def formulario_crear_orden(self, mapa_clientes, mapa_equipos, mapa_tecnicos):
        """
        mapa_clientes: {"Juan Perez": 1}
        mapa_equipos: {"Laptop Dell - SN123": 5}
        mapa_tecnicos: {"Carlos Ruiz": 2}
        """

        st.subheader("📝 Crear Nueva Orden de Servicio")

        with st.form("form_crear_orden"):
            col1, col2 = st.columns(2)

            with col1:
                cliente = st.selectbox("Cliente", options=mapa_clientes.keys())
                equipo = st.selectbox("Equipo", options=mapa_equipos.keys())
                fecha_estimada = st.date_input(
                    "Fecha estimada de entrega",
                    min_value=datetime.date.today()
                )

            with col2:
                tecnico = st.selectbox(
                    "Asignar Técnico",
                    options=["Sin asignar"] + list(mapa_tecnicos.keys())
                )
                estado = st.selectbox(
                    "Estado Inicial",
                    ["RECIBIDO", "DIAGNOSTICO", "EN_REPARACION"]
                )

            problema = st.text_area(
                "Problema Reportado por el Cliente",
                height=100
            )

            if st.form_submit_button("📄 Crear Orden"):
                return {
                    "cliente": cliente,
                    "equipo": equipo,
                    "tecnico": tecnico,
                    "fecha_estimada": fecha_estimada,
                    "estado": estado,
                    "problema": problema
                }

        return None

    # ------------------------------
    # AGREGAR SERVICIO
    # ------------------------------
    def formulario_agregar_servicio(self, mapa_servicios):
        """
        mapa_servicios: {"Mantenimiento General - $20": 1}
        """

        with st.expander("➕ Agregar Servicio", expanded=False):
            with st.form("form_servicio"):
                servicio = st.selectbox(
                    "Servicio",
                    options=mapa_servicios.keys()
                )
                precio = st.number_input(
                    "Precio Aplicado",
                    min_value=0.0,
                    step=1.0
                )
                observacion = st.text_input("Observación")

                if st.form_submit_button("Agregar Servicio"):
                    return {
                        "servicio": servicio,
                        "precio": precio,
                        "observacion": observacion
                    }
        return None

    # ------------------------------
    # AGREGAR REPUESTO
    # ------------------------------
    def formulario_agregar_repuesto(self, mapa_repuestos):
        """
        mapa_repuestos: {"Disco SSD 256GB": 3}
        """

        with st.expander("➕ Agregar Repuesto", expanded=False):
            with st.form("form_repuesto"):
                repuesto = st.selectbox(
                    "Repuesto",
                    options=mapa_repuestos.keys()
                )
                cantidad = st.number_input(
                    "Cantidad",
                    min_value=1,
                    step=1
                )
                precio = st.number_input(
                    "Precio Unitario",
                    min_value=0.0,
                    step=1.0
                )

                if st.form_submit_button("Agregar Repuesto"):
                    return {
                        "repuesto": repuesto,
                        "cantidad": cantidad,
                        "precio": precio
                    }
        return None

    # ------------------------------
    # MOSTRAR DETALLES ACTUALES
    # ------------------------------
    def mostrar_detalles(self, servicios, repuestos):
        st.subheader("📋 Detalles de la Orden")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🛠️ Servicios")
            if servicios:
                st.dataframe(servicios, use_container_width=True)
            else:
                st.info("No hay servicios agregados")

        with col2:
            st.markdown("### 🔩 Repuestos")
            if repuestos:
                st.dataframe(repuestos, use_container_width=True)
            else:
                st.info("No hay repuestos agregados")

    # ------------------------------
    # BANDEJA DE ORDENES
    # ------------------------------
    def mostrar_bandeja(self, lista_ordenes):
        st.subheader("📦 Órdenes Registradas")

        if not lista_ordenes:
            st.info("No existen órdenes registradas.")
            return None

        st.dataframe(lista_ordenes, use_container_width=True)

        opciones = {
            f"#{o['id_orden']} - {o['estado']}": o['id_orden']
            for o in lista_ordenes
        }

        seleccion = st.selectbox(
            "Seleccionar Orden",
            options=opciones.keys()
        )

        nuevo_estado = st.selectbox(
            "Nuevo Estado",
            ["DIAGNOSTICO", "EN_REPARACION", "ESPERANDO_REPUESTO", "LISTO", "ENTREGADO"]
        )

        if st.button("Actualizar Estado"):
            return {
                "id_orden": opciones[seleccion],
                "estado": nuevo_estado
            }

        return None

    # ------------------------------
    # MENSAJES
    # ------------------------------
    def exito(self, msg):
        st.success(msg)

    def error(self, msg):
        st.error(msg)

    # ------------------------------
    # MOSTRAR ORDENES REGISTRADAS
    # ------------------------------
    def mostrar_ordenes_registradas(
            self,
            ordenes,
            detalles_servicio,
            detalles_repuesto
    ):
        st.subheader("📦 Órdenes Registradas")

        if not ordenes:
            st.info("No existen órdenes registradas.")
            return None

        # -------------------------------
        # 1. Selector de orden
        # -------------------------------
        opciones = {
            f"#{o['id_orden']} - {o['cliente']} ({o['estado']})": o['id_orden']
            for o in ordenes
        }

        seleccion = st.selectbox(
            "Seleccione una orden",
            options=opciones.keys()
        )

        id_orden = opciones[seleccion]

        # -------------------------------
        # 2. Cabecera
        # -------------------------------
        orden = next(o for o in ordenes if o['id_orden'] == id_orden)

        with st.container(border=True):
            c1, c2, c3 = st.columns(3)

            c1.metric("Cliente", orden["cliente"])
            c2.metric("Equipo", orden["equipo"])
            c3.metric("Estado", orden["estado"])

            c4, c5, c6 = st.columns(3)
            c4.metric("Técnico", orden["tecnico"])
            fechaRec = orden["fecha_recepcion"].strftime("%d/%m/%Y %H:%M")
            c5.metric("Recepción", fechaRec)
            fechaEst = orden["fecha_estimada"].strftime("%d/%m/%Y %H:%M")
            c6.metric("Entrega Estimada", fechaEst)

            st.markdown("**Problema Reportado**")
            st.write(orden["problema"])

        # -------------------------------
        # 3. Servicios
        # -------------------------------
        st.markdown("### 🛠️ Servicios Aplicados")

        serv = [d for d in detalles_servicio if d["id_orden"] == id_orden]

        if serv:
            st.dataframe(
                pd.DataFrame(serv)[["servicio", "precio_aplicado", "observacion"]],
                use_container_width=True
            )
        else:
            st.info("Sin servicios registrados")

        # -------------------------------
        # 4. Repuestos
        # -------------------------------
        st.markdown("### 🔩 Repuestos Utilizados")

        rep = [d for d in detalles_repuesto if d["id_orden"] == id_orden]

        if rep:
            st.dataframe(
                pd.DataFrame(rep)[["repuesto", "cantidad", "precoin_venta"]],
                use_container_width=True
            )
        else:
            st.info("Sin repuestos registrados")

        # -------------------------------
        # 5. Total
        # -------------------------------
        st.markdown("---")
        st.metric("💰 Total Estimado", f"$ {orden['total']:.2f}")

        return id_orden

