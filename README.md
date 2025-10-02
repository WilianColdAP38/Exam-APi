# 🐍 CRUD de Usuarios con FastAPI y Prueba de Fuerza Bruta

Este repositorio contiene una API simple de CRUD (Crear, Leer, Actualizar, Eliminar) para usuarios, implementada con **FastAPI** y una base de datos en memoria (para fines de demostración). Adicionalmente, incluye un *script* de **fuerza bruta** optimizado (`brute_api.py`) para simular un ataque de credenciales contra el *endpoint* de *login*.

## 🚀 Cómo Ejecutar la API

Sigue estos pasos para levantar el servidor local de la API.

### 1. Requisitos

Asegúrate de tener **Python 3.8+** instalado.

### 2. Instalación de Dependencias

Instala las librerías necesarias utilizando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt

##Las dependencias principales son: 

fastapi, uvicorn, sqlmodel y requests.

3. Ejecutar el Servidor Uvicorn
Inicia la API ejecutando el archivo principal (main.py) con Uvicorn:

Bash

uvicorn main:app --reload
Esto levantará el servidor en http://127.0.0.1:8000.

🔒 Endpoints Clave de la API (main.py)
La API gestiona usuarios en una "base de datos" en memoria, con un usuario semilla pre-cargado: wilian con contraseña pass123.

Método	Endpoint	Descripción
POST	/users	Crea un nuevo usuario.
GET	/users	Lista todos los usuarios (sin contraseñas).
GET	/users/{user_id}	Obtiene los detalles de un usuario por ID.
PUT	/users/{user_id}	Actualiza el nombre de usuario, email o estado (is_active).
DELETE	/users/{user_id}	Elimina un usuario por ID.
POST	/login	Endpoint de autenticación. Recibe username y password. Retorna 200 OK si las credenciales son válidas.

Exportar a Hojas de cálculo
💥 Cómo Ejecutar la Prueba de Fuerza Bruta
El script brute_api.py simula un ataque de diccionario y fuerza bruta, probando contraseñas contra el endpoint /login de la API.

1. Configuración del Ataque (brute_api.py)
El script está configurado para:

URL: http://127.0.0.1:8000/login

Usuario Objetivo: "leo" (asume que este usuario fue creado previamente o existe en la base de datos).

Alfabeto: Letras minúsculas ("abcdefghijklmnopqrstuvwxyz").

Longitud Máxima: 11 caracteres.

SLEEP_TIME: Un retardo de 0.001 segundos entre peticiones para simular un ataque controlado y no saturar el servidor.

Nota: El script está diseñado para encontrar la contraseña "abc", pero el usuario objetivo "leo" (que tiene una contraseña abc en el ejemplo) no está pre-cargado. El script está actualmente configurado para buscar la contraseña 'abc' con una longitud máxima de 11, asumiendo que el usuario "leo" existe en la base de datos de la API.

2. Ejecutar el Ataque
Asegúrate de que la API (main.py) esté corriendo en segundo plano antes de iniciar el ataque.

Ejecuta el script de prueba de fuerza bruta:

Bash

python brute_api.py
El script iterará a través de todas las combinaciones de contraseñas de longitud 1 hasta MAX_LENGTH, imprimiendo el progreso y el resultado final.

3. Resultado Esperado
El ataque deberá detenerse y reportar ÉXITO al encontrar la contraseña configurada para el usuario objetivo, mostrando el tiempo total y el número de intentos realizados.

🛠️ Archivos del Repositorio
Archivo	Descripción
main.py	Implementación de la API CRUD con FastAPI y el endpoint /login.
brute_api.py	Script de fuerza bruta en Python usando requests e itertools para atacar el endpoint /login.
requirements.txt	Dependencias necesarias para el proyecto.
README.md	Este archivo.
