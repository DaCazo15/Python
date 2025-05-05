import os
import json

class Catalogo:
    ruta = 'text.json'

    @classmethod
    def load_json(cls):
        try:
            if os.path.exists(cls.ruta):
                with open(cls.ruta, 'r') as archivo:
                    try:
                        return json.load(archivo)
                    except json.JSONDecodeError:
                        print("El archivo contiene un JSON inválido.")
                        return []
            else:
                return []
        except Exception as e:
            print(f"Error cargando el archivo JSON: {e}")
            return []

    @classmethod
    def agg_pelicula(cls, pelicula):
        try:
            contenido = cls.load_json()
            index = len(contenido)
            contenido.append({index + 1: pelicula.nombre})

            with open(cls.ruta, 'w') as archivo:
                json.dump(contenido, archivo, indent=4)
            print(f"Película '{pelicula.nombre}' agregada al catálogo.")
        except Exception as e:
            print(f"Error al agregar la película: {e}")

    @classmethod
    def list_pelicula(cls):
        try:
            print(f"{' Catálogo de Películas ':=^50}")
            contenido = cls.load_json()
            if contenido:
                for pelicula in contenido:
                    for key, value in pelicula.items():
                        print(f"{key}.- Película: {value.capitalize()}")
            else:
                print("El catálogo está vacío.")
        except Exception as e:
            print(f"Error listando las películas: {e}")

    @classmethod
    def bsc_pelicula(cls, name_pelicula):
        try:
            contenido = cls.load_json()
            contenido_filtrado = [pelicula for pelicula in contenido if name_pelicula.nombre in pelicula.values()]
            if contenido_filtrado:
                print(f"Pelicula Encontrada:")
                for pelicula in contenido_filtrado:
                    for key, value in pelicula.items():
                        print(f"{key}.- Película: {value.capitalize()}")
            else:
                print(f"La película '{name_pelicula}' no se encontró en el catálogo.")
        except Exception as e:
            print(f"Error buscando la película: {e}")

    @classmethod
    def dlt_pelicula(cls, name_pelicula):
        try:
            contenido = cls.load_json()
            contenido_filtrado = [pelicula for pelicula in contenido if name_pelicula.nombre not in pelicula.values()]

            if len(contenido) == len(contenido_filtrado):
                print(f"La película '{name_pelicula}' no se encontró en el catálogo.")
                return

            with open(cls.ruta, 'w') as archivo:
                json.dump(contenido_filtrado, archivo, indent=4)
            print(f"Película '{name_pelicula}' fue eliminada del catálogo.")
        except Exception as e:
            print(f"Error al eliminar la película: {e}")

    @classmethod
    def dlt_file(cls):
        try:
            if os.path.exists(cls.ruta):
                os.remove(cls.ruta)
                print(f"El catalogo ha sido eliminado.")
            else:
                print(f"No existe el archivo '{cls.ruta}'.")
        except Exception as e:
            print(f"Error al eliminar el archivo: {e}")
            