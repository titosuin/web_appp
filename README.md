# IronMind Academy 🏋️‍♂️🛡️

**IronMind Academy** es una plataforma web orientada a la gestión de entrenamientos y la creación de una comunidad para atletas de powerlifting y fitness. 

Este proyecto fue desarrollado como evaluación final para el **Instituto Tecnológico de Las Américas (ITLA)**, integrando no solo el desarrollo funcional de la aplicación, sino también la implementación de un ciclo de vida de desarrollo seguro (S-SDLC) mediante prácticas de **DevSecOps**, análisis de vulnerabilidades y contenedorización.

---

## 🚀 Características Principales

* **Autenticación y Autorización:** Sistema de login seguro con contraseñas hasheadas (Bcrypt/PBKDF2).
* **Dashboard Personalizado:** Seguimiento de datos físicos, rutinas (RMs) y progreso del usuario.
* **Comunidad Integrada:** Chat grupal interactivo para los miembros de la academia.
* **Persistencia de Datos:** Arquitectura de base de datos relacional (SQLite) con soporte para volúmenes persistentes en Docker.
* **Seguridad Auditada:** Proyecto sometido a múltiples fases de escaneo de vulnerabilidades estáticas y dinámicas.

---

## 🛠️ Stack Tecnológico

* **Backend:** Python 3.13, Flask, Werkzeug.
* **Frontend:** HTML5, Tailwind CSS, JavaScript (FullCalendar).
* **Base de Datos:** SQLite.
* **Infraestructura:** Docker (Imagen base `python:3.13-slim`).

---

## 🔒 Auditorías de Seguridad Realizadas

Como parte de los requisitos académicos y las mejores prácticas de ciberseguridad, esta aplicación fue sometida a rigurosas pruebas:

1. **Análisis Estático (SAST):** Escaneo de código fuente utilizando **SonarQube** para identificar *Code Smells*, Bugs y *Security Hotspots*.
2. **Análisis Dinámico (DAST):** Pruebas de penetración automatizadas en tiempo de ejecución utilizando **OWASP ZAP** para detectar vulnerabilidades explotables (ej. falta de tokens CSRF, configuración de cabeceras HTTP).
3. **Seguridad de Contenedores:** Escaneo de la imagen de Docker utilizando **Trivy** para identificar CVEs (Vulnerabilidades y Exposiciones Comunes) en el sistema operativo base y las dependencias de Python.

---

## 📦 Despliegue Rápido (Docker)

La forma más eficiente y recomendada para evaluar la aplicación es a través de su imagen oficial en Docker Hub. La imagen incluye todas las dependencias necesarias y está optimizada para rendimiento.

### Instrucciones de Ejecución:

1. Asegúrate de tener el demonio de Docker ejecutándose en tu sistema.
2. Ejecuta el siguiente comando para descargar la imagen, mapear los puertos y asegurar la persistencia de los datos de sesión y usuarios:

```bash
docker run -d -p 5000:5000 -v ironmind_db:/app/instance --name ironmind_app titosuin/ironmind-academy:v1.0
Accede a la aplicación desde tu navegador en: http://localhost:5000


💻 Desarrollo Local (Sin Docker)
Si deseas correr la aplicación directamente en tu entorno local para inspeccionar el código:

Clona este repositorio:


git clone [https://github.com/titosuin/Proyecto_final.git](https://github.com/titosuin/Proyecto_final.git)
Crea y activa un entorno virtual:

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
Instala las dependencias:

Bash
pip install -r requirements.txt
Ejecuta el servidor de desarrollo:

Bash
python app.py
```
