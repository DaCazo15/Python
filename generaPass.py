import string, random

lst = []
password = ""

def listado_string():
    for x in string.ascii_letters:
        lst.append(x)
    for x in string.digits:
        lst.append(x)
    for x in string.punctuation:
        lst.append(x)
    return lst
    
long = int(input("Introduce la longitud de tu Password: "))

for i in range(long): password += random.choice(listado_string())
print(f"Tu Password es: {password}")