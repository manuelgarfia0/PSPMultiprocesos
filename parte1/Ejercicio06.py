from multiprocessing import Process, Queue
import os


def leer_pares_numeros(fichero: str, cola: Queue):
    print(f"[Lector] Leyendo fichero: {fichero}")

    try:
        with open(fichero, 'r') as f:
            for linea in f:
                numeros = linea.strip().split()
                if len(numeros) == 2:
                    valor1, valor2 = int(numeros[0]), int(numeros[1])
                    cola.put((valor1, valor2))
                    print(f"[Lector] Enviado: ({valor1}, {valor2})")

        cola.put(None)  # Señal de fin
        print("[Lector] Lectura completada")

    except FileNotFoundError:
        print(f"[Lector] Error: Fichero no encontrado")
        cola.put(None)


def calcular_suma_rango(inicio: int, fin: int) -> int:
    return (fin * (fin + 1) // 2) - ((inicio - 1) * inicio // 2)


def sumar_rangos(cola: Queue):
    print("[Sumador] Esperando pares...")

    datos = cola.get()

    # Procesar pares hasta recibir None
    while datos is not None:
        valor1, valor2 = datos
        print(f"[Sumador] Procesando: {valor1} a {valor2}")

        # Ordenar y calcular
        inicio = min(valor1, valor2)
        fin = max(valor1, valor2)
        total = calcular_suma_rango(inicio, fin)

        print(f"[Sumador] Suma de {valor1} a {valor2} = {total}")

        datos = cola.get()  # Leer siguiente par

    print("[Sumador] Finalizado")


if __name__ == "__main__":

    cola = Queue()
    fichero = os.path.join("Ejercicios", "pares_numeros.txt")

    print("=" * 60)
    print("EJERCICIO 6: Pares de números con Queue")
    print("=" * 60)

    # Crear procesos
    lector = Process(target=leer_pares_numeros, args=(fichero, cola))
    sumador = Process(target=sumar_rangos, args=(cola,))

    # Ejecutar procesos concurrentemente
    lector.start()
    sumador.start()

    # Esperar finalización
    lector.join()
    sumador.join()

    print("=" * 60)
    print("Procesos finalizados")
    print("=" * 60)