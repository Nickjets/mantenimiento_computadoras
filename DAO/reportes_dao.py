class ReportesDAO:

    def __init__(self, conn):
        self.conn = conn

    #1
    def obtener_ordenes_completas(self):
        query = """
                SELECT * FROM vista_ordenes_completas 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    #2
    def obtener_ordenes_activas(self):
        query = """
                SELECT * FROM vista_ordenes_activas 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    #3
    def inventario_bajo(self):
        query = """
                SELECT * FROM vista_inventario_bajo 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    #4
    def rendimiento_tecnicos(self):
        query = """
                SELECT * FROM vista_rendimiento_tecnicos 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    #5
    def servicios_populares(self):
        query = """
                SELECT * FROM vista_servicios_populares 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    #6
    def clientes_frecuentes(self):
        query = """
                SELECT * FROM vista_clientes_frecuentes 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    #7
    def financiero_mensual(self):
        query = """
                SELECT * FROM vista_financiero_mensual 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    #8
    def equipos_abandonados(self):
        query = """
                SELECT * FROM vista_equipos_abandonados 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    #9
    def ingreso_tecnicos(self):
        query = """
                SELECT * FROM vista_ingresos_tecnicos_mes 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    #10
    def servicios_solicitados(self):
        query = """
                SELECT * FROM vista_servicios_mes 
                """
        with self.conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
