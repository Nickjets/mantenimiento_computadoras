# from modelo.cliente import Cliente  <-- COMENTA ESTO POR AHORA
from vista.vista_clientes import VistaClientes

class ClienteControlador:
    def __init__(self):
        # self.modelo = Cliente()     <-- COMENTA ESTO
        self.vista = VistaClientes()

    def ejecutar(self):
        self.vista.mostrar_titulo()
        datos_form = self.vista.mostrar_formulario_registro()

        if datos_form:
            # SIMULACIÓN DE GUARDADO
            # En lugar de guardar en BD, solo mostramos éxito visualmente
            self.vista.mensaje_exito(f"Simulación: Cliente {datos_form['nombres']} guardado (No en BD)")

        # --- AQUÍ ESTÁ EL TRUCO (DATOS FALSOS / MOCK DATA) ---
        lista_clientes_falsa = [
            {"id_cliente": 1, "cedula": "010101", "nombres": "Pablo", "apellidos": "Jaiba", "telefono": "0999", "email": "p@test.com", "direccion": "Centro"},
            {"id_cliente": 2, "cedula": "020202", "nombres": "Katy", "apellidos": "Velasco", "telefono": "0888", "email": "k@test.com", "direccion": "Sur"},
            {"id_cliente": 3, "cedula": "030303", "nombres": "Pepe", "apellidos": "Grillo", "telefono": "0777", "email": "pepe@test.com", "direccion": "Norte"},
        ]

        # Le pasamos la lista falsa a la vista
        self.vista.mostrar_tabla(lista_clientes_falsa)