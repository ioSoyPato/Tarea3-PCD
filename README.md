# FastAPI User Management System

## Descripción

Este proyecto es un sistema básico de gestión de usuarios desarrollado con FastAPI, una de las librerías más populares para la creación de APIs en Python. El proyecto permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) sobre una base de datos de usuarios, almacenando información relevante como nombre, correo electrónico, edad, código postal y una lista de recomendaciones personalizadas para cada usuario.

El objetivo de este proyecto es demostrar las habilidades adquiridas en la materia de desarrollo de aplicaciones web con Python, enfocándose en:

- La creación de una API RESTful utilizando FastAPI.
- La validación de datos entrantes usando Pydantic.
- La interacción con una base de datos utilizando SQLAlchemy.
- La serialización y deserialización de datos complejos (como listas) para almacenarlos en una base de datos.

## Características

- **Creación de Usuarios:** Puedes agregar nuevos usuarios proporcionando un nombre, correo electrónico, edad, código postal y una lista opcional de recomendaciones.
- **Lectura de Usuarios:** Puedes consultar todos los usuarios registrados o las recomendaciones específicas de un usuario.
- **Actualización de Usuarios:** Puedes actualizar la información de un usuario existente, incluyendo su lista de recomendaciones.
- **Eliminación de Usuarios:** Puedes eliminar un usuario de la base de datos.
- **Serialización y Deserialización:** La lista de recomendaciones se serializa en un string JSON para almacenarla en la base de datos y se deserializa de vuelta a una lista cuando se recupera.

## Estructura del Proyecto

El proyecto se organiza en los siguientes archivos principales:

- **main.py:** Contiene la lógica principal de la API, definiendo las rutas y los controladores para las operaciones CRUD.
- **models.py:** Define el modelo de datos `User` utilizando SQLAlchemy, incluyendo métodos para serializar y deserializar la lista de recomendaciones.
- **database.py:** Configura la conexión a la base de datos SQLite y proporciona las funciones necesarias para interactuar con la base de datos.

## Instalación y Ejecución

Para ejecutar este proyecto en tu máquina local, sigue estos pasos:

1. **Clona el repositorio:**

    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

2. **Crea un entorno virtual y activa el entorno:**

    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Inicia el servidor:**

    ```bash
    uvicorn main:app --reload
    ```

5. **Accede a la API:**

    La API estará disponible en `http://127.0.0.1:8000`. Puedes interactuar con la API utilizando herramientas como [Postman](https://www.postman.com/) o directamente desde tu navegador en la ruta `/docs` para acceder a la documentación automática generada por FastAPI.

## Demostración de Conocimientos

Este proyecto demuestra la aplicación de varios conceptos y habilidades aprendidas en la materia, incluyendo:

- **FastAPI y Pydantic:** Uso de FastAPI para la creación de una API RESTful y Pydantic para la validación y el manejo de datos entrantes.
- **SQLAlchemy:** Interacción con una base de datos utilizando ORM (Object-Relational Mapping) para gestionar las operaciones CRUD.
- **Serialización de Datos:** Implementación de funciones para convertir estructuras de datos complejas (listas) a un formato adecuado para el almacenamiento en la base de datos, y su posterior deserialización.
- **Gestión de Sesiones de Base de Datos:** Manejo adecuado de la conexión a la base de datos utilizando sesiones de SQLAlchemy para garantizar que los recursos se gestionen correctamente.

## Futuras Mejoras

Algunas mejoras que podrían implementarse en este proyecto incluyen:

- **Autenticación y Autorización:** Añadir un sistema de autenticación para controlar el acceso a la API.
- **Pruebas Unitarias:** Incluir pruebas automatizadas para garantizar el correcto funcionamiento de la API.
- **Despliegue:** Desplegar la API en un servicio de hosting como Heroku o AWS para que esté accesible de manera pública.

## Contribuciones

Las contribuciones a este proyecto son bienvenidas. Si tienes ideas para mejorar el código, no dudes en abrir un `issue` o enviar un `pull request`.

