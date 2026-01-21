from multiprocessing import Pool
import time
import os


def leer_pares_fichero(fichero: str) -> list:
    pares = []

    try:
        with open(fichero, 'r') as f:
            for linea in f:
                numeros = linea.strip().split()
                if len(numeros) == 2:
                    valor1, valor2 = int(numeros[0]), int(numeros[1])
                    pares.append((valor1, valor2))
                    print(f"[Lector] Par leído: ({valor1}, {valor2})")

        print(f"[Lector] {len(pares)} pares cargados")
        return pares

    except FileNotFoundError:
        print(f"[Error] Fichero no encontrado: {fichero}")
        return []


def calcular_suma_rango(inicio: int, fin: int) -> int:
    return (fin * (fin + 1) // 2) - ((inicio - 1) * inicio // 2)


def sumar_rango(valor1: int, valor2: int):
    # Ordenar valores
    inicio = min(valor1, valor2)
    fin = max(valor1, valor2)

    # Calcular suma
    total = calcular_suma_rango(inicio, fin)

    print(f"[Worker] Suma de {valor1} a {valor2} = {total}")
    return total


if __name__ == "__main__":

    fichero = os.path.join("Ejercicios", "pares_numeros.txt")

    print("=" * 60)
    print("EJERCICIO 8: Pool + starmap con datos de fichero")
    print("=" * 60)

    # Leer pares del fichero
    pares = leer_pares_fichero(fichero)

    if not pares:
        print("No hay datos para procesar")
        exit(1)

    print("\n" + "-" * 60)
    print("Comparación de rendimiento con diferentes Pools")
    print("-" * 60)

    # Probar con diferentes tamaños de Pool
    for num_procesos in [1, 2, 3, 4]:
        print(f"\n--- Pool con {num_procesos} proceso(s) ---")

        start_time = time.perf_counter()

        # Usar starmap para pasar múltiples argumentos
        with Pool(processes=num_procesos) as pool:
            resultados = pool.starmap(sumar_rango, pares)

        end_time = time.perf_counter()
        tiempo_total = end_time - start_time

        print(f"Tiempo: {tiempo_total:.6f} segundos")
        print(f"Resultados: {resultados}")

    print("\n" + "=" * 60)
    print("Comparación completada")
    print("=" * 60)