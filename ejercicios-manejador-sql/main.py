import sqlite3
import os

ui = ['Crear tabla', 'Seleccionar tabla','Cerrar sesion']
opt_tabla = ['Ingresar nuevos datos', 'Buscar datos', 'Eliminar fila', 'Borrar Tabla', 'Volver']
def crear_db(name_db, dt_db):
    conn = sqlite3.connect('ejemplo_bd.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name_db}'")
    if cursor.fetchone():
        print(f"La tabla '{name_db}' ya existe.")
        return
    columnas = ", ".join([f"{col_name} {col_type} {nulo}" for col_name, col_type, nulo in dt_db])
    query = f'''
        CREATE TABLE {name_db} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {columnas}
        )
    '''
    cursor.execute(query)
    conn.commit() 
    print(f"Tabla '{name_db}' creada exitosamente.")
    conn.close()

def list_tablas():
    conn = sqlite3.connect('ejemplo_bd.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
    tablas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tablas 

def tabla(name, x):
    conn = sqlite3.connect('ejemplo_bd.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f"PRAGMA table_info({name})") 
        columnas = cursor.fetchall()
        if columnas:
            if int(x) == 1: print(f"Columnas de la tabla '{name}':")
            for columna in columnas:
                if int(x) == 1:
                    print(f"- {columna[1]} [{columna[2]} - {columna[3]}]")
            return [columna[1] for columna in columnas]
        else:
            print(f"La tabla '{name}' no tiene columnas.")
            return []
    except sqlite3.Error as e:
        print(f"Error al consultar la tabla '{name}': {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def ingresar(name, datos, columnas):
    conn = sqlite3.connect('ejemplo_bd.db')
    cursor = conn.cursor()
    try:
        query = f"INSERT INTO {name} ({', '.join(columnas)}) VALUES ({', '.join(['?' for _ in columnas])})"
        cursor.execute(query, datos)
        conn.commit()  
        print(f"Datos insertados correctamente en la tabla '{name}'.")
    except sqlite3.Error as e:
        print(f"Error al insertar datos en la tabla '{name}': {e}")
    finally:
        cursor.close()
        conn.close() 

def consult_all(name_tb, col, name):
    conn = sqlite3.connect('ejemplo_bd.db')
    cursor = conn.cursor()
    query = (f'SELECT * FROM {name_tb} WHERE {col} = ?')
    cursor.execute(query, (name,))
    x = cursor.fetchall()
    cursor.close()
    conn.close()
    return x 

def dlt_fila(name_tb, column_name, value):
    conn = sqlite3.connect('ejemplo_bd.db')
    cursor = conn.cursor()
    try:
        query = f"DELETE FROM {name_tb} WHERE {column_name} = ?"
        cursor.execute(query, (value,))
        conn.commit()  
        print(f"Fila eliminada correctamente de la tabla '{name_tb}'.")
    except sqlite3.Error as e:
        print(f"Error al eliminar la fila de la tabla '{name_tb}': {e}")
    finally:
        cursor.close()
        conn.close()

def dlt_tb(name_tb):
    conn = sqlite3.connect('ejemplo_bd.db')
    cursor = conn.cursor()
    try:
        query = f"DROP TABLE IF EXISTS {name_tb}"
        cursor.execute(query)
        conn.commit()  
        print(f"Tabla '{name_tb}' eliminada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al eliminar la tabla '{name_tb}': {e}")
    finally:
        cursor.close()
        conn.close()

while True:
    os.system('cls' if os.name == 'nt' else 'clear')  
    print(f'\n{" Gestor de base de datos ":=^50}\n')
    for index, opt in enumerate(ui, start=1):
        print(f"[{index}] {opt}")

    x = input(f"Que deseas hacer?\n-> ")

    if x == "1":  # Crear tb
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"La tabla por defecto tendrá un ID\n que será 'PRIMARY KEY' y será 'AUTOINCREMENT'.\n")
        opt = input(f"Nombre de la tabla: ")
        x = int(input(f"¿Cuántos datos tendrá? "))
        datos = []
        type_datos = ["TEXT", "INTEGER", "TEXT UNIQUE"]
        for i in range(x):
            dt = input(f"Ingrese el nombre del dato [{i + 1}]:\n-> ").lower()
            type_dt = input(f"Tipo de dato [TEXT - INTEGER - TEXT UNIQUE]:\n-> ").upper()
            if type_dt not in type_datos:
                print("Tipo de dato no válido. Operación cancelada.")
                break
            x = input(f"¿Es NOT NULL? [y/n]:\n-> ").lower()
            x = "NOT NULL" if x == "y" else ""
            datos.append((dt, type_dt, x))
        else:  
            try:
                crear_db(opt, datos)
            except sqlite3.Error as e:
                print(f"Error al crear la base de datos: {e}")

    if x == "2":  # Select tb
        os.system('cls' if os.name == 'nt' else 'clear') #posix
        print(f'\n{" Tablas disponibles ":=^50}\n')
        tablas = list_tablas()
        if tablas:
            os.system('cls' if os.name == 'nt' else 'clear')
            for i, t in enumerate(tablas, start=1):
                print(f"[{i}] {t[0]}")
            try:
                dt = int(input(f"Seleccione una tabla (número):\n-> "))
                if 1 <= dt <= len(tablas):
                    tabla_seleccionada = tablas[dt - 1][0]
                    while True:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print(f'\n{" Operaciones disponibles ":=^50}\n')
                        print(f"- Tabla seleccionada: {tabla_seleccionada}")
                        for i, opt in enumerate(opt_tabla, start=1):
                            print(f"[{i}] {opt}")
                        
                        x = input("Que deseas hacer?\n-> ")

                        if int(x) == 1: #Ingresar
                            os.system('cls' if os.name=='nt' else 'clear')
                            print(f"-> {opt_tabla[0]}")
                            columnas = tabla(tabla_seleccionada, x)
                            datos = []
                            if columnas:
                                for columna in columnas:
                                    if not columna == 'id':
                                        x = input(f"Columna: {columna}\n-> ").capitalize()
                                        datos.append(x)
                                    else:
                                        continue
                                ingresar(tabla_seleccionada, datos, [col for col in columnas if not col == 'id'])
                                continue

                        if int(x) == 2: #Buscar
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"-> {opt_tabla[1]}")
                            columnas = tabla(tabla_seleccionada, x)
                            z = input(f"{' - '.join([col for col in columnas if col != 'id'])}\n-> ")
                            if not z or z not in columnas:
                                print("Entrada no válida. Operación cancelada.")
                                z = input("Enter para continuar...")
                                continue
                            x = input(f"Introduzca el {z}\n-> ").capitalize()
                            if not x:
                                print("Entrada no válida. Operación cancelada.")
                                x = input("Enter para continuar...")
                                continue
                            result = consult_all(tabla_seleccionada, z, x)
                            print("="*50)
                            for fila in result:
                                print(" - ".join(str(valor) for i, valor in enumerate(fila) if columnas[i] != 'id'))
                            x = input("Enter para continuar...")
                            continue
                            
                        if int(x) == 3: #Eliminar
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"-> {opt_tabla[2]}")
                            columnas = tabla(tabla_seleccionada, x)
                            z = input(f"{' - '.join([col for col in columnas if col != 'id'])}\n-> ")
                            if not z or z not in columnas:
                                print("Entrada no válida. Operación cancelada.")
                                z = input("Enter para continuar...")
                                continue
                            x = input(f"Introduzca el {z}\n-> ").capitalize()
                            if not x:
                                print("Entrada no válida. Operación cancelada.")
                                x = input("Enter para continuar...")
                                continue
                            result = consult_all(tabla_seleccionada, z, x)
                            print("="*50)
                            for i, fila in enumerate(result, start=1):
                                print(f"[{i}] " + " - ".join(str(valor) for i, valor in enumerate(fila) if columnas[i] != 'id'))
                            x = int(input("Selecciona la fila a eliminar\n-> "))
                            if 1 <= x <= len(result):
                                fila_seleccionada = result[x - 1]
                                dlt_fila(tabla_seleccionada, 'id', fila_seleccionada[columnas.index('id')])
                            input("Fila eliminada correctamente.\npresiona Enter para continuar...")
                            continue

                        if int(x) == 4: #Borrar tabla
                            os.system('cls' if os.name=='nt' else 'clear')
                            print(f"-> {opt_tabla[3]}")
                            x = input(f"¿Estás seguro de que deseas eliminar la tabla '{tabla_seleccionada}'? [y/n]\n-> ").lower()
                            if x == 'y':
                                dlt_tb(tabla_seleccionada)
                                input("presiona Enter para continuar...")
                                break
                            else:
                                input("Operación cancelada.\npresiona Enter para continuar...")
                                continue
                            input("Tabla eliminada correctamente.\npresiona Enter para continuar...")
                            continue

                        if int(x) == 5: #volver
                            os.system('cls' if os.name == 'nt' else 'clear')
                            x = input("Deseas volver al menu principal? [y/n]\n-> ").lower()
                            if x == 'y':
                                break
                            else:
                                input("Operación cancelada.\npresiona Enter para continuar...")
                                continue
                else:
                    input("Entrada no válida. Operación cancelada.\npresiona Enter para continuar...")
                    continue
            except ValueError:
                input(f"Entrada no válida. Operación cancelada.\npresiona Enter para continuar...")
        else:
            input("No hay tablas disponibles.\npresiona Enter para continuar...")

    if x == "3":  # Cerrar sesión
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Cerrando sesión...")
        break