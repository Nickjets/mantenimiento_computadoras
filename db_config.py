import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import pool  # Opcional: para connection pool

load_dotenv()

class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'admin')
        self.database = os.getenv('DB_NAME', 'CompuServicio')
        self.port = os.getenv('DB_PORT', '5433')  # PostgreSQL usa puerto 5432 por defecto

    def get_connection(self):
        """Obtiene una conexión a PostgreSQL"""
        try:
            connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return connection
        except psycopg2.Error as e:
            print(f"Error al conectar a PostgreSQL: {e}")
            raise

    def get_connection_pool(self, min_conn=1, max_conn=10):
        """Crea un pool de conexiones (opcional, para mejor rendimiento)"""
        try:
            return psycopg2.pool.SimpleConnectionPool(
                min_conn, max_conn,
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
        except psycopg2.Error as e:
            print(f"Error al crear pool de conexiones: {e}")
            raise

# Instancia global
db_config = DatabaseConfig()