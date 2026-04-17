# IronMind Academy 🏋️‍♂️🛡️

**IronMind Academy** es una plataforma web integral diseñada para la gestión de entrenamientos y el fomento de comunidades de powerlifting y fitness.

Este proyecto representa la evaluación final para el **Instituto Tecnológico de Las Américas (ITLA)**. Su desarrollo integra un ciclo de vida de software seguro (**S-SDLC**) mediante prácticas de **DevSecOps**, análisis profundo de vulnerabilidades y despliegue automatizado con contenedores.

---

## 🚀 Características Principales

* **Gestión de Identidad:** Sistema de autenticación con contraseñas protegidas mediante algoritmos de hashing robustos.
* **Dashboard de Rendimiento:** Seguimiento detallado de medidas físicas, récords personales (RMs) y rutinas de entrenamiento.
* **Comunidad Interactiva:** Chat grupal diseñado para manejar múltiples peticiones concurrentes.
* **Infraestructura Resiliente:** Arquitectura basada en microservicios con persistencia de datos mediante volúmenes de Docker.

---

## 🛠️ Stack Tecnológico

* **Lenguaje y Framework:** Python 3.13.5 y Flask.
* **Servidor Web:** Werkzeug 3.0.1.
* **Frontend:** HTML5, Tailwind CSS y componentes dinámicos en JavaScript.
* **Base de Datos:** SQLite con persistencia gestionada en el directorio `/app/instance`.
* **Contenedorización:** Imagen base optimizada `python:3.13-slim` para reducir la superficie de ataque.

---

## 🔒 Auditorías de Seguridad Realizadas

La aplicación ha sido sometida a un riguroso proceso de seguridad para garantizar la integridad de los datos:

1. **Análisis Estático (SAST):** Se utilizó **SonarQube** para procesar 1.2 millones de líneas de código, identificando vulnerabilidades y "hotspots" de seguridad.
2. **Análisis Dinámico (DAST):** Mediante **OWASP ZAP 2.17.0**, se detectaron y categorizaron 18 alertas de seguridad (incluyendo fallos en tokens CSRF y políticas CSP) en tiempo de ejecución.
3. **Seguridad de Infraestructura:** Escaneo de contenedores con **Trivy**, detectando 9 vulnerabilidades de severidad alta en la capa del sistema operativo y dependencias críticas como Gunicorn y Werkzeug.

---

## 📦 Despliegue con Docker

Para una evaluación rápida y estandarizada, se recomienda utilizar la imagen alojada en **Docker Hub**.

### Instrucciones de Ejecución

1. Asegúrese de que el motor de Docker esté activo en su sistema.
2. Ejecute el siguiente comando para descargar e iniciar el contenedor con persistencia de base de datos:

```bash
docker run -d -p 5000:5000 -v ironmind_db:/app/instance --name ironmind_app titosuin/ironmind-academy:v1.0
Acceda a la aplicación en: http://localhost:5000


💻 Desarrollo Local (Debug)
Si prefiere inspeccionar el código o realizar pruebas locales:

Clonar el repositorio:


git clone [https://github.com/titosuin/web_appp.git](https://github.com/titosuin/web_appp.git)
cd web_appp
Configurar entorno:


python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Iniciar:


python app.py
