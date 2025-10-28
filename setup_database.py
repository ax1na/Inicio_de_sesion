import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv('config.env')

def create_database():
    connection = None
    try:
        print(f"Conectando a MySQL en {os.getenv('MYSQL_HOST')}...")
        print(f"Usuario: {os.getenv('MYSQL_USER')}")
        print(f"Base de datos: {os.getenv('MYSQL_DB')}")
        
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD')
        )
        
        if connection.is_connected():
            print("✓ Conexión exitosa a MySQL")
            cursor = connection.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DB')}")
            print(f"✓ Base de datos '{os.getenv('MYSQL_DB')}' creada o ya existente.")
            
            cursor.execute(f"USE {os.getenv('MYSQL_DB')}")
            
            create_table_query = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL,
                apellido VARCHAR(50) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                fecha_nacimiento DATE,
                genero ENUM('masculino', 'femenino', 'otro'),
                acepta_terminos BOOLEAN DEFAULT FALSE,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_table_query)
            print("✓ Tabla 'usuarios' creada exitosamente.")
            
            connection.commit()
            cursor.close()
            
    except Error as e:
        print(f"✗ Error conectando a MySQL: {e}")
        print("\nVerifica que:")
        print("1. MySQL esté ejecutándose")
        print("2. Las credenciales en config.env sean correctas")
        print("3. El usuario tenga permisos suficientes")
        return False
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("✓ Conexión a MySQL cerrada.")
    
    return True

if __name__ == "__main__":
    create_database()