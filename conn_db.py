import sqlite3 as sql

def conn_db():
    return sql.connect('db_usuarios.db')
