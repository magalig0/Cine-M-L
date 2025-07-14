from threading import Thread, Lock
from multiprocessing import Process
from time import sleep

# Clase que hereda de Thread (HILO)
# Simula la compra de entradas por parte de un cliente
class CompraThread(Thread):
    def __init__(self, manager, cliente, cantidad, pelicula_id, lock: Lock):
        super().__init__()
        self.manager = manager # Acceso a los servicios del cine (bll)
        self.cliente = cliente # Nombre del cliente que compra
        self.cantidad = cantidad # Cantidad de entradas a comprar
        self.pelicula_id = pelicula_id # ID de la película para la que se compran entradas
        self.lock = lock # Lock para exclusión mutua (evita condiciones de carrera)

    def run(self):
        try:
            print(f"[{self.cliente}] Intentando comprar {self.cantidad} entradas...")
            with self.lock: # Bloqueo para asegurar exclusión mutua
                # Se registra la compra de entradas dentro del bloqueo
                self.manager.entrada_service.registrar_entrada(
                    self.cliente, self.cantidad, self.pelicula_id
                )
                print(f"[{self.cliente}] Compra realizada con éxito.")
            sleep(1) # Simula un pequeño tiempo de procesamiento
        except Exception as e:
            print(f"[{self.cliente}] Error: {e}")

# PROCESO: exporta la cartelera actual a un archivo de texto
def exportar_cartelera(manager):
    try:
        cartelera = manager.pelicula_service.obtener_cartelera()
        with open("cartelera.txt", "w") as f:
            for p in cartelera:
                f.write(f"{p[1]} - {p[2]} - Sala {p[3]}\n") # Título - Horario - Sala
        print("[Proceso] Cartelera exportada a cartelera.txt")
    except Exception as e:
        print(f"[Proceso] Error al exportar cartelera: {e}")

# PROCESO: cuenta la cantidad total de entradas vendidas
def contar_entradas(manager):
    try:
        peliculas = manager.pelicula_service.obtener_cartelera()
        total = 0
        for p in peliculas:
            entradas = manager.entrada_service.entradas_vendidas(p[0])
            total += entradas
        print(f"[Proceso] Total de entradas vendidas: {total}")
    except Exception as e:
        print(f"[Proceso] Error al contar entradas: {e}")

# PROCESO: simula el envío de un resumen diario de ventas (no hace cálculos, solo mensaje)
def enviar_resumen():
    print("[Proceso] Enviando resumen diario de ventas...")
    sleep(2) # Simula el tiempo de envío
    print("[Proceso] Resumen enviado con éxito.")