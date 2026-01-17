from vista.vista_ordenes import VistaOrdenes
# from modelo.orden import Orden      <-- DESCOMENTAR EL MARTES
# from modelo.equipo import Equipo    <-- DESCOMENTAR EL MARTES
# from modelo.tecnico import Tecnico  <-- DESCOMENTAR EL MARTES

class OrdenControlador:
    def __init__(self):
        self.vista = VistaOrdenes()
        # self.modelo_orden = Orden() <-- DESCOMENTAR EL MARTES
        # self.modelo_equipo = Equipo()
        # self.modelo_tecnico = Tecnico()

    def ejecutar(self):
        self.vista.mostrar_titulo()

        tab1, tab2 = "📝 Recepción", "🔧 Taller"
        active_tab = self.vista.st.tabs([tab1, tab2]) # Usamos st desde la vista

        # --- PESTAÑA 1: NUEVA ORDEN ---
        with active_tab[0]:
            # DATOS MOCK (SIMULADOS) -
            mapa_equipos = {
                "Dell XPS 13 (Serie: 12345)": 1,
                "HP Pavilion (Serie: 67890)": 2
            }
            mapa_tecnicos = {
                "Juan Pérez (Hardware)": 1,
                "Maria López (Software)": 2
            }

            # DATOS REALES
            # equipos_raw = self.modelo_equipo.obtener_todos_con_propietario()
            # mapa_equipos = {f"{e['marca']} {e['modelo']}": e['id_equipo'] for e in equipos_raw}
            # tecnicos_raw = self.modelo_tecnico.obtener_todos()
            # mapa_tecnicos = {t['nombres']: t['id_tecnico'] for t in tecnicos_raw}

            datos_form = self.vista.mostrar_formulario_creacion(mapa_equipos, mapa_tecnicos)

            if datos_form:
                # LÓGICA DE GUARDADO
                # self.modelo_orden.crear_orden(...) <-- REAL
                self.vista.exito(f"Simulación: Orden creada para {datos_form['key_equipo']}")

        # --- PESTAÑA 2: GESTIÓN Y ACTUALIZACIÓN ---
        with active_tab[1]:
            # DATOS MOCK (SIMULADOS)
            lista_ordenes = [
                {"id_orden": 101, "fecha": "2023-10-25", "estado": "Recibido", "modelo": "Dell XPS", "tecnico_nombre": "Juan"},
                {"id_orden": 102, "fecha": "2023-10-24", "estado": "Diagnóstico", "modelo": "HP Pavilion", "tecnico_nombre": "Maria"},
                {"id_orden": 103, "fecha": "2023-10-20", "estado": "Listo para Retiro", "modelo": "Macbook Air", "tecnico_nombre": "Pedro"},
            ]

            # DATOS REALES
            # lista_ordenes = self.modelo_orden.obtener_todas()

            datos_update = self.vista.mostrar_bandeja_gestion(lista_ordenes)

            if datos_update:
                id_orden = datos_update["id_orden"]
                estado = datos_update["nuevo_estado"]

                # LÓGICA DE ACTUALIZACIÓN
                # exito, msg = self.modelo_orden.actualizar_estado(id_orden, estado) <-- REAL
                # if exito: self.vista.exito(msg)

                # SIMULACIÓN
                if estado == "Entregado":
                    self.vista.exito(f"🎉 Orden #{id_orden} entregada al cliente. ¡Proceso cerrado!")
                else:
                    self.vista.exito(f"Simulación: Estado de Orden #{id_orden} cambiado a '{estado}'.")