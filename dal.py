import sqlite3

def metodo_general(path, accion):
    with sqlite3.connect(path) as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")
        cursor = conexion.cursor()
        resultado = accion(cursor)
        conexion.commit()
        return resultado

def crear_tablas(path, borrar_existentes=True):
    def accion(cursor):
        if borrar_existentes:
            cursor.execute("DROP TABLE IF EXISTS entradas")
            cursor.execute("DROP TABLE IF EXISTS peliculas")
            cursor.execute("DROP TABLE IF EXISTS sala")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sala(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                capacidad INTEGER NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS peliculas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                horario TEXT NOT NULL,
                sala_id INTEGER,
                FOREIGN KEY (sala_id) REFERENCES sala(id),
                UNIQUE (sala_id, horario)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entradas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                pelicula_id INTEGER,
                FOREIGN KEY (pelicula_id) REFERENCES peliculas(id)
            )
        ''')
    return metodo_general(path, accion)

def inserta_sala(path, nombre, capacidad):
    def accion(cursor):
        cursor.execute("INSERT INTO sala (nombre, capacidad) VALUES (?, ?)", (nombre, capacidad))
    return metodo_general(path, accion)

def traer_salas(path):
    def accion(cursor):
        cursor.execute("SELECT * FROM sala")
        return cursor.fetchall()
    return metodo_general(path, accion)

def inserta_pelicula(path, titulo, horario, sala_id):
    def accion(cursor):
        cursor.execute(
            "INSERT INTO peliculas (titulo, horario, sala_id) VALUES (?, ?, ?)",
            (titulo, horario, sala_id)
        )
    return metodo_general(path, accion)

def traer_peliculas(path):
    def accion(cursor):
        cursor.execute("SELECT * FROM peliculas")
        return cursor.fetchall()
    return metodo_general(path, accion)

def inserta_entrada(path, cliente, cantidad, pelicula_id):
    def accion(cursor):
        cursor.execute(
            "INSERT INTO entradas (cliente, cantidad, pelicula_id) VALUES (?, ?, ?)",
            (cliente, cantidad, pelicula_id)
        )
    return metodo_general(path, accion)

def traer_entradas_por_cliente(path, cliente):
    def accion(cursor):
        cursor.execute(
            "SELECT * FROM entradas WHERE cliente = ?",
            (cliente,)
        )
        return cursor.fetchall()
    return metodo_general(path, accion)
