from multiprocessing import Process
import time


def contar_vocal(vocal, ruta_fichero):
    """
    Función que cuenta cuántas veces aparece una vocal en un fichero
    
    Args:
        vocal: La vocal a contar (a, e, i, o, u)
        ruta_fichero: Ruta al fichero de texto
    """
    try:
        with open(ruta_fichero, 'r', encoding='utf-8') as f:
            contenido = f.read().lower()
            
        contador = contenido.count(vocal.lower())
        print(f"La vocal '{vocal}' aparece {contador} veces en el fichero")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el fichero {ruta_fichero}")
    except Exception as e:
        print(f"Error al procesar la vocal '{vocal}': {e}")


if __name__ == '__main__':
    # Ruta al fichero de texto
    ruta_fichero = 'Texto.txt'
    
    # Lista de vocales
    vocales = ['a', 'e', 'i', 'o', 'u']
    
    # Lista para almacenar los procesos
    procesos = []
    
    print("=" * 60)
    print("EJERCICIO 1: Conteo de vocales en paralelo")
    print("=" * 60)
    print(f"Fichero: {ruta_fichero}\n")
    
    # Medir el tiempo de ejecución
    tiempo_inicio = time.time()
    
    # Crear y lanzar un proceso para cada vocal
    for vocal in vocales:
        p = Process(target=contar_vocal, args=(vocal, ruta_fichero))
        procesos.append(p)
        p.start()
    
    # Esperar a que todos los procesos terminen
    for p in procesos:
        p.join()
    
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    
    print(f"\n{'=' * 60}")
    print(f"Tiempo total de ejecución: {tiempo_total:.4f} segundos")
    print(f"{'=' * 60}")