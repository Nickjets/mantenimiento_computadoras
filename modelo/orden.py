from db_config import db_config

class OrdenServicio:

    def __init__(
            self,
            id_orden=None,
            id_equipo=None,
            id_cliente=None,
            id_tecnico=None,
            fecha_estimada_entrega=None,
            estado="RECIBIDO",
            problema_reportado="",
            diagnostico_tecnico="",
            total_estimado=0
    ):
        self.id_orden = id_orden
        self.id_equipo = id_equipo
        self.id_cliente = id_cliente
        self.id_tecnico = id_tecnico
        self.fecha_estimada_entrega = fecha_estimada_entrega
        self.estado = estado
        self.problema_reportado = problema_reportado
        self.diagnostico_tecnico = diagnostico_tecnico
        self.total_estimado = total_estimado

    def guardar(self):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO orden_servicio (
                                id_equipo, id_cliente, id_tecnico,
                                fecha_estimada_entrega, estado,
                                problema_reportado, diagnostico_tecnico,
                                total_estimado
                            )
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                                RETURNING id_orden
                            """, (
                                self.id_equipo,
                                self.id_cliente,
                                self.id_tecnico,
                                self.fecha_estimada_entrega,
                                self.estado,
                                self.problema_reportado,
                                self.diagnostico_tecnico,
                                self.total_estimado
                            ))
                self.id_orden = cur.fetchone()[0]
                conn.commit()
                return self.id_orden
        finally:
            conn.close()

    @staticmethod
    def actualizar_total(id_orden, total):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE orden_servicio
                            SET total_estimado=%s
                            WHERE id_orden=%s
                            """, (total, id_orden))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id_orden, id_equipo, id_cliente, id_tecnico,
                                   fecha_recepcion, fecha_estimada_entrega,
                                   estado, problema_reportado,
                                   diagnostico_tecnico, total_estimado
                            FROM orden_servicio
                            ORDER BY id_orden DESC
                            """)
                return [
                    dict(zip(
                        [
                            "id_orden","id_equipo","id_cliente","id_tecnico",
                            "fecha_recepcion","fecha_estimada_entrega",
                            "estado","problema_reportado",
                            "diagnostico_tecnico","total_estimado"
                        ],
                        row
                    )) for row in cur.fetchall()
                ]
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_orden):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM orden_servicio WHERE id_orden=%s", (id_orden,))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def listar_ordenes():
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT o.id_orden,
                                   c.nombres || ' ' || c.apellidos AS cliente,
                                   e.tipo_equipo || ' ' || e.marca AS equipo,
                                   COALESCE(t.nombres || ' ' || t.apellidos, 'Sin asignar') AS tecnico,
                                   o.estado,
                                   o.fecha_recepcion,
                                   o.fecha_estimada_entrega,
                                   o.problema_reportado,
                                   o.total_estimado
                            FROM orden_servicio o
                                     JOIN cliente c ON c.id_cliente = o.id_cliente
                                     JOIN equipo e ON e.id_equipo = o.id_equipo
                                     LEFT JOIN tecnico t ON t.id_tecnico = o.id_tecnico
                            ORDER BY o.id_orden DESC
                            """)
                return [
                    {
                        "id_orden": r[0],
                        "cliente": r[1],
                        "equipo": r[2],
                        "tecnico": r[3],
                        "estado": r[4],
                        "fecha_recepcion": r[5],
                        "fecha_estimada": r[6],
                        "problema": r[7],
                        "total": r[8] or 0
                    }
                    for r in cur.fetchall()
                ]
        finally:
            conn.close()