import streamlit as st
from vista.vista_ordenes import VistaOrdenes

from modelo.orden import OrdenServicio
from modelo.orden_detalle_servico import DetalleOrdenServicio
from modelo.orden_detalle_repuesto import DetalleOrdenRepuesto

from modelo.cliente import Cliente
from modelo.equipo import equipo
from modelo.tecnico import Tecnico
from modelo.catalogo_servicio import CatalogoServicio
from modelo.repuesto import Repuesto


class OrdenServicioControlador:

    def ejecutar(self):
        vista = VistaOrdenes()
        vista.mostrar_titulo()

        # -------------------------
        # SESSION STATE INICIAL
        # -------------------------
        if "orden_id" not in st.session_state:
            st.session_state.orden_id = None
            st.session_state.servicios = []
            st.session_state.repuestos = []
            st.session_state.estado_orden = None

        # -------------------------
        # MAPAS PARA SELECTBOX
        # -------------------------
        mapa_clientes = {
            f"{c['nombres']} {c['apellidos']}": c["id_cliente"]
            for c in Cliente.listar_todos()
        }

        mapa_equipos = {
            f"{e['tipo_equipo']} {e['marca']} ({e['numero_serie']})": e["id_equipo"]
            for e in equipo.listar_todos()
        }

        mapa_tecnicos = {
            f"{t['nombres']} {t['apellidos']}": t["id_tecnico"]
            for t in Tecnico.listar_todos()
        }

        mapa_servicios = {
            f"{s['nombre_servicio']} - ${s['precio_base']}": s["id_servicio"]
            for s in CatalogoServicio.listar_todos()
        }

        mapa_repuestos = {
            f"{r['nombre']} ({r['stock_actual']} en stock)": r["id_repuesto"]
            for r in Repuesto.listar_todos()
        }

        # -------------------------
        # CREAR ORDEN (CABECERA)
        # -------------------------
        if st.session_state.orden_id is None:

            data = vista.formulario_crear_orden(
                mapa_clientes, mapa_equipos, mapa_tecnicos
            )

            if data:
                id_cliente = mapa_clientes[data["cliente"]]
                id_equipo = mapa_equipos[data["equipo"]]
                id_tecnico = None if data["tecnico"] == "Sin asignar" else mapa_tecnicos[data["tecnico"]]

                orden = OrdenServicio(
                    id_equipo=id_equipo,
                    id_cliente=id_cliente,
                    id_tecnico=id_tecnico,
                    fecha_estimada_entrega=data["fecha_estimada"],
                    estado=data["estado"],
                    problema_reportado=data["problema"]
                )

                st.session_state.orden_id = orden.guardar()
                st.session_state.estado_orden = data["estado"]

                vista.exito("Orden de servicio creada correctamente")
                st.rerun()

        # -------------------------
        # BLOQUEO SI ENTREGADA
        # -------------------------
        if st.session_state.estado_orden == "ENTREGADO":
            st.warning("⚠️ Esta orden está ENTREGADA. No se puede modificar.")
            self._mostrar_resumen(vista)

            # Botón para volver
            if st.button("🔙 Volver al listado"):
                self._reset()
                st.rerun()
            return

        # -------------------------
        # AGREGAR SERVICIOS
        # -------------------------
        servicio = vista.formulario_agregar_servicio(mapa_servicios)
        if servicio:
            st.session_state.servicios.append({
                "id_servicio": mapa_servicios[servicio["servicio"]],
                "precio": servicio["precio"],
                "observacion": servicio["observacion"]
            })
            st.rerun()

        # -------------------------
        # AGREGAR REPUESTOS
        # -------------------------
        repuesto = vista.formulario_agregar_repuesto(mapa_repuestos)
        if repuesto:
            st.session_state.repuestos.append({
                "id_repuesto": mapa_repuestos[repuesto["repuesto"]],
                "cantidad": repuesto["cantidad"],
                "precio": repuesto["precio"]
            })
            st.rerun()

        # -------------------------
        # MOSTRAR DETALLES
        # -------------------------
        vista.mostrar_detalles(
            st.session_state.servicios,
            st.session_state.repuestos
        )

        # -------------------------
        # TOTAL AUTOMÁTICO
        # -------------------------
        total = self._calcular_total()
        st.metric("💰 Total Estimado", f"${total:.2f}")

        # -------------------------
        # CONFIRMAR ORDEN
        # -------------------------
        if st.button("✅ Confirmar Orden"):
            self._guardar_detalles()
            OrdenServicio.actualizar_total(
                st.session_state.orden_id,
                total
            )
            vista.exito("Orden finalizada correctamente")
            self._reset()
            st.rerun()

        # -------------------------
        # VER ÓRDENES EXISTENTES
        # -------------------------
        st.markdown("---")
        ordenes = OrdenServicio.listar_ordenes()

        det_serv = []
        det_rep = []

        if ordenes:
            for o in ordenes:
                det_serv.extend(
                    DetalleOrdenServicio.listar_por_orden(o["id_orden"])
                )
                det_rep.extend(
                    DetalleOrdenRepuesto.listar_por_orden(o["id_orden"])
                )

            # CAPTURAR LA ACCIÓN RETORNADA
            accion = vista.mostrar_ordenes_registradas(
                ordenes,
                det_serv,
                det_rep
            )

            # MANEJAR LAS ACCIONES
            if accion:
                if accion["tipo"] == "actualizar_estado":
                    OrdenServicio.actualizar_estado(
                        accion["id_orden"],
                        accion["nuevo_estado"]
                    )
                    vista.exito(f"Estado actualizado a {accion['nuevo_estado']}")
                    st.rerun()

                elif accion["tipo"] == "editar_diagnostico":
                    st.session_state["editando_diagnostico"] = accion["id_orden"]
                    st.rerun()

                elif accion["tipo"] == "volver":
                    if "editando_diagnostico" in st.session_state:
                        del st.session_state["editando_diagnostico"]
                    st.rerun()

    # =====================================================
    # MÉTODOS PRIVADOS
    # =====================================================
    def _calcular_total(self):
        total_servicios = sum(s["precio"] for s in st.session_state.servicios)
        total_repuestos = sum(
            r["precio"] * r["cantidad"] for r in st.session_state.repuestos
        )
        return total_servicios + total_repuestos

    def _guardar_detalles(self):
        for s in st.session_state.servicios:
            DetalleOrdenServicio(
                id_orden=st.session_state.orden_id,
                id_servicio=s["id_servicio"],
                precio_aplicado=s["precio"],
                observacion=s["observacion"]
            ).guardar()

        for r in st.session_state.repuestos:
            DetalleOrdenRepuesto(
                id_orden=st.session_state.orden_id,
                id_repuesto=r["id_repuesto"],
                cantidad=r["cantidad"],
                precio_venta=r["precio"]  # CORREGIDO: precio_venta en lugar de precoin_venta
            ).guardar()

    def _mostrar_resumen(self, vista):
        vista.mostrar_detalles(
            st.session_state.servicios,
            st.session_state.repuestos
        )
        total = self._calcular_total()
        st.metric("💰 Total Final", f"${total:.2f}")

    def _reset(self):
        st.session_state.orden_id = None
        st.session_state.servicios = []
        st.session_state.repuestos = []
        st.session_state.estado_orden = None