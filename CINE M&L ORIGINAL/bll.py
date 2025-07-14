import dal  # Importa las funciones de acceso a base de datos (capa DAL)

# Servicio que gestiona las salas
class SalaService:
    def __init__(self, db_path):
        self.db_path = db_path  # Ruta a la base de datos

    def agregar_sala(self, nombre, capacidad):
        # Valida que el nombre no esté vacío y que la capacidad sea positiva
        if not nombre or capacidad <= 0:
            raise ValueError("Datos inválidos para la sala.")
        dal.inserta_sala(self.db_path, nombre, capacidad)  # Llama a DAL para guardar

    def obtener_salas(self):
        return dal.traer_salas(self.db_path)  # Devuelve todas las salas existentes

# Servicio que gestiona las películas
class PeliculaService:
    def __init__(self, db_path):
        self.db_path = db_path

    def agregar_pelicula(self, titulo, horario, sala_id):
        # Valida que todos los datos estén presentes
        if not titulo or not horario or sala_id is None:
            raise ValueError("Todos los campos de la película son obligatorios.")

        # Verifica que no haya superposición de películas en la misma sala y horario
        peliculas_existentes = self.obtener_cartelera()
        for p in peliculas_existentes:
            id_pelicula, titulo_existente, horario_existente, sala_id_existente = p
            if horario.strip() == horario_existente.strip() and sala_id == sala_id_existente:
                raise ValueError(f"No se puede agregar dos películas en la misma sala ({sala_id}) y horario ({horario}).")

        dal.inserta_pelicula(self.db_path, titulo, horario, sala_id)  # Guarda en DB

    def obtener_cartelera(self):
        return dal.traer_peliculas(self.db_path)  # Lista todas las películas

    def obtener_capacidad_sala(self, pelicula_id):
        # Busca la capacidad de la sala asociada a una película
        peliculas = self.obtener_cartelera()
        for p in peliculas:
            if p[0] == pelicula_id:
                sala_id = p[3]
                salas = dal.traer_salas(self.db_path)
                for s in salas:
                    if s[0] == sala_id:
                        return s[2]  # Devuelve capacidad
        return 0  # Si no encuentra la sala, devuelve 0

# Servicio que gestiona las entradas (ventas)
class EntradaService:
    def __init__(self, db_path, pelicula_service):
        self.db_path = db_path
        self.pelicula_service = pelicula_service  # Necesita saber la capacidad de la sala

    def entradas_vendidas(self, pelicula_id):
        # Suma cuántas entradas ya se vendieron para una película
        def accion(cursor):
            cursor.execute(
                "SELECT SUM(cantidad) FROM entradas WHERE pelicula_id = ?", (pelicula_id,)
            )
            resultado = cursor.fetchone()[0]
            return resultado if resultado else 0
        return dal.metodo_general(self.db_path, accion)

    def registrar_entrada(self, cliente, cantidad, pelicula_id):
        # Valida datos del cliente y cantidad
        if not cliente or cantidad <= 0:
            raise ValueError("Datos inválidos para la compra de entradas.")

        # Controla que no se exceda la capacidad de la sala
        capacidad = self.pelicula_service.obtener_capacidad_sala(pelicula_id)
        vendidas = self.entradas_vendidas(pelicula_id)
        if vendidas + cantidad > capacidad:
            raise ValueError("No hay entradas suficientes disponibles para esta película.")

        # Registra la compra
        dal.inserta_entrada(self.db_path, cliente, cantidad, pelicula_id)

    def obtener_compras_cliente(self, cliente):
        if not cliente:
            raise ValueError("Debe ingresar un nombre de cliente válido.")
        return dal.traer_entradas_por_cliente(self.db_path, cliente)

# Servicio para inicializar la base de datos
class BaseService:
    def __init__(self, db_path):
        self.db_path = db_path

    def inicializar_base(self, borrar_existentes=False):
        # Crea las tablas necesarias, con opción de borrar las anteriores
        dal.crear_tablas(self.db_path, borrar_existentes)

# Clase central que conecta todos los servicios
class CineManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.sala_service = SalaService(db_path)
        self.pelicula_service = PeliculaService(db_path)
        self.entrada_service = EntradaService(db_path, self.pelicula_service)
        self.base_service = BaseService(db_path)

    def inicializar_sistema(self, borrar_existentes=False):
        # Llama a base_service para crear la base de datos
        self.base_service.inicializar_base(borrar_existentes)

