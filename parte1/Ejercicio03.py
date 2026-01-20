from multiprocessing import Process, Queue
import time

def sumarNumeros(cola):
    terminado = False

    while not terminado:
        numero = cola.get()

        if numero is None:
            terminado = True
        else:
            resultado = 0
            for i in range(numero + 1):
                resultado += i

            print(f"Suma de 0 a {numero}: {resultado}")

def leerFichero(cola):
    with open("Ejercicio03.txt", "r") as archivo:
        for linea in archivo:
            numero = int(linea.strip())
            print(f"Leyendo número: {numero}")
            cola.put(numero)

    cola.put(None)

if __name__ == "__main__":
    inicio = time.perf_counter()
    
    cola = Queue()

    proceso_lector = Process(target=leerFichero, args=(cola,))
    proceso_sumador = Process(target=sumarNumeros, args=(cola,))

    proceso_sumador.start()
    proceso_lector.start()

    proceso_lector.join()
    proceso_sumador.join()

    print("\nTodos los procesos han terminado")

    fin = time.perf_counter()
    tiempo = fin - inicio
    print(f"Tiempo: {tiempo}")
