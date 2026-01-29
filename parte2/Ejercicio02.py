from multiprocessing import Process, Pipe
import random
import time


def generar_ip_aleatoria():
    """Genera una dirección IP aleatoria"""
    return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"


def clasificar_ip(ip):
    """
    Determina la clase de una dirección IP
    
    Clase A: 0.0.0.0 - 127.255.255.255 (primer octeto: 0-127)
    Clase B: 128.0.0.0 - 191.255.255.255 (primer octeto: 128-191)
    Clase C: 192.0.0.0 - 223.255.255.255 (primer octeto: 192-223)
    Clase D: 224.0.0.0 - 239.255.255.255 (Multicast)
    Clase E: 240.0.0.0 - 255.255.255.255 (Reservada)
    """
    primer_octeto = int(ip.split('.')[0])
    
    if 0 <= primer_octeto <= 127:
        return 'A'
    elif 128 <= primer_octeto <= 191:
        return 'B'
    elif 192 <= primer_octeto <= 223:
        return 'C'
    elif 224 <= primer_octeto <= 239:
        return 'D'
    else:
        return 'E'


def proceso1_generar_ips(conn):
    """
    Proceso 1: Genera 10 direcciones IP aleatorias y las envía al Proceso 2
    """
    print("[Proceso 1] Generando 10 direcciones IP aleatorias...")
    
    for i in range(10):
        ip = generar_ip_aleatoria()
        print(f"[Proceso 1] IP generada #{i+1}: {ip}")
        conn.send(ip)
    
    # Enviar señal de finalización
    conn.send(None)
    conn.close()
    print("[Proceso 1] Finalizado")


def proceso2_filtrar_ips(conn_entrada, conn_salida):
    """
    Proceso 2: Lee las IPs del Proceso 1 y envía al Proceso 3
    solo las de clase A, B o C
    """
    print("[Proceso 2] Esperando direcciones IP para filtrar...")
    
    ips_filtradas = 0
    ips_descartadas = 0
    
    while True:
        ip = conn_entrada.recv()
        
        if ip is None:  # Señal de finalización
            break
        
        clase = clasificar_ip(ip)
        
        if clase in ['A', 'B', 'C']:
            print(f"[Proceso 2] ✓ IP {ip} (Clase {clase}) - ACEPTADA")
            conn_salida.send((ip, clase))
            ips_filtradas += 1
        else:
            print(f"[Proceso 2] ✗ IP {ip} (Clase {clase}) - RECHAZADA")
            ips_descartadas += 1
    
    # Enviar señal de finalización
    conn_salida.send((None, None))
    conn_entrada.close()
    conn_salida.close()
    
    print(f"[Proceso 2] Finalizado - Filtradas: {ips_filtradas}, Rechazadas: {ips_descartadas}")


def proceso3_mostrar_ips(conn):
    """
    Proceso 3: Lee las IPs del Proceso 2 e imprime la IP con su clase
    """
    print("[Proceso 3] Esperando direcciones IP filtradas...\n")
    print("=" * 60)
    print("DIRECCIONES IP VÁLIDAS (Clases A, B, C)")
    print("=" * 60)
    
    contador = 0
    
    while True:
        ip, clase = conn.recv()
        
        if ip is None:  # Señal de finalización
            break
        
        contador += 1
        print(f"{contador}. IP: {ip:<15} → Clase: {clase}")
    
    conn.close()
    print("=" * 60)
    print(f"[Proceso 3] Total de IPs válidas recibidas: {contador}")
    print(f"[Proceso 3] Finalizado")


if __name__ == '__main__':
    print("=" * 60)
    print("EJERCICIO 2: Filtrado de direcciones IP con procesos enlazados")
    print("=" * 60)
    print()
    
    # Medir tiempo de ejecución
    tiempo_inicio = time.time()
    
    # Crear dos pipes para la comunicación entre procesos
    # pipe1: Proceso 1 → Proceso 2
    # pipe2: Proceso 2 → Proceso 3
    conn1_send, conn1_recv = Pipe()
    conn2_send, conn2_recv = Pipe()
    
    # Crear los tres procesos
    p1 = Process(target=proceso1_generar_ips, args=(conn1_send,))
    p2 = Process(target=proceso2_filtrar_ips, args=(conn1_recv, conn2_send))
    p3 = Process(target=proceso3_mostrar_ips, args=(conn2_recv,))
    
    # Lanzar los procesos en orden
    p1.start()
    p2.start()
    p3.start()
    
    # Esperar a que todos terminen
    p1.join()
    p2.join()
    p3.join()
    
    tiempo_fin = time.time()
    tiempo_total = tiempo_fin - tiempo_inicio
    
    print()
    print("=" * 60)
    print(f"Tiempo total de ejecución: {tiempo_total:.4f} segundos")
    print("=" * 60)