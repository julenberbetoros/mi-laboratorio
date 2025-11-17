import sqlite3
import mysql.connector

# --- Conexión SQLite ---
sqlite_conn = sqlite3.connect('users.db')
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT username, password_hash, created_at FROM users")
usuarios = sqlite_cursor.fetchall()
sqlite_cursor.close()
sqlite_conn.close()

# --- Conexión MySQL ---
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="labuser",
    password="labpass",
    database="laboratorio"
)

mysql_cursor = mysql_conn.cursor()

# Insertar usuarios
for username, password_hash, created_at in usuarios:
    mysql_cursor.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (%s, %s, %s)",
        (username, password_hash, created_at)
    )

mysql_conn.commit()
mysql_cursor.close()
mysql_conn.close()

print("Migración completada: todos los usuarios con bcrypt han sido insertados en MySQL.")

