import streamlit as st

class VistaEquipos:

    @staticmethod
    def mostrar_titulo():
        st.header("💻 Gestión de Equipos")

    @staticmethod
    def mostrar_formulario_registro(lista_clientes):
        """
        lista_clientes: lista de dicts [{id_cliente, nombre}]
        """
        with st.expander("➕ Ingresar Nuevo Equipo al Taller", expanded=False):
            with st.form("form_equipo"):
                cliente = st.selectbox(
                    "Propietario (Cliente)",
                    options=lista_clientes,
                    format_func=lambda c: c["nombre"]
                )

                col1, col2 = st.columns(2)
                with col1:
                    tipo = st.selectbox(
                        "Tipo de Equipo",
                        ["Laptop", "PC Escritorio", "All-in-One", "Impresora", "Servidor", "Otro"]
                    )
                    marca = st.text_input("Marca")
                with col2:
                    modelo = st.text_input("Modelo")
                    serie = st.text_input("Número de Serie")

                observaciones = st.text_area("Estado Físico")

                if st.form_submit_button("Guardar Equipo"):
                    return {
                        "id_cliente": cliente["id_cliente"],
                        "tipo_equipo": tipo,
                        "marca": marca,
                        "modelo": modelo,
                        "numero_serie": serie,
                        "observaciones_fisicas": observaciones
                    }
        return None

    @staticmethod
    def mostrar_tabla(datos):
        st.subheader("📋 Inventario de Equipos")

        if not datos:
            st.info("No hay equipos registrados")
            return (None, None)

        headers = ["ID", "Cliente", "Tipo", "Marca", "Modelo", "Serie", "Acciones"]
        cols = st.columns([1, 3, 2, 2, 2, 2, 2])

        for col, h in zip(cols, headers):
            col.markdown(f"**{h}**")

        st.divider()

        for e in datos:
            c1, c2, c3, c4, c5, c6, c7 = st.columns([1,3,2,2,2,2,2])

            c1.write(e["id_equipo"])
            c2.write(e["cliente"])
            c3.write(e["tipo_equipo"])
            c4.write(e["marca"])
            c5.write(e["modelo"])
            c6.write(e["numero_serie"])

            with c7:
                eliminar = st.button("❌", key=f"del_eq_{e['id_equipo']}")

            if eliminar:
                return ("eliminar", e)

        return (None, None)

    @staticmethod
    def mensaje_exito(msg): st.success(msg)
    @staticmethod
    def mensaje_error(msg): st.error(msg)