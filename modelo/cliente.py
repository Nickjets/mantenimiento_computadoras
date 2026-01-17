import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import get_connection

class Cliente:
    def crear_cliente(self, cedula, nombres, apellidos, telefono, email, direccion):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO CLIENTE (cedula, nombres, apellidos, telefono, email, direccion)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            val = (cedula, nombres, apellidos, telefono, email, direccion)
            cursor.execute(sql, val)
            conn.commit()
            return True, "✅ Cliente registrado correctamente."
        except Exception as e:
            return False, f"❌ Error SQL: {e}"
        finally:
            if conn: conn.close()

    def obtener_todos(self):
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # Ordenamos por apellidos para que la lista se vea ordenada
            cursor.execute("SELECT * FROM CLIENTE ORDER BY apellidos ASC")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []
        finally:
            if conn: conn.close()