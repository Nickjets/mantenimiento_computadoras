import re
from db_config import db_config

class Cliente:
    def __init__(self, id_cliente=None, cedula="", nombres="", apellidos="", telefono="", email="", direccion=""):
        self.id_cliente = id_cliente
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.email = email
        self.direccion = direccion

    # ---------- VALIDACIONES ----------
    @staticmethod
    def validar_cedula_ec(cedula):
        if not cedula.isdigit() or len(cedula) != 10:
            return False
        total = 0
        for i in range(9):
            num = int(cedula[i])
            if i % 2 == 0:
                num *= 2
                if num > 9:
                    num -= 9
            total += num
        verificador = (10 - total % 10) % 10
        return verificador == int(cedula[9])

    @staticmethod
    def validar_email(email):
        return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)

    # ---------- CRUD ----------
    def guardar(self):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            INSERT INTO cliente (cedula, nombres, apellidos, telefono, email, direccion)
                            VALUES (%s,%s,%s,%s,%s,%s)
                            """, (self.cedula, self.nombres, self.apellidos,
                                  self.telefono, self.email, self.direccion))
                conn.commit()
        finally:
            conn.close()

    def actualizar(self):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            UPDATE cliente
                            SET cedula=%s, nombres=%s, apellidos=%s,
                                telefono=%s, email=%s, direccion=%s
                            WHERE id_cliente=%s
                            """, (
                                self.cedula, self.nombres, self.apellidos,
                                self.telefono, self.email, self.direccion,
                                self.id_cliente
                            ))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def eliminar(id_cliente):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM cliente WHERE id_cliente=%s", (id_cliente,))
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def listar_todos():
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id_cliente, cedula, nombres, apellidos, telefono, email, direccion
                            FROM cliente ORDER BY id_cliente DESC
                            """)
                return [
                    dict(zip(
                        ["id_cliente","cedula","nombres","apellidos","telefono","email","direccion"],
                        row
                    )) for row in cur.fetchall()
                ]
        finally:
            conn.close()

    @staticmethod
    def buscar_por_cedula(cedula):
        conn = db_config.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id_cliente, cedula, nombres, apellidos, telefono, email, direccion
                            FROM cliente WHERE cedula=%s
                            """, (cedula,))
                row = cur.fetchone()
                if row:
                    return dict(zip(
                        ["id_cliente","cedula","nombres","apellidos","telefono","email","direccion"],
                        row
                    ))
                return None
        finally:
            conn.close()