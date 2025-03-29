import sqlite3 as sql


def criar_db():
    connection = sql.connect('db_usuarios.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_usuarios (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            EMAIL TEXT,
            PASSWORD TEXT,
            NOME TEXT,
            AUTHORIZED INTEGER
        )
    ''')


criar_db()
