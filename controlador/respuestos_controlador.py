from vista.vista_repuestos import VistaRepuestos
# from modelo.repuesto import Repuesto

class RepuestoControlador:
    def __init__(self):
        self.vista = VistaRepuestos()
        # self.modelo = Repuesto()

    def ejecutar(self):
        # 1. TÍTULO
        self.vista.mostrar_titulo()

        # 2. DATOS SIMULADOS (MOCK)
        inventario_falso = [
            {"ID": 1, "Producto": "SSD Kingston 240GB", "Marca": "Kingston", "Stock": 8, "Precio": 35.00},
            {"ID": 2, "Producto": "Memoria RAM 8GB", "Marca": "Corsair", "Stock": 12, "Precio": 45.50},
            {"ID": 3, "Producto": "Pasta Térmica", "Marca": "Arctic", "Stock": 2, "Precio": 15.00}, # Stock bajo
        ]

        # Calculamos las métricas matemáticamente aquí (Lógica de Negocio)
        total_items = sum(item["Stock"] for item in inventario_falso)
        valor_total = sum(item["Stock"] * item["Precio"] for item in inventario_falso)
        bajo_stock = sum(1 for item in inventario_falso if item["Stock"] < 5)

        # 3. MOSTRAR MÉTRICAS
        self.vista.mostrar_metricas(total_items, valor_total, bajo_stock)

        # 4. FORMULARIO
        datos = self.vista.mostrar_formulario()
        if datos:
            # Aquí iría: self.modelo.crear_repuesto(...)
            if not datos["nombre"]:
                self.vista.error("⚠️ El nombre es obligatorio")
            else:
                self.vista.exito(f"Simulación: {datos['nombre']} ({datos['stock']} u.) guardado correctamente.")

        # 5. TABLA
        self.vista.mostrar_tabla(inventario_falso)