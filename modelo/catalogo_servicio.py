from db_config import db_config

class CatalogoServicio:

    def __init__(self, id_servicio=None, nombre_servicio="", precio_base=0, descripcion=""):
        self.id_servicio = id_servicio
        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base
        self.descripcion = descripcion

    def guardar(self):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO catalogo_servicio (nombre_servicio, precio_base, descripcion)
                            VALUES (%s,%s,%s)
                            """, (self.nombre_servicio, self.precio_base, self.descripcion))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id_servicio, nombre_servicio, precio_base, descripcion
                            FROM catalogo_servicio
                            ORDER BY id_servicio DESC
                            """)
                return [
                    dict(zip(
                        ["id_servicio","nombre_servicio","precio_base","descripcion"],
                        row
                    )) for row in cur.fetchall()
                ]
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_servicio):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM catalogo_servicio WHERE id_servicio=%s", (id_servicio,))
                conn.commit()
        finally:
            conn.close()
