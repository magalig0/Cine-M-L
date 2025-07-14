Sistema Cine M&L


Descripción

    Este proyecto es una aplicación en Python para la gestión de un cine. Permite administrar salas, películas y la compra de entradas. Además, simula concurrencia usando hilos y procesos para manejar compras simultáneas y exportar datos.


Tecnologías usadas

    Python 3

    SQLite3 (base de datos local)

    Módulos threading y multiprocessing para concurrencia


Cómo ejecutar

    Asegurarse de tener Python 3 instalado.

    Ejecutar el archivo gui.py con el comando:

    python gui.py
    Seguir las instrucciones del menú para interactuar con la aplicación.


Estructura del proyecto

    dal.py: Manejo de base de datos (crear tablas, consultas, inserciones).

    bll.py: Lógica de negocio y servicios para salas, películas y entradas.

    concurrencia.py: Clases y funciones para hilos y procesos concurrentes.

    gui.py: Interfaz de consola para interacción con el usuario.


Manejo de concurrencia

    Se usan 5 hilos (threading.Thread) para simular compras simultáneas con exclusión mutua (Lock).

    Se usan 3 procesos (multiprocessing.Process) para tareas como exportar cartelera, contar entradas y enviar resumen.


Base de datos

    Base local SQLite llamada cine_M&L.db.

    Tablas: sala, peliculas, entradas, con relaciones entre ellas.


Autores

    Magalí Godoy: Diseño de la base de datos, implementacion del GUI, DAL y BLL y creación del diagrama de clases.

    Lucía Palombo: Desarrollo de la concurrencia, elaboración del README y documentación técnica.