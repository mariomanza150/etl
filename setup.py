import pyodbc
from config import *
from setup_data import *
import mysql.connector

# Metodo de Creacion de BD y Tablas
def check_create():
    # Conexion a Microsoft SQL para Libreria
    conn = pyodbc.connect(winsql['string'], autocommit=True)

    # Listar Bases de Datos y crear en caso de no existir
    cur = conn.cursor()
    dbs = [x[0] for x in cur.execute("SELECT name FROM sys.databases;")]
    
    if "BarnesNoble" not in dbs:
        cur.execute("CREATE DATABASE BarnesNoble;") # Crear BD

        with open("barnes_noble.txt") as table_querys: # Leer y ejecutar Create TABLES
            cur.execute(table_querys.read())

    cur.close() # Cerrar Conexion
    conn.close()
    # Conexion a MySQL para Electronica
    conn = mysql.connector.connect(
        host=sql['host'],
        user=sql['user'],
        password=sql['password']
    )
    
    cur = conn.cursor()
    cur.execute("SHOW DATABASES")
    dbs = [x[0] for x in cur]
    
    if "eluktronics" not in dbs:
        cur.execute("CREATE DATABASE eluktronics;")

        with open("electronics.txt") as table_querys:
            cur.execute(table_querys.read(), multi=True)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_create()
    main()