from db_config import db_config

class DetalleOrdenRepuesto:

    def __init__(
            self,
            id_detalle_repuesto=None,
            id_orden=None,
            id_repuesto=None,
            cantidad=1,
            precio_venta=0
    ):
        self.id_detalle_repuesto = id_detalle_repuesto
        self.id_orden = id_orden
        self.id_repuesto = id_repuesto
        self.cantidad = cantidad
        self.precio_venta = precio_venta

    def guardar(self):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO detalle_orden_repuesto
                                (id_orden, id_repuesto, cantidad, precio_venta)
                            VALUES (%s,%s,%s,%s)
                            """, (
                                self.id_orden,
                                self.id_repuesto,
                                self.cantidad,
                                self.precio_venta
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
                            SELECT id_detalle_repuesto, id_orden,
                                   id_repuesto, cantidad, precio_venta
                            FROM detalle_orden_repuesto
                            WHERE id_orden=%s
                            """, (id_orden,))
                return [
                    dict(zip(
                        ["id_detalle_repuesto","id_orden","id_repuesto","cantidad","precio_venta"],
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
                            SELECT r.nombre,
                                   d.cantidad,
                                   d.precio_venta
                            FROM detalle_orden_repuesto d
                                     JOIN repuesto r ON r.id_repuesto = d.id_repuesto
                            WHERE d.id_orden = %s
                            """, (id_orden,))
                return [
                    {
                        "id_orden": id_orden,
                        "repuesto": r[0],
                        "cantidad": r[1],
                        "precio_venta": r[2]
                    }
                    for r in cur.fetchall()
                ]
        finally:
            conn.close()