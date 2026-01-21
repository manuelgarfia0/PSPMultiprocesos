from multiprocessing import Process, Pipe
import os


def leer_pares_numeros(fichero: str, conexion):
    print(f"[Lector] Leyendo fichero: {fichero}")

    try:
        with open(fichero, 'r') as f:
            for linea in f:
                numeros = linea.strip().split()
                if len(numeros) == 2:
                    valor1, valor2 = int(numeros[0]), int(numeros[1])
                    conexion.send((valor1, valor2))
                    print(f"[Lector] Enviado: ({valor1}, {valor2})")

        conexion.send(None)  # Señal de fin
        print("[Lector] Lectura completada")

    except FileNotFoundError:
        print(f"[Lector] Error: Fichero no encontrado")
        conexion.send(None)
    finally:
        conexion.close()


def calcular_suma_rango(inicio: int, fin: int) -> int:
    return (fin * (fin + 1) // 2) - ((inicio - 1) * inicio // 2)


def sumar_rangos(conexion):
    print("[Sumador] Esperando pares...")

    datos = conexion.recv()

    # Procesar pares hasta recibir None
    while datos is not None:
        valor1, valor2 = datos
        print(f"[Sumador] Procesando: {valor1} a {valor2}")

        # Ordenar y calcular
        inicio = min(valor1, valor2)
        fin = max(valor1, valor2)
        total = calcular_suma_rango(inicio, fin)

        print(f"[Sumador] Suma de {valor1} a {valor2} = {total}")

        datos = conexion.recv()  # Leer siguiente par

    print("[Sumador] Finalizado")
    conexion.close()


if __name__ == "__main__":
    # Crear Pipe: retorna dos conexiones
    conn_envio, conn_recepcion = Pipe()

    fichero = os.path.join("Ejercicios", "pares_numeros.txt")

    print("=" * 60)
    print("EJERCICIO 7: Pares de números con Pipe")
    print("=" * 60)

    # Crear procesos
    lector = Process(target=leer_pares_numeros, args=(fichero, conn_envio))
    sumador = Process(target=sumar_rangos, args=(conn_recepcion,))

    # Ejecutar procesos concurrentemente
    lector.start()
    sumador.start()

    # Cerrar conexiones en proceso principal
    conn_envio.close()
    conn_recepcion.close()

    # Esperar finalización
    lector.join()
    sumador.join()

    print("=" * 60)
    print("Procesos finalizados")
    print("=" * 60)