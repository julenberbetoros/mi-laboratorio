#!/usr/bin/env python3
"""
Genera contraseñas a partir de 3 palabras por fila, las hashea con bcrypt
y guarda username + hash en SQLite.

Requisitos:
    pip install bcrypt

Uso:
    python crear_hashes_bcrypt.py
"""

import bcrypt        # biblioteca de hashing seguro para contraseñas
import sqlite3       # base de datos ligera
from datetime import datetime  # para guardar fecha/hora de creación

# --- Configuración ---
DB_PATH = "users.db"           # nombre del archivo SQLite
SEPARATOR = "_"                # separador entre palabras para crear la contraseña
STORE_CLEARTEXT_FOR_CLASS = False  # guardar contraseñas en texto plano (solo para demo)

# --- Datos: las 23 respuestas del formulario ---
rows = [
    ("user1", "Mi pez favorito, mi clado taxonomico favorito, un organulo de la celula vegetal"),
    ("user2", "cafe, libro, flor"),
    ("user3", "Apellido, DNI, numero de teléfono"),
    ("user4", "Pacopiso Marzo Cachivache"),
    ("user5", "Nala, Baskonia, Ribabellosa"),
    ("user6", "Barandiaran, Badaia, Alan"),
    ("user7", "Rueda, luz, puerta"),
    ("user8", "Julio, cerveza, fútbol."),
    ("user9", "Croqueta, fentanilo, Mariano"),
    ("user10", "Nombre de mi mascota, nombre de mi equipo de fútbol favorito, nombre de mi jugador favorito"),
    ("user11", "Baskonia, Mus, Gasteiz"),
    ("user12", "Robert, 26/04/2025, Porsche"),
    ("user13", "vitoria, 23, bocajr"),
    ("user14", "Animal,Año,NombreFamiliar"),
    ("user15", "Arrigo Opel Athletic"),
    ("user16", "Mus,Luis,Alaves"),
    ("user17", "cazador, Cuautepec, Bustamante."),
    ("user18", "Duke, Tías, Portátil"),
    ("user19", "Ordenador, letras, mascota"),
    ("user20", "Chivas, paraiso, acámbaro"),
    ("user21", "menditxo,unamuno,blackjack"),
    ("user22", "balón, poker, dinero"),
    ("user23", "Emi, rocallosas, 27/04/04"),
]

# --- Funciones auxiliares ---

def split_into_three(raw_line):
    """
    Divide la cadena original (raw_line) en tres partes.
    Prioriza separar por comas, pero si no hay, lo hace por espacios.
    """
    parts = [p.strip().strip(".") for p in raw_line.split(",")]
    parts = [p for p in parts if p != ""]
    if len(parts) == 3:
        return parts
    # fallback: dividir por palabras y agrupar en 3 trozos
    words = raw_line.replace(".", "").split()
    if len(words) >= 3:
        n = len(words)
        a = " ".join(words[: max(1, n//3)])
        b = " ".join(words[max(1, n//3): 2*max(1, n//3)])
        c = " ".join(words[2*max(1, n//3):])
        return [a.strip(), b.strip(), c.strip()]
    return [raw_line, "", ""]

def make_password(parts, sep=SEPARATOR):
    """
    Une las tres partes para formar una contraseña simple.
    Ejemplo: ["cafe", "libro", "flor"] -> "cafe_libro_flor"
    """
    parts_clean = [p.replace(" ", "") for p in parts]
    return sep.join(parts_clean)

def hash_password_bcrypt(password):
    """
    Genera un hash seguro con bcrypt.
    """
    salt = bcrypt.gensalt(rounds=12)  # cost = 12 (recomendado)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")  # guardar como texto

def verify_password_bcrypt(password, hashed):
    """
    Verifica si una contraseña coincide con su hash.
    """
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

# --- Crear DB ---
def init_db(conn):
    """
    Crea la tabla users si no existe.
    """
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            cleartext_demo TEXT
        );
    """)
    conn.commit()

def insert_user(conn, username, password_hash, cleartext=None):
    """
    Inserta un usuario con su hash en la base de datos.
    """
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO users (username, password_hash, created_at, cleartext_demo)
        VALUES (?, ?, ?, ?)
    """, (username, password_hash, datetime.utcnow().isoformat(), cleartext))
    conn.commit()

# --- Proceso principal ---
def main():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    for uid, raw in rows:
        parts = split_into_three(raw)
        password = make_password(parts)
        hashed = hash_password_bcrypt(password)
        cleartext_store = password if STORE_CLEARTEXT_FOR_CLASS else None
        insert_user(conn, uid, hashed, cleartext_store)
        print(f"{uid}: password='{password}'  -> bcrypt hashed saved")

    print("\nHecho. Base de datos:", DB_PATH)
    print("Ejemplo de verificación: comprobando user1")
    cur = conn.cursor()
    cur.execute("SELECT username, password_hash FROM users WHERE username = ?", ("user1",))
    r = cur.fetchone()
    if r:
        u, h = r
        p_local = make_password(split_into_three(rows[0][1]))
        ok = verify_password_bcrypt(p_local, h)
        print("  verificación de user1:", ok)
    conn.close()

if __name__ == "__main__":
    main()
