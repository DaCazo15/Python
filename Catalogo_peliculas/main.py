from catalogo import Catalogo
from pelicula import Peliculas
import os

opt = ["Agregar una pelicula", "Buscar una pelicula", "Ver catalogo", "Eliminar una pelicula", "Borrar el catalogo", "salir"]

def cls_console(): return os.system('cls' if os.name == 'nt' else 'clear')

def taquilla(opt):
    cls_console()
    while True:
        try:
            print(f"{'Menu':=^50}")
            for x, option in enumerate(opt, start=1):
                print(f"[{x}] {option}")
            respt = int(input("Que deseas haces?\n\n- "))
            if respt == 1:
                agg_peli = input("Que pelicula deseas agregar al catalogo?\n\n- ").lower()
                pelicula = Peliculas(agg_peli)
                Catalogo.agg_pelicula(pelicula)
            elif respt == 2:
                bsc_peli = input("Que pelicula deseas buscar en el catalogo?\n\n- ").lower()
                pelicula = Peliculas(bsc_peli)
                Catalogo.bsc_pelicula(pelicula)
            elif respt == 3:
                Catalogo.list_pelicula()
            elif respt == 4:
                dlt_peli = input("Que pelicula deseas eliminar del catalogo?\n\n- ").lower()
                pelicula = Peliculas(dlt_peli)
                Catalogo.dlt_pelicula(pelicula)
            elif respt == 5:
                dlt_file = input("Deseas eliminar el catalogo? [y][n]\n\n- ")
                if dlt_file.lower() == 'y':
                    Catalogo.dlt_file()
            elif respt == 6:
                salir = input("Deseas salir [y][n]\n\n- ")
                if salir.lower() == 'y':
                    exit()
            else:
                print("Opcion invalidad, intenta ota vez")
        except ValueError:
            print("Por favor, ingresa un número válido.")
if __name__ == "__main__":
    taquilla(opt)