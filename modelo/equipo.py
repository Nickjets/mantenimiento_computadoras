from db_config import db_config

class equipo:
    def __init__(
            self,
            id_equipo=None,
            id_cliente=None,
            tipo_equipo="",
            marca="",
            modelo="",
            numero_serie="",
            observaciones_fisicas=""
    ):
        self.id_equipo = id_equipo
        self.id_cliente = id_cliente
        self.tipo_equipo = tipo_equipo
        self.marca = marca
        self.modelo = modelo
        self.numero_serie = numero_serie
        self.observaciones_fisicas = observaciones_fisicas

    # ---------- CRUD ----------

    def guardar(self):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO equipo (
                                id_cliente, tipo_equipo, marca, modelo,
                                numero_serie, observaciones_fisicas
                            )
                            VALUES (%s,%s,%s,%s,%s,%s)
                            """, (
                                self.id_cliente,
                                self.tipo_equipo,
                                self.marca,
                                self.modelo,
                                self.numero_serie,
                                self.observaciones_fisicas
                            ))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        """
        Lista equipos con datos del cliente (JOIN)
        """
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT
                                e.id_equipo,
                                c.id_cliente,
                                c.nombres || ' ' || c.apellidos AS cliente,
                                e.tipo_equipo,
                                e.marca,
                                e.modelo,
                                e.numero_serie,
                                e.observaciones_fisicas
                            FROM equipo e
                                     JOIN cliente c ON c.id_cliente = e.id_cliente
                            ORDER BY e.id_equipo DESC
                            """)
                return [
                    dict(zip(
                        [
                            "id_equipo",
                            "id_cliente",
                            "cliente",
                            "tipo_equipo",
                            "marca",
                            "modelo",
                            "numero_serie",
                            "observaciones_fisicas"
                        ],
                        row
                    )) for row in cur.fetchall()
                ]
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_equipo):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM equipo WHERE id_equipo=%s", (id_equipo,))
                conn.commit()
        finally:
            conn.close()