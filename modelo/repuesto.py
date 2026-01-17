import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import get_connection

class Repuesto:
    def crear_repuesto(self, nombre, marca, stock, precio):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO REPUESTO (nombre, marca, stock_actual, precio_unitario)
                     VALUES (%s, %s, %s, %s)"""
            val = (nombre, marca, stock, precio)
            cursor.execute(sql, val)
            conn.commit()
            return True, "✅ Repuesto guardado en bodega."
        except Exception as e:
            return False, f"❌ Error SQL: {e}"
        finally:
            if conn: conn.close()

    def obtener_todos(self):
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            sql = "SELECT * FROM REPUESTO ORDER BY nombre ASC"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            if conn: conn.close()