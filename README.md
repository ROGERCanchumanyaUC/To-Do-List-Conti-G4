```markdown
# OOPRA – Gestor de Tareas (Python + SQLite + Docker)

Herramienta de línea de comandos (CLI) para **gestionar y organizar tareas diarias**. Permite **crear, listar, editar, eliminar** y **marcar tareas como completadas**, asegurando **persistencia** en una base de datos **SQLite** (`DB.sqlite`). El proyecto se desarrolla con **TDD**, control de versiones con **Git/GitHub**, y entorno reproducible con **Docker**.

---

## Objetivo de la aplicación

- Centralizar el registro de tareas diarias.
- Mantener la información persistente en `DB.sqlite`.
- Aplicar buenas prácticas: **PEP-8**, arquitectura por capas (lógica / modelo), **TDD** y **cobertura de pruebas**.
- Generar documentación técnica con **Sphinx** (incluyendo módulos y tests).

---

## Integrantes del equipo

- Canchumanya Avellaneda Roger
- De La Cruz Cardenas Antony
- Ochoa Vilchez Diego 
- Zamudio Benito Dayaneira

---

## Requisitos técnicos

- **Python** (trabajando con entorno virtual `.venv`)
- **SQLite** (archivo persistente `DB.sqlite` en la raíz del proyecto)
- **Git + GitHub** (ramas por funcionalidad `feature/huXX-*`)
- **Docker** (entorno reproducible)
- **PyCharm** (IDE sugerido por la consigna)

---

## Estructura del proyecto (actual)

```test

OOPRA/
├─ DB.sqlite
├─ main.py
├─ requirements.txt
├─ src/
│  ├─ **init**.py
│  ├─ logica/
│  │  ├─ **init**.py
│  │  └─ task_manager.py
│  ├─ modelo/
│  │  ├─ **init**.py
│  │  ├─ conexion.py
│  │  ├─ bd_model.py
│  │  └─ repositorio_tareas.py
│  └─ tests/
│     ├─ **init**.py
│     ├─ test_task_manager.py
│     └─ (otros tests)
└─ docs/
├─ make.bat
├─ Makefile
├─ source/
└─ build/
```
---

## Historias de Usuario (rama por funcionalidad)

Cada historia se desarrolla en una rama independiente, siguiendo el esquema:

- `feature/hu01-login`
- `feature/hu02-crear-tarea`
- `feature/hu03-ver-lista`
- `feature/hu04-editar-tarea`
- `feature/hu05-eliminar-tarea`
- `feature/hu06-marcar-completada`

> **Regla académica:** las ramas **no se eliminan**; deben quedar visibles en el repo remoto como evidencia.

---

## Instalación y ejecución (Windows / PowerShell)

### 1) Crear y activar entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\activate
````

### 2) Instalar dependencias

```powershell
pip install -r requirements.txt
```

> Si no tienes `requirements.txt` instalado en el entorno, asegúrate que `pip` apunte a tu `.venv`.

### 3) Ejecutar el proyecto

```powershell
python main.py
```

**Resultado esperado (según tu main actual):**

* Verifica/crea `DB.sqlite`
* Crea/verifica tablas ORM (SQLAlchemy)
* (Opcional) carga datos desde un `.sql` si lo agregas y lo habilitas en `main.py`

---

## Base de datos (SQLite)

### Archivo persistente

* El proyecto usa un único archivo: **`DB.sqlite`** (en la raíz del proyecto).

### Modelos ORM (SQLAlchemy)

* `src/modelo/bd_model.py` define:

  * `Usuario`
  * `Tarea`

Incluye:

* Relaciones (`Usuario` ↔ `Tarea`)
* Índices para búsquedas/listados
* Restricciones (validación del título, valores booleanos)

### Conexión

* `src/modelo/conexion.py` centraliza:

  * `ENGINE`, `SessionLocal`
  * PRAGMAs SQLite necesarios (FK ON, etc.)
  * `init_db()` para crear/verificar tablas

---

## Capa lógica y repositorio

### `src/logica/task_manager.py`

Contiene reglas de negocio para:

* Crear tarea (valida título)
* Listar tareas
* Editar tarea
* Eliminar tarea
* Marcar completada

### `src/modelo/repositorio_tareas.py`

Repositorio para persistencia con SQLAlchemy:

* Maneja transacciones
* Controla duplicados (IntegrityError)
* Evita que la capa lógica maneje SQL o sesiones directamente

---

## Pruebas (TDD) y organización

Las pruebas están en:

```
src/tests/
```

Se ejecutan con descubrimiento de `unittest`.

### Ejecutar tests

Desde la raíz del proyecto:

```powershell
python -m unittest discover -s src/tests -p "test_*.py" -v
```

---

## Cobertura de pruebas (coverage)

### 1) Instalar coverage (si aún no está)

```powershell
pip install coverage
```

### 2) Ejecutar coverage + tests

```powershell
coverage run -m unittest discover -s src/tests -p "test_*.py" -v
```

### 3) Ver reporte

```powershell
coverage report -m
```

### 4) (Opcional) Reporte HTML

```powershell
coverage html
```

Se genera en:

```
htmlcov/index.html
```

---

## Estándares de código (PEP-8 + formateo)

Se aplicó verificación y formateo automático con:

### Ruff

```powershell
python -m ruff check . --fix
python -m ruff check .
```

### Black

```powershell
python -m black .
```

### isort

```powershell
python -m isort .
```

---

## Documentación (Sphinx)

La documentación se encuentra en:

```
docs/
```

### 1) Instalar dependencias de documentación

```powershell
pip install sphinx sphinx-rtd-theme
```

### 2) Generar `.rst` automáticamente

Desde `docs/`:

```powershell
sphinx-apidoc -o source ..\src -f
```

### 3) Compilar HTML

```powershell
.\make.bat html
```

### 4) Ver HTML

El índice generado está en:

```
docs/build/html/index.html
```

En PowerShell:

```powershell
start .\build\html\index.html
```

### Documentar módulos y tests

Actualmente Sphinx está configurado para:

* Documentar módulos bajo `src/`
* Incluir también los tests (`src/tests`) si están referenciados en `toctree`

---

## Avances completados (últimos avances)

- ✅ Git y GitHub en uso
- ✅ `.gitignore` incluido
- ✅ `README.md` completo (este archivo)
- ✅ SQLite configurado y persistencia en `DB.sqlite`
- ✅ Modelos ORM (`Usuario`, `Tarea`) y relaciones
- ✅ Repositorio SQLite (transacciones + errores de integridad)
- ✅ Lógica de negocio en `TaskManager`
- ✅ Pruebas con `unittest` en `src/tests`
- ✅ Cobertura con `coverage` (reporte en consola y opcional HTML)
- ✅ Estándares PEP-8 con Ruff + Black + isort
- ✅ Documentación técnica con Sphinx (HTML generado)

---

## Problemas comunes y solución rápida

### “NO TESTS RAN”

Asegúrate de ejecutar desde la **raíz** y que tus tests estén en `src/tests/`:

```powershell
python -m unittest discover -s src/tests -p "test_*.py" -v
```

### Sphinx warning “document isn’t included in any toctree”

Incluye `modules` (y si deseas tests) en tu `index.rst`.
Luego vuelve a compilar:

```powershell
.\make.bat clean
.\make.bat html
```

