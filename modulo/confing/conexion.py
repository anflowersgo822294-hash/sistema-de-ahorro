import mysql.connector
from mysql.connector import Error
import os

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "bzd1eng5tfooqaj4orni-mysql.services.clever-cloud.com"),
            user=os.getenv("DB_USER", "urjmaioxweivcu3l"),
            password=os.getenv("DB_PASSWORD", "uKTWahQxnMw9xcKTzG5C"),
            database=os.getenv("DB_NAME", "bzd1eng5tfooqaj4orni"),
            port=int(os.getenv("DB_PORT", "3306"))
        )
        if conexion.is_connected():
            print("✅ Conexión establecida")
            return conexion
        else:
            print("❌ Conexión fallida (is_connected = False)")
            return None
    except Error as e:
        print(f"❌ Error al conectar: {e}")
        return None
