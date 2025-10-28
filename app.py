from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import re
import os
from dotenv import load_dotenv

load_dotenv('config.env')

app = Flask(__name__, 
            template_folder='Inicio_de_sesion_y_registro/templates',
            static_folder='Inicio_de_sesion_y_registro/static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configuración de SQLite (más simple para testing)
def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crear la tabla de usuarios si no existe"""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            fecha_nacimiento DATE,
            genero TEXT,
            acepta_terminos BOOLEAN DEFAULT 0,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Inicializar la base de datos
init_db()

def validar_nombre_apellido(texto):
    if not texto or len(texto.strip()) < 2:
        return False
    return re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', texto.strip()) is not None

def validar_email(email):
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_password(password):
    if not password or len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    return True

def verificar_edad(fecha_nacimiento):
    if not fecha_nacimiento:
        return False
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad >= 18

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre'].strip()
        apellido = request.form['apellido'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        fecha_nacimiento_str = request.form['fecha_nacimiento']
        genero = request.form['genero']
        acepta_terminos = 'acepta_terminos' in request.form
        
        errores = []
        
        if not validar_nombre_apellido(nombre):
            errores.append("El nombre debe tener al menos 2 caracteres y solo letras.")
        
        if not validar_nombre_apellido(apellido):
            errores.append("El apellido debe tener al menos 2 caracteres y solo letras.")
        
        if not validar_email(email):
            errores.append("El formato del email no es válido.")
        
        if not validar_password(password):
            errores.append("La contraseña debe tener al menos 8 caracteres, un número y una mayúscula.")
        
        if password != confirm_password:
            errores.append("Las contraseñas no coinciden.")
        
        if fecha_nacimiento_str:
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
                if not verificar_edad(fecha_nacimiento):
                    errores.append("Debes ser mayor de 18 años para registrarte.")
            except ValueError:
                errores.append("La fecha de nacimiento no es válida.")
        else:
            fecha_nacimiento = None
        
        if genero not in ['masculino', 'femenino', 'otro']:
            errores.append("Debes seleccionar un género válido.")
        
        if not acepta_terminos:
            errores.append("Debes aceptar los términos y condiciones.")
        
        if errores:
            for error in errores:
                flash(error, 'error')
            return redirect(url_for('index'))
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
            if cur.fetchone():
                flash("El email ya está registrado.", 'error')
                conn.close()
                return redirect(url_for('index'))
            
            password_hash = generate_password_hash(password)
            
            cur.execute("""
                INSERT INTO usuarios (nombre, apellido, email, password_hash, fecha_nacimiento, genero, acepta_terminos)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nombre, apellido, email, password_hash, fecha_nacimiento, genero, acepta_terminos))
            
            conn.commit()
            user_id = cur.lastrowid
            cur.close()
            conn.close()
            
            session['user_id'] = user_id
            session['nombre'] = nombre
            session['apellido'] = apellido
            
            flash("¡Registro exitoso! Bienvenido.", 'success')
            return redirect(url_for('exito'))
            
        except Exception as e:
            flash(f"Error en el registro: {str(e)}", 'error')
            return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['login_email'].strip()
        password = request.form['login_password']
        
        if not email or not password:
            flash("Por favor completa todos los campos.", 'error')
            return redirect(url_for('index'))
        
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, apellido, password_hash FROM usuarios WHERE email = ?", (email,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            
            if user and check_password_hash(user[3], password):
                session['user_id'] = user[0]
                session['nombre'] = user[1]
                session['apellido'] = user[2]
                
                flash("¡Inicio de sesión exitoso!", 'success')
                return redirect(url_for('exito'))
            else:
                flash("Email o contraseña incorrectos.", 'error')
                return redirect(url_for('index'))
                
        except Exception as e:
            flash(f"Error en el inicio de sesión: {str(e)}", 'error')
            return redirect(url_for('index'))

@app.route('/exito')
def exito():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", 'error')
        return redirect(url_for('index'))
    
    return render_template('exito.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Has cerrado sesión exitosamente.", 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)