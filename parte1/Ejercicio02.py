from multiprocessing import Pool
import time

def sumarNumeros(numero : int) -> int:
    i = 1
    resultado = 0
    for i in range (numero + 1):
        resultado = resultado + i
    return resultado

def main():
    pass

if __name__ == "__main__":
    inicio = time.perf_counter()

    with Pool(processes=3) as pool:
        numeros = [10, 15, 20]
        results = pool.map(sumarNumeros, numeros)

    fin = time.perf_counter()
    tiempo = fin - inicio

    print(f"Proceso terminado {results}")
    print(f"Tiempo: {tiempo}")