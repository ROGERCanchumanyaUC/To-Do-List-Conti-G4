"""
Script de carga inicial (seed) para DB.sqlite.

- Crea 2 usuarios con password_hash (SHA256) compatible con LoginLogica.
- Inserta 20 tareas en total:
    * 10 Pendientes (completada = 0)
    * 10 Completadas (completada = 1)

Ejecución (desde la raíz del proyecto):
    python seed_demo_data.py

Notas:
- Requiere que exista tu estructura de proyecto `src/`.
- Usa SQLAlchemy (SessionLocal) y tus modelos (Usuario, Tarea).
"""

from __future__ import annotations

from datetime import datetime, timedelta

from src.logica.login_logica import LoginLogica
from src.modelo.conexion import SessionLocal, init_db
from src.modelo.bd_model import Tarea, Usuario


def _crear_usuario_si_no_existe(
    session,
    username: str,
    password_plano: str,
) -> Usuario:
    usuario = session.query(Usuario).filter_by(username=username).first()
    if usuario is not None:
        return usuario

    password_hash = LoginLogica.generar_hash(password_plano)
    usuario = Usuario(username=username, password_hash=password_hash)
    session.add(usuario)
    session.flush()  # genera id_usuario
    return usuario


def _crear_tarea(
    id_usuario: int,
    titulo: str,
    descripcion: str,
    completada: bool,
    creada_en: datetime,
) -> Tarea:
    return Tarea(
        id_usuario=id_usuario,
        titulo=titulo,
        descripcion=descripcion,
        completada=bool(completada),
        creada_en=creada_en,
    )


def main() -> None:
    init_db()

    # ====== CONFIG: 2 USUARIOS (cámbialos si deseas) ======
    usuarios_seed = [
        {"username": "Juan", "password": "admin123"},
        {"username": "Marleni", "password": "colab123"},
    ]

    session = SessionLocal()
    try:
        u1 = _crear_usuario_si_no_existe(
            session, usuarios_seed[0]["username"], usuarios_seed[0]["password"]
        )
        u2 = _crear_usuario_si_no_existe(
            session, usuarios_seed[1]["username"], usuarios_seed[1]["password"]
        )
        session.commit()
        session.refresh(u1)
        session.refresh(u2)

        ahora = datetime.now()

        # ====== TAREAS REALISTAS (20 total) ======
        # 10 por usuario (5 pendientes + 5 completadas) => total 10 pendientes / 10 completadas
        u1_pendientes = [
            (
                "Preparar informe semanal",
                "Resumir avances del proyecto, riesgos y próximos pasos. "
                "Adjuntar métricas y capturas relevantes.",
            ),
            (
                "Revisar pull request de la API",
                "Validar estilo, pruebas y manejo de errores. "
                "Dejar comentarios y solicitar cambios si corresponde.",
            ),
            (
                "Llamar al proveedor de internet",
                "Consultar interrupciones recientes y solicitar mejora de estabilidad. "
                "Pedir número de ticket y tiempo estimado.",
            ),
            (
                "Actualizar README del repositorio",
                "Agregar instrucciones de instalación, ejecución de tests y estructura del proyecto. "
                "Verificar que funcione en Windows.",
            ),
            (
                "Planificar tareas de la semana",
                "Definir prioridades (alto/medio/bajo), estimación y dependencias. "
                "Bloquear tiempos de foco en el calendario.",
            ),
        ]

        u1_completadas = [
            (
                "Instalar dependencias del entorno",
                "Se creó el entorno virtual y se instalaron requerimientos. "
                "Se validó que `python -m unittest -v` ejecute sin errores.",
            ),
            (
                "Diseñar mockup del dashboard",
                "Se definió layout: header, tarjetas de estadísticas y listas de tareas. "
                "Se alineó con estilo profesional y tipografías.",
            ),
            (
                "Configurar base de datos SQLite",
                "Se generó DB.sqlite y se verificaron tablas `usuarios` y `tareas`. "
                "Se habilitaron PRAGMAs de integridad.",
            ),
            (
                "Implementar búsqueda por título",
                "Se conectó el input de búsqueda con la vista y se filtra por coincidencia parcial. "
                "Se mantiene el comportamiento al limpiar el texto.",
            ),
            (
                "Corregir estilos de botones",
                "Se ajustaron colores y estados hover/pressed para mejorar contraste. "
                "Se revisó que los textos sean legibles.",
            ),
        ]

        u2_pendientes = [
            (
                "Organizar carpeta de recursos",
                "Ordenar imágenes, iconos y archivos QSS. "
                "Eliminar duplicados y nombrar de forma consistente.",
            ),
            (
                "Preparar presentación para clase",
                "Crear una diapositiva por HU (login, CRUD, completar). "
                "Incluir arquitectura por capas y captura del UI.",
            ),
            (
                "Registrar tareas de ejemplo",
                "Cargar un set de tareas reales para demo. "
                "Verificar que pendientes y completadas se muestren bien.",
            ),
            (
                "Revisar reglas de negocio",
                "Confirmar validaciones: título obligatorio, duplicados por usuario, "
                "y permisos por sesión activa.",
            ),
            (
                "Optimizar rendimiento del listado",
                "Revisar creación/destrucción de widgets en layouts. "
                "Evitar refrescos innecesarios al buscar.",
            ),
        ]

        u2_completadas = [
            (
                "Integrar navegación con QStackedWidget",
                "Se conectaron señales entre login, dashboard y registrar tarea. "
                "Se validó el flujo volver/cerrar sesión.",
            ),
            (
                "Agregar validación de campos en registrar tarea",
                "Se bloquea guardar sin título y se muestra mensaje al usuario. "
                "Se limpia formulario al cancelar.",
            ),
            (
                "Implementar edición de tareas",
                "Se carga la tarea en el formulario, se actualiza y se vuelve al dashboard. "
                "Se mantiene consistencia de datos.",
            ),
            (
                "Marcar tareas como completadas",
                "Se añadió botón de completar y actualiza el estado en BD. "
                "La tarea pasa a la sección de completadas.",
            ),
            (
                "Configurar estructura del proyecto",
                "Se organizaron carpetas `logica`, `modelo`, `vista` y `tests`. "
                "Se verificaron imports y __init__.py.",
            ),
        ]

        tareas: list[Tarea] = []

        # Fechas escalonadas para que se vea natural en la UI
        def _fecha_con_offset(dias_atras: int) -> datetime:
            return ahora - timedelta(days=dias_atras)

        # Usuario 1: 5 pendientes + 5 completadas
        for idx, (titulo, desc) in enumerate(u1_pendientes, start=1):
            tareas.append(
                _crear_tarea(
                    id_usuario=int(u1.id_usuario),
                    titulo=titulo,
                    descripcion=desc,
                    completada=False,
                    creada_en=_fecha_con_offset(30 - idx),
                )
            )

        for idx, (titulo, desc) in enumerate(u1_completadas, start=1):
            tareas.append(
                _crear_tarea(
                    id_usuario=int(u1.id_usuario),
                    titulo=titulo,
                    descripcion=desc,
                    completada=True,
                    creada_en=_fecha_con_offset(20 - idx),
                )
            )

        # Usuario 2: 5 pendientes + 5 completadas
        for idx, (titulo, desc) in enumerate(u2_pendientes, start=1):
            tareas.append(
                _crear_tarea(
                    id_usuario=int(u2.id_usuario),
                    titulo=titulo,
                    descripcion=desc,
                    completada=False,
                    creada_en=_fecha_con_offset(12 - idx),
                )
            )

        for idx, (titulo, desc) in enumerate(u2_completadas, start=1):
            tareas.append(
                _crear_tarea(
                    id_usuario=int(u2.id_usuario),
                    titulo=titulo,
                    descripcion=desc,
                    completada=True,
                    creada_en=_fecha_con_offset(6 - idx),
                )
            )

        # Insertar evitando duplicados por UniqueConstraint (id_usuario, titulo)
        insertadas = 0
        for t in tareas:
            existe = (
                session.query(Tarea)
                .filter_by(id_usuario=t.id_usuario, titulo=t.titulo)
                .first()
            )
            if existe is None:
                session.add(t)
                insertadas += 1

        session.commit()

        print("✅ Seed completado.")
        print(
            f"Usuarios: {u1.username} (id={u1.id_usuario}), "
            f"{u2.username} (id={u2.id_usuario})"
        )
        print(f"Tareas insertadas (nuevas): {insertadas}")
        print("Credenciales:")
        print(f" - {usuarios_seed[0]['username']} / {usuarios_seed[0]['password']}")
        print(f" - {usuarios_seed[1]['username']} / {usuarios_seed[1]['password']}")

    finally:
        session.close()


if __name__ == "__main__":
    main()
