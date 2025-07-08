import dal

class SalaService:
    def __init__(self, db_path):
        self.db_path = db_path

    def agregar_sala(self, nombre, capacidad):
        if not nombre or capacidad <= 0:
            raise ValueError("Datos inválidos para la sala.")
        dal.inserta_sala(self.db_path, nombre, capacidad)

    def obtener_salas(self):
        return dal.traer_salas(self.db_path)

class PeliculaService:
    def __init__(self, db_path):
        self.db_path = db_path

    def agregar_pelicula(self, titulo, horario, sala_id):
        if not titulo or not horario or sala_id is None:
            raise ValueError("Todos los campos de la película son obligatorios.")

        # Chequeo de superposición
        peliculas_existentes = self.obtener_cartelera()
        for p in peliculas_existentes:
            id_pelicula, titulo_existente, horario_existente, sala_id_existente = p
            if horario.strip() == horario_existente.strip() and sala_id == sala_id_existente:
                raise ValueError(f"No se puede agregar dos películas en la misma sala ({sala_id}) y horario ({horario}).")

        dal.inserta_pelicula(self.db_path, titulo, horario, sala_id)

    def obtener_cartelera(self):
        return dal.traer_peliculas(self.db_path)

class EntradaService:
    def __init__(self, db_path):
        self.db_path = db_path

    def registrar_entrada(self, cliente, cantidad, pelicula_id):
        if not cliente or cantidad <= 0:
            raise ValueError("Datos inválidos para la compra de entradas.")
        dal.inserta_entrada(self.db_path, cliente, cantidad, pelicula_id)

    def obtener_compras_cliente(self, cliente):
        if not cliente:
            raise ValueError("Debe ingresar un nombre de cliente válido.")
        return dal.traer_entradas_por_cliente(self.db_path, cliente)

class BaseService:
    def __init__(self, db_path):
        self.db_path = db_path

    def inicializar_base(self, borrar_existentes=False):
        dal.crear_tablas(self.db_path, borrar_existentes)

class CineManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.sala_service = SalaService(db_path)
        self.pelicula_service = PeliculaService(db_path)
        self.entrada_service = EntradaService(db_path)
        self.base_service = BaseService(db_path)

    def inicializar_sistema(self, borrar_existentes=False):
        self.base_service.inicializar_base(borrar_existentes)