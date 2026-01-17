import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import get_connection

class Equipo:
    def crear_equipo(self, id_cliente, tipo, marca, modelo, serie, observaciones):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO EQUIPO (id_cliente, tipo_equipo, marca, modelo, numero_serie, observaciones_fisicas)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            val = (id_cliente, tipo, marca, modelo, serie, observaciones)
            cursor.execute(sql, val)
            conn.commit()
            return True, "✅ Equipo registrado exitosamente."
        except Exception as e:
            return False, f"❌ Error al guardar equipo: {e}"
        finally:
            if conn: conn.close()

    def obtener_todos_con_propietario(self):
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # JOIN CLAVE: Unimos EQUIPO con CLIENTE
            sql = """
                  SELECT
                      E.id_equipo, E.tipo_equipo, E.marca, E.modelo, E.numero_serie,
                      CONCAT(C.nombres, ' ', C.apellidos) AS dueno_nombre,
                      E.observaciones_fisicas
                  FROM EQUIPO E
                           JOIN CLIENTE C ON E.id_cliente = C.id_cliente
                  ORDER BY E.id_equipo DESC \
                  """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error listando equipos: {e}")
            return []
        finally:
            if conn: conn.close()