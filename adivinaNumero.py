import random

init, numero = 0, 0

while True:
    while init == 0:
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        if (a+10) < b:
            numero = random.randint(a, b)
            init += 1 
            break
    
    while True:
        mensaje = f"Adivina el numero [{a}/{b}]: "
        print(f"=" * len(mensaje))
        try:
            respuesta = int(input(mensaje))
            break
        except ValueError:
            print(f"--Entrada invalida--")
            continue

    if isinstance(respuesta, int):
        if respuesta == numero: 
            print(f"Respuesta correcta\nEl numero es {numero}")
            q = input("Continuar [s][n]: ")
            if q == 'n':
                break
        elif respuesta > b or respuesta < a: 
            print(f"-- El {respuesta} no esta en el rango --")
        elif (numero - respuesta) > 1 and (numero - respuesta) < 5:
            print(f"{respuesta} Esta cerca")
        elif (numero - respuesta) > 5:
            print(f"{respuesta} Esta lejos")
