# Importación de capas
from bll import CineManager  # Clase central que conecta los servicios
from concurrencia import CompraThread, exportar_cartelera, contar_entradas, enviar_resumen  # Hilos y procesos
from threading import Lock  # Para exclusión mutua entre hilos
from multiprocessing import Process  # Para procesos

# Ruta a la base de datos
DB_PATH = "cine_M&L.db"

# Muestra el menú principal
def mostrar_menu():
    print("-------MENU CINE M&L-------")
    print("1. Inicializar base de datos")
    print("2. Agregar sala")
    print("3. Ver salas")
    print("4. Agregar películas")
    print("5. Ver cartelera")
    print("6. Registrar compra de entradas")
    print("7. Ver mis compras por cliente")
    print("8. Simular compras concurrentes")  # HILOS
    print("9. Ejecutar procesos")              # PROCESOS
    print("0. Salir")

# Función principal del sistema
def main():
    manager = CineManager(DB_PATH)  # Crea el gestor principal del cine

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Inicializa la base de datos
            confirm = input("¿Seguro? Se borrarán los datos. (s/n): ").lower()
            if confirm == "s":
                manager.inicializar_sistema(borrar_existentes=True)
                print("Base de datos inicializada correctamente.")

        elif opcion == "2":
            # Agrega una nueva sala
            try:
                nombre = input("Nombre de la sala: ")
                capacidad = int(input("Capacidad de la sala: "))
                manager.sala_service.agregar_sala(nombre, capacidad)
                print("Sala agregada con éxito.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "3":
            # Muestra las salas existentes
            salas = manager.sala_service.obtener_salas()
            if salas:
                print("\nSalas disponibles:")
                for s in salas:
                    print(f"ID: {s[0]}, Nombre: {s[1]}, Capacidad: {s[2]}")
            else:
                print("No hay salas registradas.")

        elif opcion == "4":
            # Agrega una película
            try:
                titulo = input("Título de la película: ")
                horario = input("Horario (HH:MM): ")
                salas = manager.sala_service.obtener_salas()
                if not salas:
                    print("Primero debe agregar salas.")
                    continue

                print("\nSalas disponibles:")
                for s in salas:
                    print(f"ID: {s[0]} - {s[1]} (Capacidad: {s[2]})")

                sala_id = int(input("ID de la sala asignada: "))
                manager.pelicula_service.agregar_pelicula(titulo, horario, sala_id)
                print("Película agregada con éxito.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "5":
            # Muestra la cartelera
            peliculas = manager.pelicula_service.obtener_cartelera()
            if peliculas:
                print("\nCartelera:")
                for p in peliculas:
                    print(f"ID: {p[0]}, Título: {p[1]}, Horario: {p[2]}, Sala ID: {p[3]}")
            else:
                print("No hay películas cargadas.")

        elif opcion == "6":
            # Registra una compra de entradas
            try:
                cliente = input("Nombre del cliente: ")
                cantidad = int(input("Cantidad de entradas: "))
                peliculas = manager.pelicula_service.obtener_cartelera()
                if not peliculas:
                    print("No hay películas cargadas.")
                    continue

                print("\nPelículas disponibles:")
                for p in peliculas:
                    print(f"ID: {p[0]} - {p[1]} (Horario: {p[2]}, Sala ID: {p[3]})")

                pelicula_id = int(input("ID de la película: "))
                manager.entrada_service.registrar_entrada(cliente, cantidad, pelicula_id)
                print("Compra registrada con éxito.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "7":
            # Muestra compras de un cliente
            cliente = input("Ingrese el nombre del cliente: ")
            compras = manager.entrada_service.obtener_compras_cliente(cliente)
            if compras:
                print("\nCompras registradas para", cliente)
                for c in compras:
                    print(f"ID: {c[0]}, Cliente: {c[1]}, Cantidad: {c[2]}, Película ID: {c[3]}")
            else:
                print("No se encontraron compras para ese cliente.")

        elif opcion == "8":
            # Simula compras simultáneas con hilos
            print("Simulando compras concurrentes...")
            lock = Lock()  # Lock para exclusión mutua
            pelicula_id = 1  # Se debe asegurar que exista esta película

            # Lista de hilos simulando clientes comprando
            hilos = [
                CompraThread(manager, "Lucía", 2, pelicula_id, lock),
                CompraThread(manager, "Magalí", 1, pelicula_id, lock),
                CompraThread(manager, "Pedro", 3, pelicula_id, lock),
                CompraThread(manager, "Juli", 1, pelicula_id, lock),
                CompraThread(manager, "Nico", 2, pelicula_id, lock),
            ]

            for h in hilos:
                h.start()
            for h in hilos:
                h.join()

            print("Todas las compras fueron procesadas.")

        elif opcion == "9":
            # Ejecuta 3 procesos: exportar cartelera, contar entradas y enviar resumen
            print("Ejecutando procesos...")
            p1 = Process(target=exportar_cartelera, args=(manager,))
            p2 = Process(target=contar_entradas, args=(manager,))
            p3 = Process(target=enviar_resumen)

            p1.start()
            p2.start()
            p3.start()

            p1.join()
            p2.join()
            p3.join()

        elif opcion == "0":
            print("Cerrando...")
            break

        else:
            print("Opción inválida. Volvé a intentarlo.")

# Punto de entrada del programa
if __name__ == "__main__":
    main()
