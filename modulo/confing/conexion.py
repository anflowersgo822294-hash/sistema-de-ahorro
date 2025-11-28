import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host='bzd1eng5tfooqaj4orni-mysql.services.clever-cloud.com',
            user='urjmaioxweivcu3l',
            password='uKTWahQxnMw9xcKTzG5C',
            database='bzd1eng5tfooqaj4orni',
            port=3306
        )
        if conexion.is_connected():
            print("✅ Conexión establecida")
            return conexion
        else:
            print("❌ Conexión fallida (is_connected = False)")
            return None
    except mysql.connector.Error as e:
        print(f"❌ Error al conectar: {e}")
        return None

