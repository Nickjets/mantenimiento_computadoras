import streamlit as st

class VistaCatalogoServicio:

    @staticmethod
    def titulo():
        st.header("🛠️ Catálogo de Servicios")

    @staticmethod
    def formulario():
        with st.expander("➕ Nuevo Servicio"):
            with st.form("form_servicio"):
                nombre = st.text_input("Servicio")
                precio = st.number_input("Precio Base", min_value=0.0, step=1.0)
                descripcion = st.text_area("Descripción")

                if st.form_submit_button("Guardar"):
                    return {
                        "nombre_servicio": nombre,
                        "precio_base": precio,
                        "descripcion": descripcion
                    }
        return None

    @staticmethod
    def tabla(datos):
        st.subheader("📋 Servicios")
        for s in datos:
            c1, c2, c3, c4 = st.columns([4,2,4,1])
            c1.write(s["nombre_servicio"])
            c2.write(f"${s['precio_base']}")
            c3.write(s["descripcion"])
            if c4.button("❌", key=f"del_serv_{s['id_servicio']}"):
                return s
        return None
