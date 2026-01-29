from multiprocessing import Process, Queue
import time
import os


def proceso1_filtrar_peliculas(ruta_fichero, anio, queue):
    try:
        print(f"[Proceso 1] Leyendo fichero: {ruta_fichero}")
        print(f"[Proceso 1] Filtrando películas del año {anio}...")
        
        peliculas_enviadas = 0
        
        with open(ruta_fichero, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                
                # Separar nombre y año por punto y coma
                partes = linea.split(';')
                if len(partes) == 2:
                    nombre_pelicula = partes[0].strip()
                    anio_estreno = partes[1].strip()
                    
                    # Filtrar por año
                    if anio_estreno == str(anio):
                        queue.put((nombre_pelicula, anio_estreno))
                        peliculas_enviadas += 1
                        print(f"[Proceso 1] ✓ Enviada: {nombre_pelicula} ({anio_estreno})")
        
        # Enviar señal de finalización
        queue.put((None, None))
        
        print(f"\n[Proceso 1] Finalizado - Películas enviadas: {peliculas_enviadas}")
        
    except FileNotFoundError:
        print(f"[Proceso 1] ❌ Error: No se encontró el fichero {ruta_fichero}")
        queue.put((None, None))
    except Exception as e:
        print(f"[Proceso 1] ❌ Error: {e}")
        queue.put((None, None))


def proceso2_guardar_peliculas(queue, anio):
    nombre_fichero = f"peliculas{anio}.txt"
    
    print(f"\n[Proceso 2] Esperando películas para guardar en {nombre_fichero}...")
    
    peliculas_recibidas = 0
    
    with open(nombre_fichero, 'w', encoding='utf-8') as f:
        while True:
            pelicula, anio_estreno = queue.get()
            
            # Verificar señal de finalización
            if pelicula is None:
                break
            
            # Escribir en el fichero
            f.write(f"{pelicula};{anio_estreno}\n")
            peliculas_recibidas += 1
            print(f"[Proceso 2] 💾 Guardada: {pelicula}")
    
    print(f"\n[Proceso 2] Finalizado - Películas guardadas: {peliculas_recibidas}")
    print(f"[Proceso 2] Fichero creado: {nombre_fichero}")


def main():
    print("=" * 70)
    print("EJERCICIO 4: Filtrado de películas por año")
    print("=" * 70)
    
    # Cambiar al directorio del ejercicio
    os.chdir('/home/claude/ejercicio4')
    
    # Solicitar año al usuario
    anio_actual = 2026
    anio = None
    
    while anio is None:
        try:
            entrada = input(f"\nIntroduce un año (menor a {anio_actual}): ").strip()
            anio = int(entrada)
            
            if anio >= anio_actual:
                print(f"El año debe ser menor a {anio_actual}")
                anio = None
            elif anio < 1800:
                print("Por favor, introduce un año válido")
                anio = None
                
        except ValueError:
            print("Por favor, introduce un número válido")
    
    # Solicitar ruta al fichero
    ruta_fichero = input("\nIntroduce la ruta al fichero de películas (o Enter para usar 'peliculas.txt'): ").strip()
    
    if not ruta_fichero:
        ruta_fichero = 'peliculas.txt'
    
    # Verificar que el fichero existe
    if not os.path.exists(ruta_fichero):
        print(f"\nError: El fichero '{ruta_fichero}' no existe")
        print("Creando fichero de ejemplo 'peliculas.txt'...")
        ruta_fichero = 'peliculas.txt'
        
        if not os.path.exists(ruta_fichero):
            print("No se pudo encontrar el fichero de películas")
            return
    
    print("\n" + "=" * 70)
    print(f"Configuración:")
    print(f"  - Año de filtrado: {anio}")
    print(f"  - Fichero de origen: {ruta_fichero}")
    print(f"  - Fichero de destino: peliculas{anio}.txt")
    print("=" * 70)
    
    # Medir tiempo de ejecución
    tiempo_inicio = time.time()
    
    # Crear una Queue para la comunicación entre procesos
    # Queue es mejor que Pipe cuando no sabemos cuántos elementos se enviarán
    queue = Queue()
    
    # Crear los procesos
    p1 = Process(target=proceso1_filtrar_peliculas, args=(ruta_fichero, anio, queue))
    p2 = Process(target=proceso2_guardar_peliculas, args=(queue, anio))
    
    # Lanzar los procesos
    print("\n[MAIN] Iniciando procesos...\n")
    p1.start()
    p2.start()
    
    # Esperar a que terminen
    p1.join()
    p2.join()
    
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    
    # Mostrar resultados
    print("\n" + "=" * 70)
    print("PROCESO COMPLETADO")
    print("=" * 70)
    
    # Verificar si se creó el fichero y mostrar su contenido
    fichero_salida = f"peliculas{anio}.txt"
    if os.path.exists(fichero_salida):
        print(f"\n📁 Contenido de {fichero_salida}:")
        print("-" * 70)
        
        with open(fichero_salida, 'r', encoding='utf-8') as f:
            contenido = f.read()
            if contenido:
                print(contenido)
            else:
                print(f"(No se encontraron películas del año {anio})")
        
        print("-" * 70)
    
    print(f"\nTiempo total de ejecución: {tiempo_total:.4f} segundos")
    print("=" * 70)


if __name__ == '__main__':
    main()