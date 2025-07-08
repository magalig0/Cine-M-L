from bll import CineManager

DB_PATH = "cine_M&L.db"

def mostrar_menu():
    print("-------MENU CINE M&L-------")
    print("1. Inicializar base de datos")
    print("2. Agregar sala")
    print("3. Ver salas")
    print("4. Agregar películas")
    print("5. Ver cartelera")
    print("6. Registrar compra de entradas")
    print("7. Ver mis compras por cliente")
    print("0. Salir")

def main():
    manager = CineManager(DB_PATH)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            confirm = input("¿Seguro? Se borrarán los datos. (s/n): ").lower()
            if confirm == "s":
                manager.inicializar_sistema(borrar_existentes=True)
                print("Base de datos inicializada correctamente.")

        elif opcion == "2":
            try:
                nombre = input("Nombre de la sala: ")
                capacidad = int(input("Capacidad de la sala: "))
                manager.sala_service.agregar_sala(nombre, capacidad)
                print("Sala agregada con éxito.")
            except ValueError as e:
                print(f"Error: {e}")

        elif opcion == "3":
            salas = manager.sala_service.obtener_salas()
            if salas:
                print("\nSalas disponibles:")
                for s in salas:
                    print(f"ID: {s[0]}, Nombre: {s[1]}, Capacidad: {s[2]}")
            else:
                print("No hay salas registradas.")

        elif opcion == "4":
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
            peliculas = manager.pelicula_service.obtener_cartelera()
            if peliculas:
                print("\nCartelera:")
                for p in peliculas:
                    print(f"ID: {p[0]}, Título: {p[1]}, Horario: {p[2]}, Sala ID: {p[3]}")
            else:
                print("No hay películas cargadas.")

        elif opcion == "6":
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
            cliente = input("Ingrese el nombre del cliente: ")
            compras = manager.entrada_service.obtener_compras_cliente(cliente)
            if compras:
                print("\nCompras registradas para", cliente)
                for c in compras:
                    print(f"ID: {c[0]}, Cliente: {c[1]}, Cantidad: {c[2]}, Película ID: {c[3]}")
            else:
                print("No se encontraron compras para ese cliente.")

        elif opcion == "0":
            print("Cerrando...")
            break

        else:
            print("Opción inválida. Volve a intentarlo de nuevo.")

if __name__ == "__main__":
    main()
