from multiprocessing import Process

def sumarNumeros(numero : int) -> None:
    i = 1
    resultado = 0
    for i in range (numero + 1):
        resultado = resultado + i
    print(resultado)

def main():
    pass

if __name__ == "__main__":
    p1 = Process(target=sumarNumeros, args=(10,))
    p2 = Process(target=sumarNumeros, args=(15,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("El programa ha terminado")