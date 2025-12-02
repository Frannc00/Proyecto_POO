# src/models/conexion.py
import mysql.connector
from mysql.connector import Error
from src.config.db_config import get_db_config

class Conexion:
    def __init__(self):
        self.config = get_db_config()
        self.conn = None

    def conectar(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            return self.conn
        except Error as e:
            raise ConnectionError(f"No se pudo conectar a la BD: {e}")

    def cerrar(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            self.conn = None
