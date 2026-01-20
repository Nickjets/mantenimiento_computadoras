import pandas as pd
from typing import List, Dict, Any
import db_config

class ReportesDAO:
    def __init__(self):
        self.connection = db_config.db_config.get_connection()

    def _ejecutar_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """Me  todo genérico para ejecutar queries y devolver resultados como diccionarios"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            cursor.close()

            # Convertir a lista de diccionarios
            resultados = []
            for row in rows:
                resultados.append(dict(zip(column_names, row)))

            return resultados

        except Exception as e:
            print(f"Error en query: {str(e)}")
            return []


    def _ejecutar_query_dataframe(self, query: str, params: tuple = None) -> pd.DataFrame:
        """Ejecuta query y devuelve DataFrame"""
        resultados = self._ejecutar_query(query, params)
        return pd.DataFrame(resultados) if resultados else pd.DataFrame()



    # 1. Vista para órdenes de servicio con información completa
    def obtener_ordenes_completas(self, estado: str = None, fecha_desde: str = None, fecha_hasta: str = None):
        query = """
                SELECT * FROM vista_ordenes_completas
                WHERE 1=1 \
                """
        params = []

        if estado:
            query += " AND estado = %s"
            params.append(estado)

        if fecha_desde:
            query += " AND fecha_recepcion >= %s"
            params.append(fecha_desde)

        if fecha_hasta:
            query += " AND fecha_recepcion <= %s"
            params.append(fecha_hasta)

        query += " ORDER BY fecha_recepcion DESC"

        return self._ejecutar_query_dataframe(query, tuple(params) if params else None)

    # 2. Vista para órdenes pendientes/activas
    def obtener_ordenes_activas(self, tecnico_id: int = None):
        query = """
                SELECT * FROM vista_ordenes_activas
                WHERE 1=1 \
                """
        params = []

        if tecnico_id:
            query += " AND id_tecnico = %s"
            params.append(tecnico_id)

        query += " ORDER BY dias_restantes ASC, fecha_recepcion DESC"

        return self._ejecutar_query_dataframe(query, tuple(params) if params else None)

    # 3. Vista para inventario bajo de stock
    def inventario_bajo(self, nivel_stock: str = None, marca: str = None):
        query = """
                SELECT * FROM vista_inventario_bajo
                WHERE 1=1 \
                """
        params = []

        if nivel_stock:
            query += " AND nivel_stock = %s"
            params.append(nivel_stock)

        if marca:
            query += " AND marca ILIKE %s"
            params.append(f"%{marca}%")

        query += " ORDER BY stock_actual ASC"

        return self._ejecutar_query_dataframe(query, tuple(params) if params else None)

    # 4. Vista para reporte de técnicos (productividad)
    def rendimiento_tecnicos(self, fecha_desde: str = None, fecha_hasta: str = None):
        query = """
                SELECT * FROM vista_rendimiento_tecnicos
                WHERE 1=1 \
                """
        params = []

        # Nota: La vista ya filtra últimos 90 días, pero podemos añadir filtros adicionales
        if fecha_desde or fecha_hasta:
            # En este caso, necesitaríamos modificar la vista o usar subquery
            # Por simplicidad, omitimos este filtro para esta vista
            pass

        query += " ORDER BY total_facturado DESC"

        return self._ejecutar_query_dataframe(query, tuple(params) if params else None)

    # 5. Vista para servicios más solicitados
    def servicios_populares(self, top_n: int = None):
        query = """
                SELECT * FROM vista_servicios_populares
                ORDER BY veces_solicitado DESC \
                """

        df = self._ejecutar_query_dataframe(query)

        if top_n and not df.empty:
            df = df.head(top_n)

        return df

    # 6. Vista para clientes frecuentes
    def clientes_frecuentes(self, min_ordenes: int = None, min_gasto: float = None):
        query = """
                SELECT * FROM vista_clientes_frecuentes
                WHERE 1=1 \
                """
        params = []

        if min_ordenes:
            query += " AND total_ordenes >= %s"
            params.append(min_ordenes)

        if min_gasto:
            query += " AND total_gastado >= %s"
            params.append(min_gasto)

        query += " ORDER BY total_gastado DESC NULLS LAST"

        return self._ejecutar_query_dataframe(query, tuple(params) if params else None)

    # 7. Vista para reporte financiero mensual
    def financiero_mensual(self, meses_atras: int = 12):
        query = """
                SELECT * FROM vista_financiero_mensual
                """
        return self._ejecutar_query_dataframe(query, (meses_atras,))

    # 8. Vista de equipos 'Abandonados'
    def equipos_abandonados(self, nivel_alerta: str = None, dias_minimo: int = None):
        query = """
                SELECT * FROM vista_equipos_abandonados
                WHERE 1=1 \
                """
        params = []

        if nivel_alerta:
            query += " AND nivel_alerta = %s"
            params.append(nivel_alerta)

        if dias_minimo:
            query += " AND dias_en_taller >= %s"
            params.append(dias_minimo)

        query += " ORDER BY dias_en_taller DESC"

        return self._ejecutar_query_dataframe(query, tuple(params) if params else None)

    # 9. Vista de Ingresos por Técnico del Mes Actual
    def ingreso_tecnicos(self):
        query = """
                SELECT * FROM vista_ingresos_tecnicos_mes
                ORDER BY ordenes_atendidas_mes DESC \
                """

        return self._ejecutar_query_dataframe(query)

    # 10. Vista de Servicios Solicitados en el Mes Actual
    def servicios_solicitados(self):
        query = """
                SELECT * FROM vista_servicios_mes
                WHERE veces_solicitado_mes > 0
                ORDER BY veces_solicitado_mes DESC \
                """

        return self._ejecutar_query_dataframe(query)

    # Métodos adicionales para estadísticas
    def obtener_estadisticas_generales(self):
        """Obtiene estadísticas generales para el dashboard"""
        estadisticas = {}

        try:
            cursor = self.connection.cursor()

            # Total órdenes activas
            cursor.execute("SELECT COUNT(*) FROM vista_ordenes_activas")
            estadisticas['ordenes_activas'] = cursor.fetchone()[0]

            # Repuestos críticos
            cursor.execute("""
                           SELECT COUNT(*) FROM vista_inventario_bajo
                           WHERE nivel_stock IN ('AGOTADO', 'CRÍTICO')
                           """)
            estadisticas['repuestos_criticos'] = cursor.fetchone()[0]

            # Equipos abandonados
            cursor.execute("SELECT COUNT(*) FROM vista_equipos_abandonados")
            estadisticas['equipos_abandonados'] = cursor.fetchone()[0]

            # Ingresos mes actual
            cursor.execute("""
                           SELECT COALESCE(SUM(ingresos_totales), 0)
                           FROM vista_financiero_mensual
                           WHERE EXTRACT(MONTH FROM mes) = EXTRACT(MONTH FROM CURRENT_DATE)
                             AND EXTRACT(YEAR FROM mes) = EXTRACT(YEAR FROM CURRENT_DATE)
                           """)
            estadisticas['ingresos_mes_actual'] = cursor.fetchone()[0] or 0

            # Clientes nuevos este mes
            cursor.execute("""
                           SELECT COUNT(*) FROM cliente
                           WHERE DATE_TRUNC('month', CURRENT_DATE) = DATE_TRUNC('month', CURRENT_TIMESTAMP)
                           """)
            estadisticas['clientes_nuevos_mes'] = cursor.fetchone()[0]

            cursor.close()

        except Exception as e:
            print(f"Error obteniendo estadísticas: {str(e)}")

        return estadisticas

    def obtener_ordenes_por_estado(self):
        """Obtiene distribución de órdenes por estado"""
        query = """
                SELECT estado, COUNT(*) as cantidad
                FROM orden_servicio
                GROUP BY estado
                ORDER BY cantidad DESC \
                """

        return self._ejecutar_query_dataframe(query)

    def obtener_tendencias_mensuales(self, meses: int = 6):
        """Obtiene tendencias de órdenes e ingresos últimos N meses"""
        query = """
                SELECT
                    DATE_TRUNC('month', fecha_recepcion) as mes,
                    TO_CHAR(DATE_TRUNC('month', fecha_recepcion), 'Mon YYYY') as mes_nombre,
                    COUNT(*) as ordenes,
                    COALESCE(SUM(total_estimado), 0) as ingresos
                FROM orden_servicio
                WHERE fecha_recepcion >= CURRENT_DATE - INTERVAL '%s months'
                  AND estado = 'ENTREGADO'
                GROUP BY DATE_TRUNC('month', fecha_recepcion)
                ORDER BY mes \
                """

        return self._ejecutar_query_dataframe(query, (meses,))