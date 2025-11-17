import sqlite3
from argon2 import PasswordHasher
import mysql.connector

# Inicializa Argon2
ph = PasswordHasher()

# --- Conexión SQLite ---
sqlite_conn = sqlite3.connect('users.db')
sqlite_cursor = sqlite_conn.cursor()

# Obtener todos los usuarios
sqlite_cursor.execute("SELECT username, cleartext, created_at FROM users")
usuarios = sqlite_cursor.fetchall()

sqlite_cursor.close()
sqlite_conn.close()

# --- Conexión MySQL ---
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",          # Cambia si tu usuario es otro
    password="tu_password",
    database="laboratorio"  # Asegúrate de haber creado la BD
)

mysql_cursor = mysql_conn.cursor()

# Crear tabla en MySQL si no existe
mysql_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL
)
""")

# Insertar usuarios con hashes argon2
for username, cleartext, created_at in usuarios:
    hash_argon2 = ph.hash(cleartext)
    mysql_cursor.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (%s, %s, %s)",
        (username, hash_argon2, created_at)
    )

mysql_conn.commit()
mysql_cursor.close()
mysql_conn.close()

print("Migración completada: todos los usuarios han sido insertados en MySQL con argon2.")

