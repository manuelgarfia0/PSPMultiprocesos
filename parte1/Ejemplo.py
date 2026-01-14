from multiprocessing import Process
import os

def saludar(nombre : str) -> None:
    print(f"[HIJO] Hola {nombre}. PID = {os.getpid()}")

if __name__ == "__main__":
    
    print(f"[PADRE] PID={os.getpid()}")

    p = Process(target=saludar, args=("Manuel",))
    p.start()
    p.join()
    print("[PADRE] El proceso ha terminado")