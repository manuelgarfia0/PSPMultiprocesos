from multiprocessing import Process, Pipe
import os


def leer_numeros(fichero: str, conexion):
    print(f"[Lector] Leyendo fichero: {fichero}")

    try:
        with open(fichero, 'r') as f:
            for linea in f:
                numero = int(linea.strip())
                conexion.send(numero)
                print(f"[Lector] Enviado: {numero}")

        conexion.send(None)  # Señal de fin
        print("[Lector] Lectura completada")

    except FileNotFoundError:
        print(f"[Lector] Error: Fichero no encontrado")
        conexion.send(None)
    finally:
        conexion.close()


def calcular_suma(numero: int) -> int:
    return numero * (numero + 1) // 2


def sumar_numeros(conexion):
    print("[Sumador] Esperando números...")

    numero = conexion.recv()

    # Procesar números hasta recibir None
    while numero is not None:
        print(f"[Sumador] Procesando: {numero}")

        total = calcular_suma(numero)
        print(f"[Sumador] Suma hasta {numero} = {total}")

        numero = conexion.recv()  # Leer siguiente número

    print("[Sumador] Finalizado")
    conexion.close()


if __name__ == "__main__":
    # Crear Pipe: retorna dos conexiones (extremos de la tubería)
    conn_envio, conn_recepcion = Pipe()

    fichero = os.path.join("parte1", "Ejercicio04.txt")

    print("=" * 60)
    print("EJERCICIO 4: Comunicación con Pipe")
    print("=" * 60)

    # Crear procesos
    lector = Process(target=leer_numeros, args=(fichero, conn_envio))
    sumador = Process(target=sumar_numeros, args=(conn_recepcion,))

    # Ejecutar procesos concurrentemente
    lector.start()
    sumador.start()

    # Cerrar conexiones en proceso principal (buena práctica)
    conn_envio.close()
    conn_recepcion.close()

    # Esperar finalización
    lector.join()
    sumador.join()

    print("=" * 60)
    print("Procesos finalizados")
    print("=" * 60)