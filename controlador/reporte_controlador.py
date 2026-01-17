from vista.vista_reportes import VistaReportes
# from modelo.reporte import Reporte

class ReporteControlador:
    def __init__(self):
        self.vista = VistaReportes()

    def ejecutar(self):
        self.vista.mostrar_titulo()

        # --- 1. DATOS SIMULADOS (MOCK) PARA GRÁFICOS ---
        mock_ingresos = {
            "Técnico": ["Juan Pérez", "Maria López", "Pedro (Nuevo)", "Carlos"],
            "Total ($)": [1250.50, 2800.00, 450.00, 900.00]
        }

        # Query: SELECT servicio, COUNT(*) ... GROUP BY servicio
        mock_servicios = {
            "Servicio": ["Formateo", "Limpieza", "Cambio Pantalla", "Antivirus", "Recuperación"],
            "Cantidad": [45, 30, 15, 60, 5]
        }

        self.vista.mostrar_graficos_principales(mock_ingresos, mock_servicios)

        # --- 2. DATOS SIMULADOS PARA TABLA (La consulta compleja) ---
        mock_abandonados = [
            {"Orden": "#004", "Cliente": "Luis Fonsi", "Equipo": "Macbook Air", "Días en Taller": 45, "Estado": "Terminado"},
            {"Orden": "#012", "Cliente": "Ana Gabriel", "Equipo": "Impresora Epson", "Días en Taller": 32, "Estado": "Diagnóstico"},
        ]

        self.vista.mostrar_tabla_alertas(mock_abandonados)