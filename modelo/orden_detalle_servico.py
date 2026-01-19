from db_config import db_config

class DetalleOrdenServicio:

    def __init__(
            self,
            id_detalle_serv=None,
            id_orden=None,
            id_servicio=None,
            precio_aplicado=0,
            observacion=""
    ):
        self.id_detalle_serv = id_detalle_serv
        self.id_orden = id_orden
        self.id_servicio = id_servicio
        self.precio_aplicado = precio_aplicado
        self.observacion = observacion

    def guardar(self):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO detalle_orden_servicio
                                (id_orden, id_servicio, precio_aplicado, observacion)
                            VALUES (%s,%s,%s,%s)
                            """, (
                                self.id_orden,
                                self.id_servicio,
                                self.precio_aplicado,
                                self.observacion
                            ))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def listar_por_orden(id_orden):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id_detalle_serv, id_orden, id_servicio,
                                   precio_aplicado, observacion
                            FROM detalle_orden_servicio
                            WHERE id_orden=%s
                            """, (id_orden,))
                return [
                    dict(zip(
                        ["id_detalle_serv","id_orden","id_servicio","precio_aplicado","observacion"],
                        row
                    )) for row in cur.fetchall()
                ]
        finally:
            conn.close()

    @staticmethod
    def listar_por_orden(id_orden):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT s.nombre_servicio,
                                   d.precio_aplicado,
                                   d.observacion
                            FROM detalle_orden_servicio d
                                     JOIN catalogo_servicio s ON s.id_servicio = d.id_servicio
                            WHERE d.id_orden = %s
                            """, (id_orden,))
                return [
                    {
                        "id_orden": id_orden,
                        "servicio": r[0],
                        "precio_aplicado": r[1],
                        "observacion": r[2]
                    }
                    for r in cur.fetchall()
                ]
        finally:
            conn.close()