# 🐍 CRUD de Usuarios con FastAPI y Análisis de Seguridad

Este proyecto implementa una API REST simple utilizando **FastAPI** para gestionar usuarios (crear, leer, actualizar, eliminar). La API utiliza una **base de datos en memoria** para facilitar su ejecución y prueba.

El objetivo principal es **educativo**: demostrar una vulnerabilidad común de **ataque de fuerza bruta** contra un endpoint de autenticación desprotegido y comprender la importancia de implementar medidas de seguridad (como Rate Limiting).

---

## 1. Archivos del Proyecto

El repositorio se compone de los siguientes archivos esenciales:

| Archivo | Descripción | Fuente |
| :--- | :--- | :--- |
| `main.py` | Código fuente de la API CRUD de FastAPI con el endpoint `/login`. Contiene un usuario semilla: **`wilian:pass123`**. | |
| `brute_api.py` | Script de demostración de **fuerza bruta** (`requests` e `itertools`) que ataca el endpoint `/login`. Está configurado para buscar el usuario **`leo`**. | |
| `requirements.txt` | Dependencias de Python necesarias para el proyecto: `fastapi`, `uvicorn`, `sqlmodel`, `requests`. | |
| `README.md` | Este archivo de documentación. | |

---

## 2. Configuración del Entorno

Sigue estos pasos para preparar tu entorno de desarrollo.

### Prerrequisitos

* **Python 3.8 o superior**.

### Instalación

1.  **Clona o descarga** el repositorio.

2.  **Crea y activa un entorno virtual** (recomendado):

    ```bash
    # Crear el entorno virtual
    python -m venv venv 
    
    # Activar en Windows
    .\venv\Scripts\activate

    # Activar en macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias.** Utiliza el archivo `requirements.txt` para instalar todas las librerías necesarias:

    ```bash
    pip install -r requirements.txt
    ```

---

## 3. Ejecución de la API

Una vez configurado el entorno, puedes iniciar el servidor de la API.

1.  Abre una terminal en la raíz del proyecto.
2.  Ejecuta el siguiente comando para iniciar el servidor con Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```

    * Alternativamente, puedes usar `fastapi dev` si lo tienes instalado.

El servidor estará activo en **`http://127.0.0.1:8000`**.

Puedes acceder a la **documentación interactiva** de la API (generada por Swagger UI) en **`http://127.0.0.1:8000/docs`**.

---

## 4. Análisis de Seguridad y Demostración de Vulnerabilidad

Esta API tiene un endpoint `/login` que es **vulnerable a ataques de fuerza bruta**. Esto se debe a dos razones principales:

1.  **No hay límite de intentos (Rate Limiting):** Un atacante puede intentar iniciar sesión miles de veces sin ser bloqueado.
2.  **No hay bloqueo de cuentas:** Una cuenta puede ser objeto de infinitos intentos fallidos sin que se bloquee temporalmente.

### Cómo Demostrar la Vulnerabilidad

El script **`brute_api.py`** está diseñado para simular este ataque en nuestro entorno local y controlado.

1.  Asegúrate de que el **servidor de la API se esté ejecutando** (Paso 3).
2.  **Crea el usuario objetivo** (`leo`) con una contraseña simple, por ejemplo, **`abc`**, utilizando el endpoint `POST /users` desde `/docs`.
3.  Abre una **segunda terminal**.
4.  Ejecuta el script de ataque. Por defecto, ya está configurado para el usuario `"leo"` y buscará la contraseña `"abc"` (hasta longitud 11):

    ```bash
    python brute_api.py
    ```

Observarás en la terminal del atacante cómo se prueban contraseñas de forma incremental hasta encontrar la correcta (`abc`). Al mismo tiempo, en la terminal del servidor API, verás el flujo de peticiones `POST /login` entrantes.
