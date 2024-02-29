# ST0263-241 <topicos.telematica>

# Estudiante: David Madrid Restrepo, dmadridr@eafit.edu.co

# Profesor: Alvaro Enrique Ospina Sanjuan, aospinas@eafit.brightspace.com

# <para borrar: renombre este archivo a README.md cuando lo vaya a usar en un caso específico>

# Reto No 1 y 2: P2P - Comunicación entre procesos mediante API REST y RPC

# 1. Descripción de la actividad
Implementación de un sistema P2P con arquitectura de microservicios, usando tanto REST API como gRPC para la comunicación entre los clientes y los servidores, y entre los peer. La arquitectura de microservicios está estructurada de manera modular con funciones específicas para correr endpoints únicos, haciendo así que los microservicios estén encapsulados. Adicionalmente, la comunicación peer-to-peer es facilitada gracias a que usa gRPC entre los peers, para permitir la transferencia dummy de archivos.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

La implementación cumple con los requisitos de descomponer la arquitectura en componentes de servidor, cliente y peer-to-peer, empleando gRPC para la comunicación de microservicios y REST API para la interacción entre el cliente y el servidor.

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Para los requerimientos funcionales y no funcionales definidos explícitamente dentro del enunciado, no existe un aspecto que no se haya cumplido con lo requerido, sin embargo, sería bueno implementar para una futura versión, un sistema de seguridad en la autenticación.

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

 - **Diseño de alto nivel:** El sistema se adhiere a una arquitectura cliente-servidor, en la cual el servidor desempeña el papel de un componente centralizado encargado de gestionar las interacciones entre los clientes y los pares. Los pares se comunican entre sí a través de un modelo de comunicación entre peers (P2P) facilitado por gRPC.
 - **Arquitectura:**
	 - **Arquitectura cliente-servidor:** Los clientes interactúan con el servidor a través de las API RESTful, las cuales se encargan de gestionar diversas operaciones como el inicio de sesión, cierre de sesión, indexación y recuperación de archivos. Por su parte, el servidor mantiene una lista de peers registrados y se encarga de administrar las solicitudes de indexación y recuperación de archivos provenientes de los clientes. 
	 - **Comunicación entre pares:** Los peers establecen comunicación entre sí mediante gRPC, lo cual permite una comunicación eficiente y asíncrona para la transferencia de archivos. Cada peer aloja un servicio que se encarga de escuchar las solicitudes de descarga provenientes de otros peer y responde en consecuencia.
 - **Patrones de diseño:** 
	 - **Modelo-Vista-Controlador (MVC):** Flask sigue el patrón MVC, en el cual los modelos representan las estructuras de datos, las vistas muestran los datos al usuario y los controladores gestionan la entrada del usuario y orquestan las interacciones. 
	 - **Patrón cliente-servidor:** El patrón cliente-servidor se utiliza para las interacciones cliente-servidor, donde los clientes (peers) realizan solicitudes al servidor para llevar a cabo diversas operaciones. 
	 - **Arquitectura orientada a servicios (SOA):** El sistema se diseña con principios orientados a servicios, en los cuales las funcionalidades se dividen en servicios independientes, como el servidor y el servicio de peers.
	 - **Patrón de repositorio:** El sistema emplea un patrón de repositorio para abstraer las operaciones de acceso a datos, encapsulando la lógica de acceso a datos en funciones como load_logged_peers y write_logged_peer.
 - **Buenas prácticas:** 
	 - **División de intereses:** El código base se encuentra estructurado de manera que separa las funciones, estableciendo una clara distinción entre la lógica del servidor, la comunicación entre peers y las interacciones con el cliente. 
	 - **Reutilización de código:** Las funciones y componentes han sido diseñados con el propósito de ser reutilizables y modulares, lo cual facilita el mantenimiento y la extensibilidad del código. 
	 - **Escalabilidad y rendimiento:** Se emplea la comunicación asíncrona y la concurrencia para mejorar la escalabilidad y el rendimiento del sistema, especialmente en la gestión de múltiples solicitudes de clientes y transferencias entre peers. 
	 - **Manejo de errores:** Se ha implementado un manejo básico de errores para abordar los errores más comunes de manera elegante, garantizando la robustez y confiabilidad del sistema.

# 3. Descripción del ambiente de desarrollo y técnico
## Lenguaje
Python 3.9
## Framework Web
Flask en su última versión a la fecha (2.0.2)
## Protocolo de comunicación
HTTP y gRCP
## Librerías
- grcpio
- grcpio-tools
- flask
- requests
- json
- concurrent.future

## Compilación y ejecución
Para la compilación, es necesario primero hacer un docker build de los 3 archivos "Dockerfile", para ello, ejecutamos los siguientes comandos respectivamente,

    docker build -t main-server
	docker run -p hostPort:dockerPort main-server
  Una vez hecho esto, en la ejecución saldrá una IP en la cual el servidor está corriendo, es necesario anotarla ya que se necesitará para terminar de configurar el cliente
  
    docker build -t peer-server
    docker run -p hostPort:dockerPort peer-server
Una vez hecho esto, en la ejecución saldrá una IP en la cual el PServer está corriendo, es necesario anotarla ya que se necesitará para terminar de configurar el cliente.

  Luego, cambiaremos las IP con sus puertos respectivos dentro de peer/p_client/config.ini. Y por último, haremos build del docker peer-client y run para ejecutarlo

    docker build -t peer-client
    docker run -ti peer-client

Donde la flag -p nos ayuda a hacer un port mapping de los puertos especificados, y la flag -ti le indica al contenedor que el programa recibirá input por la terminal, ya que el cliente está basado en CLI.
### Nota adicional
En caso tal de que el programa encuentre errores a la hora de ejecutar las librerías relacionadas con _pb2 y con _pb2_grcp, es necesario ejecutar el comando

    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. peer_service.proto
Con este podremos generar las librerías necesarias para ejecutar el código con gRCP.
    

## Configuración parámetros
La configuración tanto del servidor, como del cliente se hace a través de unos archivos .ini, los cuales contienen la siguiente información

    [Servidor.ini]  
    ip = 127.0.0.1  
    puerto = 5000  
    
    [Cliente.ini]  
    ip_servidor = 127.0.0.1 
    puerto_servidor = 5000
    ip_servidor_peer = 127.0.0.1 
    puerto_servidor = 50051
	
	[PServer.ini]
	puerto = 50051
	sleep_time = 86400
También, se tiene que para la base de datos, se está usando un archivo tipo JSON, el cual está almacenando toda la información relevante para el correcto funcionamiento de la implementación.

## Detalles técnicos
El proyecto se estructura en un sistema de directorios que separa la lógica del servidor, el cliente y los servicios de los pares. Para la implementación del servidor se utiliza Flask, un framework web ligero para Python. Se definen rutas para manejar las solicitudes de los clientes, tales como /login, /logout, /indexFiles, /getFiles. El intercambio de datos entre el servidor y los clientes se realiza mediante el uso de JSON. El servidor mantiene un registro de los pares conectados y sus archivos indexados en un archivo JSON llamado "logged_peers.json". Cada peer cuenta con un nombre de usuario, una dirección IP y una lista de archivos indexados asociados. Se han implementado funciones para cargar, escribir y eliminar pares del registro. Por otro lado, el cliente se ha desarrollado como un script independiente o módulo que interactúa con el servidor a través de solicitudes HTTP. 
El cliente tiene la capacidad de enviar solicitudes de inicio de sesión, cierre de sesión, indexación de archivos y recuperación de archivos al servidor. 
La comunicación entre los peers se lleva a cabo utilizando gRPC, donde cada peer implementa un servicio gRPC que permite a otros pares solicitar la descarga de archivos; el servicio gRPC de los peers escucha las solicitudes de descarga de archivos provenientes de otros pares, cuando se recibe una solicitud de descarga, el servicio responde con el archivo solicitado en caso de estar disponible.

## Estructura directorios y archivos importantes
    +---peer
	|   |   proto.sh
	|   |
	|   +---p_client
	|   |       Dockerfile
	|   |       peer_service.proto
	|   |       peer_service_pb2.py
	|   |       peer_service_pb2_grpc.py
	|   |       p_client.py
	|   |       requirements.txt
	|   |
	|   \---p_server
	|           Dockerfile
	|           peer_service.proto
	|           peer_service_pb2.py
	|           peer_service_pb2_grpc.py
	|           p_server.py
	|           requirements.txt
	|
	+---server
	|       Dockerfile
	|       requirements.txt
	|       sv copy.py
	|       sv.py
	|
	\---__pycache__
	        peer_service_pb2.cpython-311.pyc

## Guía rápida de cómo usar la aplicación
Para empezar, clonar el repositorio INSERTE URL DE GITHUB, luego, hacer los pasos especificados en el punto 3 para hacer el docker build, la generación de los archivos relevantes para gRCP y hacer docker run, habiendo configurado previamente el archivo .ini del servidor y del cliente con sus respectivos datos. Luego de eso, podremos lanzar una instancia cliente, la cual nos saldrá con un menú de 5 opciones

    1. Login
	2. Logout
	3. Index Files
	4. Get Files
	5. Exit
	Enter your choice: X
Cada opción dentro del menú, indica un microservicio expuesto por el servidor. Cabe aclarar que para hacer logout, index y/o get, se necesita primero haberse logeado con el servidor, de lo contrario, no se podrá acceder a los microservicios especificados.

# Referencias:

- gRCP (https://grpc.io/) 
- Repo del curso (https://github.com/st0263eafit/st0263-241/tree/main)
- requests (https://requests.readthedocs.io/en/latest/)
- concurrent.futures (https://docs.python.org/3/library/concurrent.futures.html)
- configparser (https://docs.python.org/3/library/configparser.html)
- socket (https://docs.python.org/3/library/socket.html)
- Docker (https://docs.docker.com/)
- protobuf (https://protobuf.dev/overview/)
