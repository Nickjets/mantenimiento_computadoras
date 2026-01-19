import streamlit as st

class VistaTecnico:

    @staticmethod
    def titulo():
        st.header("🧑‍🔧 Técnicos")

    @staticmethod
    def formulario():
        with st.expander("➕ Nuevo Técnico"):
            with st.form("form_tecnico"):
                cedula = st.text_input("Cédula")
                nombres = st.text_input("Nombres")
                apellidos = st.text_input("Apellidos")
                especialidad = st.text_input("Especialidad")
                telefono = st.text_input("Teléfono")

                if st.form_submit_button("Guardar"):
                    return {
                        "cedula": cedula,
                        "nombres": nombres,
                        "apellidos": apellidos,
                        "especialidad": especialidad,
                        "telefono": telefono
                    }
        return None

    @staticmethod
    def tabla(datos):
        st.subheader("📋 Lista de Técnicos")

        for t in datos:
            col1, col2, col3, col4, col5, col6 = st.columns([2,3,3,3,2,1])
            col1.write(t["cedula"])
            col2.write(t["nombres"])
            col3.write(t["apellidos"])
            col4.write(t["especialidad"])
            col5.write(t["telefono"])
            if col6.button("❌", key=f"del_tecnico_{t['id_tecnico']}"):
                return t
        return None
