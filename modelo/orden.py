import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import get_connection

class Orden:
    def crear_orden(self, id_equipo, id_tecnico, problema, fecha_entrega):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            # Estado inicial automático: 'Recibido'
            sql = """INSERT INTO ORDEN_SERVICIO
                     (id_equipo, id_tecnico, problema_reportado, fecha_estimada_entrega, estado)
                     VALUES (%s, %s, %s, %s, 'Recibido')"""
            val = (id_equipo, id_tecnico, problema, fecha_entrega)
            cursor.execute(sql, val)
            conn.commit()
            return True, "✅ Orden generada correctamente."
        except Exception as e:
            return False, f"❌ Error SQL: {e}"
        finally:
            if conn: conn.close()

    def obtener_todas(self):
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            # Traemos datos útiles para la tabla (Join con Equipo y Técnico)
            sql = """
                  SELECT
                      O.id_orden, O.fecha_recepcion, O.estado, O.fecha_estimada_entrega,
                      E.marca, E.modelo,
                      T.nombres as tecnico_nombre
                  FROM ORDEN_SERVICIO O
                           JOIN EQUIPO E ON O.id_equipo = E.id_equipo
                           JOIN TECNICO T ON O.id_tecnico = T.id_tecnico
                  ORDER BY O.id_orden DESC \
                  """
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error listando órdenes: {e}")
            return []
        finally:
            if conn: conn.close()

    def actualizar_estado(self, id_orden, nuevo_estado):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = "UPDATE ORDEN_SERVICIO SET estado = %s WHERE id_orden = %s"
            val = (nuevo_estado, id_orden)
            cursor.execute(sql, val)
            conn.commit()
            return True, f"✅ Estado actualizado a '{nuevo_estado}'."
        except Exception as e:
            return False, f"❌ Error actualizando estado: {e}"
        finally:
            if conn: conn.close()