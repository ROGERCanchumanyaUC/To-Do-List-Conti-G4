# OOPRA – Gestor de Tareas (Python + SQLite + PyQt6)

Aplicación de escritorio con interfaz gráfica para
**gestionar y organizar tareas diarias**. Permite
**crear, listar, editar, eliminar** y
**marcar tareas como completadas**, con
**persistencia** en una base de datos **SQLite** (`DB.sqlite`).
El proyecto se desarrolla con **TDD**, control de versiones con **Git/GitHub**,
entorno reproducible con **Docker**, e interfaz visual con **PyQt6**.

---

## Objetivo de la aplicación

- Centralizar el registro de tareas diarias con interfaz gráfica moderna.
- Mantener la información persistente en `DB.sqlite`.
- Aplicar buenas prácticas: **PEP-8**, arquitectura por capas (vista / lógica / modelo), **TDD** y **cobertura de pruebas**.
- Generar documentación técnica con **Sphinx**.

---

## Integrantes del equipo

| Integrante | Ramas a cargo |
|---|---|
| Zamudio Benito Dayaneira | `feature/hu01-login`, `feature/hu04-editar-tarea` |
| Ochoa Vilchez Diego | `feature/hu02-crear-tarea`, `feature/hu05-eliminar-tarea` |
| Canchumanya Avellaneda Roger | `feature/hu03-ver-lista`, `feature/hu06-marcar-completada` |
| De La Cruz Cardenas Antony |`feature/vista` |

---

## Requisitos técnicos

- **Python** (entorno virtual `.venv`)
- **SQLite** (archivo persistente `DB.sqlite` en la raíz del proyecto)
- **PyQt6** (interfaz gráfica de escritorio)
- **SQLAlchemy** (ORM para acceso a la base de datos)
- **Git + GitHub** (ramas por funcionalidad `feature/huXX-*`)
- **Docker** (entorno reproducible)
- **PyCharm** (IDE sugerido)

---

## Estructura del proyecto (actual)
```
OOPRA/
├── DB.sqlite
├── main.py
├── seed_demo_data.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── logica/
│   │   ├── __init__.py
│   │   ├── task_manager.py
│   │   └── login_logica.py
│   ├── modelo/
│   │   ├── __init__.py
│   │   ├── conexion.py
│   │   ├── bd_model.py
│   │   └── repositorio_tareas.py
│   ├── vista/
│   │   ├── __init__.py
│   │   ├── ventana_principal.py
│   │   ├── pantalla_login.py
│   │   ├── pantalla_dashboard.py
│   │   ├── pantalla_registrar_tarea.py
│   │   ├── controladores.py
│   │   └── animaciones.py
│   └── tests/
│       ├── __init__.py
│       ├── test_login.py
│       └── test_task_manager.py
└── docs/
    ├── make.bat
    ├── Makefile
    └── source/
```

---

## Historias de Usuario implementadas

| Rama | Descripción | Responsable |
|---|---|---|
| `feature/hu01-login` | Inicio de sesión con usuario y contraseña | Dayaneria |
| `feature/hu02-crear-tarea` | Formulario para crear nueva tarea | Diego |
| `feature/hu03-ver-lista` | Dashboard con lista de tareas del usuario | Roger |
| `feature/hu04-editar-tarea` | Editar título y descripción de una tarea | Dayaneria |
| `feature/hu05-eliminar-tarea` | Botón eliminar en cada tarjeta de tarea | Diego |
| `feature/hu06-marcar-completada` | Checkbox para marcar tarea como completada | Roger |

> **Regla académica:** las ramas **no se eliminan**; deben quedar visibles en el repo remoto como evidencia.

---

## Instalación y ejecución (Windows / PowerShell)

### 1) Crear y activar entorno virtual
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

### 2) Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 3) Ejecutar el proyecto
```powershell
python main.py
```

### 4) Cargar datos de prueba (opcional)
```powershell
python seed_demo_data.py
```

---

## Interfaz gráfica (PyQt6)

### Pantallas disponibles

| Pantalla | Archivo | Descripción |
|---|---|---|
| Login | `pantalla_login.py` | Formulario de autenticación |
| Dashboard | `pantalla_dashboard.py` | Lista de tareas con tarjetas |
| Registrar/Editar | `pantalla_registrar_tarea.py` | Formulario crear o editar tarea |

### Flujo de navegación
```
Login → Dashboard → [Registrar Tarea] → Dashboard
                 → [Editar Tarea]    → Dashboard
```

---

## Base de datos (SQLite)

- `src/modelo/bd_model.py` — Modelos ORM: `Usuario`, `Tarea`
- `src/modelo/conexion.py` — `ENGINE`, `SessionLocal`, `init_db()`
- `src/modelo/repositorio_tareas.py` — CRUD con transacciones y control de duplicados

---

## Capa lógica (`src/logica/task_manager.py`)

- `crear_tarea(id_usuario, titulo, descripcion)` — HU02
- `listar_tareas(id_usuario)` — HU03
- `editar_tarea(id_usuario, id_tarea, nuevo_titulo, nueva_descripcion)` — HU04
- `eliminar_tarea(id_usuario, id_tarea)` — HU05
- `marcar_completada(id_usuario, id_tarea, completada)` — HU06

---

## Pruebas (TDD)
```powershell
python -m unittest discover -s src/tests -p "test_*.py" -v
```

---

## Cobertura de pruebas
```powershell
coverage run -m unittest discover -s src/tests -p "test_*.py" -v
coverage report -m
coverage html
```

---

## Estándares de código (PEP-8)
```powershell
python -m ruff check . --fix
python -m black .
python -m isort .
```

---

## Documentación (Sphinx)
```powershell
pip install sphinx sphinx-rtd-theme
sphinx-apidoc -o source ..\src -f
.\make.bat html
start .\build\html\index.html
```

---

## Avances completados

- ✅ Git y GitHub con ramas por historia de usuario
- ✅ SQLite configurado con persistencia en `DB.sqlite`
- ✅ Modelos ORM (`Usuario`, `Tarea`) con relaciones y restricciones
- ✅ Repositorio SQLite con transacciones y control de duplicados
- ✅ Lógica de negocio en `TaskManager` (HU02–HU06)
- ✅ Interfaz gráfica completa con PyQt6 (Login, Dashboard, Formulario)
- ✅ Navegación entre pantallas mediante señales PyQt6
- ✅ Confirmación al salir con cambios sin guardar (HU11)
- ✅ Pruebas con `unittest` en `src/tests/`
- ✅ Cobertura con `coverage`
- ✅ Estándares PEP-8 con Ruff + Black + isort
- ✅ Documentación técnica con Sphinx
