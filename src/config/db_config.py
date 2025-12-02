# src/config/db_config.py
import os

# Opcional: leer variables de entorno si preferís (ej: en producción)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "root")
DB_NAME = os.getenv("DB_NAME", "gestion_ventas")

def get_db_config():
    return {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASS,
        "database": DB_NAME,
        "auth_plugin": "mysql_native_password"
    }
