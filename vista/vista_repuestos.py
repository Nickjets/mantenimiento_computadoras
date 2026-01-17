import streamlit as st

class VistaRepuestos:

    def mostrar_titulo(self):
        st.title("📦 Gestión de Bodega")

    def mostrar_metricas(self, total_items, valor_inventario, items_bajo_stock):

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Productos", f"{total_items} u.", "Unidades físicas")
        col2.metric("Valor en Bodega", f"${valor_inventario:,.2f}", "Dinero invertido")
        # Si hay bajo stock, mostramos el número en rojo (inverse)
        col3.metric("Stock Crítico", f"{items_bajo_stock} items", "⚠️ Reponer", delta_color="inverse")
        st.divider()

    def mostrar_formulario(self):

        with st.expander("➕ Ingresar Nueva Mercadería", expanded=False):
            with st.form("form_repuesto"):
                col1, col2 = st.columns(2)
                with col1:
                    nombre = st.text_input("Nombre del Repuesto (Ej: SSD 240GB)")
                    marca = st.text_input("Marca")
                with col2:
                    precio = st.number_input("Precio Venta ($)", min_value=0.0, step=0.5)
                    stock = st.number_input("Cantidad Inicial", min_value=1, step=1)

                if st.form_submit_button("Guardar en Inventario"):
                    return {
                        "nombre": nombre,
                        "marca": marca,
                        "precio": precio,
                        "stock": stock
                    }
        return None

    def mostrar_tabla(self, datos):
        st.subheader("📋 Inventario Detallado")
        if datos:
            st.dataframe(datos, use_container_width=True)
        else:
            st.info("La bodega está vacía.")

    def exito(self, msg): st.success(msg)
    def error(self, msg): st.error(msg)