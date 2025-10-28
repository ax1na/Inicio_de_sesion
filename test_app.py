# Script de prueba para verificar la funcionalidad de la aplicación Flask

import requests
import json
from datetime import datetime, timedelta

def test_connection():
    """Prueba la conexión básica a la aplicación"""
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Conexión exitosa a la aplicación")
            return True
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ No se pudo conectar a la aplicación: {e}")
        return False

def test_registration():
    """Prueba el registro de un usuario"""
    test_user = {
        'nombre': 'Usuario',
        'apellido': 'Prueba',
        'email': f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
        'password': 'TestPass123',
        'confirm_password': 'TestPass123',
        'fecha_nacimiento': (datetime.now() - timedelta(days=365*25)).strftime('%Y-%m-%d'),
        'genero': 'otro',
        'acepta_terminos': 'on'
    }
    
    try:
        response = requests.post('http://localhost:5000/registro', data=test_user, timeout=10)
        if response.status_code == 302: 
            print("✅ Registro de usuario exitoso")
            return test_user['email']
        else:
            print(f"❌ Error en el registro: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la solicitud de registro: {e}")
        return None

def test_login(email):
    """Prueba el inicio de sesión"""
    login_data = {
        'login_email': email,
        'login_password': 'TestPass123'
    }
    
    try:
        response = requests.post('http://localhost:5000/login', data=login_data, timeout=10)
        if response.status_code == 302: 
            print("✅ Inicio de sesión exitoso")
            return True
        else:
            print(f"❌ Error en el inicio de sesión: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la solicitud de login: {e}")
        return False

def test_protected_route():
    """Prueba el acceso a una ruta protegida"""
    try:
        response = requests.get('http://localhost:5000/exito', timeout=5)
        if response.status_code == 302: 
            print("✅ Ruta protegida correctamente protegida")
            return True
        else:
            print(f"❌ Ruta protegida accesible sin autenticación: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al probar ruta protegida: {e}")
        return False

def run_tests():
    """Ejecuta todas las pruebas"""
    print("🚀 Iniciando pruebas de la aplicación Flask...")
    print("=" * 50)
    
    if not test_connection():
        print("❌ La aplicación no está ejecutándose. Ejecuta 'python app.py' primero.")
        return
    
    test_protected_route()
    
    email = test_registration()
    if not email:
        print("❌ No se pudo completar el registro")
        return
    
    if test_login(email):
        print("✅ Todas las pruebas básicas pasaron exitosamente")
    else:
        print("❌ Falló el inicio de sesión")
    
    print("=" * 50)
    print("📝 Nota: Para probar la funcionalidad completa, abre http://localhost:5000 en tu navegador")

if __name__ == "__main__":
    print("🔧 Script de prueba para la aplicación Flask de Autenticación")
    print("⚠️  Asegúrate de que la aplicación esté ejecutándose en http://localhost:5000")
    print()
    
    response = input("¿Deseas ejecutar las pruebas? (s/n): ").lower()
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        run_tests()
    else:
        print("❌ Pruebas canceladas")