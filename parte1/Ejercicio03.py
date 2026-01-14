from multiprocessing import Process, Queue

def sumarNumeros(cola):
    while True:
        numero = cola.get()

        i = 1
        resultado = 0
        for i in range (numero + 1):
            resultado = resultado + i
        print(resultado)

def leerFichero(cola):
    with open("coño/Ejercicio03.txt", "r") as archivo:
        for linea in archivo:
            numero = int(linea.strip())  # Convertir a entero
            print(f"Leyendo número: {numero}")
            cola.put(numero)  # Añadir a la cola
    
    cola.put(None)  # Señal de que terminó de leer
    print("Fichero leído completamente")

if __name__ == "__main__":
    # Crear la cola compartida
    cola = Queue()
    
    # Crear los procesos
    p_lector = Process(target=leerFichero, args=(cola,))
    p_sumador = Process(target=sumarNumeros, args=(cola,))
    
    # Iniciar los procesos
    # Primero el sumador (consumidor) y luego el lector (productor)
    p_sumador.start()
    p_lector.start()
    
    # Esperar a que terminen
    p_lector.join()
    p_sumador.join()
    
    print("\nTodos los procesos han terminado")

