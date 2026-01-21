from multiprocessing import Process


def calcular_suma_rango(inicio: int, fin: int) -> int:
    return (fin * (fin + 1) // 2) - ((inicio - 1) * inicio // 2)


def sumar_rango(valor1: int, valor2: int):
    # Ordenar valores
    inicio = min(valor1, valor2)
    fin = max(valor1, valor2)

    # Calcular suma
    total = calcular_suma_rango(inicio, fin)

    # Mostrar resultado
    print(f"Suma de {valor1} a {valor2} = {total}")
    return total


if __name__ == "__main__":

    print("=" * 60)
    print("EJERCICIO 5: Suma de rangos con Process")
    print("=" * 60)

    # Rangos a procesar (incluye casos donde valor1 > valor2)
    rangos = [
        (1, 10),
        (5, 15),
        (20, 10),     # Invertido
        (100, 50),    # Invertido
        (1, 100),
        (500, 1000),
    ]

    # Crear lista de procesos
    procesos = [Process(target=sumar_rango, args=rango) for rango in rangos]

    # Iniciar todos los procesos
    for p in procesos:
        p.start()

    # Esperar a que todos terminen
    for p in procesos:
        p.join()

    print("=" * 60)
    print("Todos los procesos finalizados")
    print("=" * 60)