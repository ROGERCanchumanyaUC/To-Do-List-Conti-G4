# OOPRA — Gestor de Tareas (Python + SQLite + Docker)

## 1) Descripción general del proyecto
**OOPRA** es una herramienta desarrollada en **Python** que permite a los usuarios **gestionar y organizar sus tareas diarias**.  
La aplicación cumple funciones esenciales como **añadir, editar, eliminar y marcar tareas como completadas**, asegurando la **persistencia de datos** mediante una base de datos **SQLite**.  
El proyecto está versionado con **Git/GitHub** y utiliza **Docker** para estandarizar el entorno de desarrollo.

---

## 2) Objetivo de la aplicación
El objetivo de **OOPRA** es brindar una solución simple y organizada para:
- Registrar tareas diarias.
- Actualizar información de tareas existentes.
- Eliminar tareas que ya no son necesarias.
- Marcar tareas como completadas para reflejar el progreso del usuario.
- Mantener los datos persistentes mediante **SQLite** en el archivo **DB.sqlite**.
- Permitir la ejecución del proyecto de forma reproducible usando **Docker**.

---

## 3) Integrantes del equipo
- Integrante 1: Canchumanya Avellaneda Roger
- Integrante 2: De La Cruz Cardenas Antony
- Integrante 3: Ochoa Vilchez Diego
- Integrante 4: Zamudio Benito Dayaneira

---

## 4) Tecnologías y requisitos técnicos
- **Lenguaje:** Python  
- **Base de datos:** SQLite (**persistencia en DB.sqlite**)  
- **Control de versiones:** Git + GitHub  
- **IDE:** PyCharm  
- **Contenedorización:** Docker  

---
## 5) Estructura del proyecto
```text
To-Do-List-Conti-G4/
│
├── main.py
├── DB.sqlite
├── BD.sql
├── src/
│   ├── logica/
│   │   └── task_manager.py
│   ├── modelo/
│   │   ├── bd_model.py
│   │   ├── conexion.py
│   │   └── repositorio_tareas.py
│   └── tests/
│       ├── test_task_manager.py
│       └── cobertura_extra.py
│
├── .gitignore
└── README.md
```
---
## 6) Instalación y configuración
  - Clonar el repositorio
    - git clone https://github.com/ROGERCanchumanyaUC/To-Do-List-Conti-G4.git
cd To-Do-List-Conti-G4
  - Crear y activar el entorno virtual
    - python -m venv .venv
    - .venv\Scripts\activate
  - Instalar dependencias
    - pip install -r requirements.txt
---
## 7) Inicialización de la base de datos
  - Ejecutar el siguiente comando:
    - python main.py
  - Este comando:
    - Crea o verifica la base de datos DB.sqlite

    - Crea las tablas mediante SQLAlchemy

    - Ejecuta el script BD.sql

    - Muestra un resumen de las tablas creadas
---
## 8) Uso de la aplicación
  - La aplicación permite:
    - Crear tareas

    - Listar tareas por usuario

    - Editar tareas

    - Eliminar tareas

    - Marcar tareas como completada
---
## 9) Ejecución de pruebas
  - Para ejecutar las pruebas unitarias:
    - python -m unittest discover -s src/tests -v
---
## 10) Control de versiones (Git)
  - El proyecto sigue buenas prácticas de Git:
    - Commits atómicos y descriptivos

    - Historial de cambios coherente

    - Uso de ramas para organizar el desarrollo

    - Archivo .gitignore adecuado para proyectos Python

