import streamlit as st

class VistaRepuesto:

    @staticmethod
    def titulo():
        st.header("📦 Repuestos")

    @staticmethod
    def formulario():
        with st.expander("➕ Nuevo Repuesto"):
            with st.form("form_repuesto"):
                nombre = st.text_input("Nombre")
                marca = st.text_input("Marca")
                stock = st.number_input("Stock", min_value=0, step=1)
                precio = st.number_input("Precio Unitario", min_value=0.0, step=0.5)

                if st.form_submit_button("Guardar"):
                    return {
                        "nombre": nombre,
                        "marca": marca,
                        "stock_actual": stock,
                        "precio_unitario": precio
                    }
        return None

    @staticmethod
    def tabla(datos):
        st.subheader("📋 Inventario")
        for r in datos:
            c1, c2, c3, c4, c5 = st.columns([3,2,2,2,1])
            c1.write(r["nombre"])
            c2.write(r["marca"])
            c3.write(r["stock_actual"])
            c4.write(f"${r['precio_unitario']}")
            if c5.button("❌", key=f"del_rep_{r['id_repuesto']}"):
                return r
        return None
