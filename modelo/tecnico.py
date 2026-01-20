from db_config import db_config
import psycopg2

class Tecnico:

    def __init__(self, id_tecnico=None, cedula="", nombres="", apellidos="", especialidad="", telefono=""):
        self.id_tecnico = id_tecnico
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.especialidad = especialidad
        self.telefono = telefono

    def guardar(self):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO tecnico (cedula, nombres, apellidos, especialidad, telefono)
                            VALUES (%s,%s,%s,%s,%s)
                            """, (self.cedula, self.nombres, self.apellidos, self.especialidad, self.telefono))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id_tecnico, cedula, nombres, apellidos, especialidad, telefono
                            FROM tecnico
                            ORDER BY id_tecnico DESC
                            """)
                return [
                    dict(zip(
                        ["id_tecnico","cedula","nombres","apellidos","especialidad","telefono"],
                        row
                    )) for row in cur.fetchall()
                ]
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_tecnico):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM tecnico WHERE id_tecnico=%s", (id_tecnico,))
                conn.commit()
                return True
        except psycopg2.errors.ForeignKeyViolation:
            conn.rollback()
            return False
        except Exception:
            conn.rollback()
            return False
        finally:
            conn.close()