# from modelo.equipo import Equipo    <-- COMENTA
# from modelo.cliente import Cliente  <-- COMENTA
from vista.vista_equipos import VistaEquipos

class EquipoControlador:
    def __init__(self):
        self.vista = VistaEquipos()

    def ejecutar(self):
        self.vista.mostrar_titulo()

        # --- 1. SIMULAR CLIENTES PARA EL DROPDOWN ---
        # Fingimos que la BD nos devolvió esto
        mapa_clientes_falso = {
            "Pablo Jaiba (010101)": 1,
            "Katy Velasco (020202)": 2,
            "Cliente Nuevo (999999)": 3
        }

        datos_formulario = self.vista.mostrar_formulario_registro(list(mapa_clientes_falso.keys()))

        if datos_formulario:
            # SIMULACIÓN DE GUARDADO
            if not datos_formulario["serie"]:
                self.vista.mostrar_error("⚠️ La serie es obligatoria (Validado en Controlador)")
            else:
                self.vista.mostrar_exito(f"Simulación: Equipo {datos_formulario['marca']} registrado correctamente.")

        # --- 2. SIMULAR TABLA DE INVENTARIO ---
        inventario_falso = [
            {"id_equipo": 101, "tipo_equipo": "Laptop", "marca": "Dell", "modelo": "XPS", "dueno_nombre": "Pablo Jaiba", "observaciones_fisicas": "Rayado"},
            {"id_equipo": 102, "tipo_equipo": "PC", "marca": "HP", "modelo": "Pavilion", "dueno_nombre": "Katy Velasco", "observaciones_fisicas": "Nuevo"},
        ]

        self.vista.mostrar_tabla_inventario(inventario_falso)