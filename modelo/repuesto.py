from db_config import db_config

class Repuesto:

    def __init__(self, id_repuesto=None, nombre="", marca="", stock_actual=0, precio_unitario=0):
        self.id_repuesto = id_repuesto
        self.nombre = nombre
        self.marca = marca
        self.stock_actual = stock_actual
        self.precio_unitario = precio_unitario

    def guardar(self):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO repuesto (nombre, marca, stock_actual, precio_unitario)
                            VALUES (%s,%s,%s,%s)
                            """, (self.nombre, self.marca, self.stock_actual, self.precio_unitario))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id_repuesto, nombre, marca, stock_actual, precio_unitario
                            FROM repuesto
                            ORDER BY id_repuesto DESC
                            """)
                return [
                    dict(zip(
                        ["id_repuesto","nombre","marca","stock_actual","precio_unitario"],
                        row
                    )) for row in cur.fetchall()
                ]
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_repuesto):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM repuesto WHERE id_repuesto=%s", (id_repuesto,))
                conn.commit()
        finally:
            conn.close()
