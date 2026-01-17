import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import get_connection

class Tecnico:
    def obtener_todos(self):
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            sql = "SELECT id_tecnico, nombres, especialidad FROM TECNICO"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error cargando técnicos: {e}")
            return []
        finally:
            if conn: conn.close()