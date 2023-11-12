import sqlite3

try:
    with sqlite3.connect("taller_mecanico_DB.db") as conn:
        mi_cursor = conn.cursor()

        print("Creando clientes")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS clientes \
                          (clave INTEGER PRIMARY KEY, nombre TEXT NOT NULL, \
                          rfc TEXT NOT NULL, correo TEXT NOT NULL, estado INTEGER NOT NULL);")
        
        print("Creando notas")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS notas \
                          (folio INTEGER PRIMARY KEY, fecha TIMESTAMP, \
                          cliente INTEGER NOT NULL, monto INTEGER, estado INTEGER NOT NULL, \
                          FOREIGN KEY(cliente) REFERENCES clientes(clave));")
        
        print("Creando servicios")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS servicios \
                          (clave INTEGER PRIMARY KEY, nombre TEXT NOT NULL, \
                          costo INTEGER NOT NULL, estado INTEGER NOT NULL);")
        
        print("Creando detalles_nota")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS detalles_nota \
                          (folio_nota INTEGER NOT NULL, clave_servicio INTEGER NOT NULL, \
                          FOREIGN KEY (folio_nota) REFERENCES notas(folio), \
                          FOREIGN KEY (clave_servicio) REFERENCES servicios(clave));")
        
        print("Tablas agregadas")
except sqlite3.Error as e:
    print(e)
except Exception as e:
    print(e)
finally:
    if (conn):
        conn.close()
        print("Se ha cerrado la conexión")