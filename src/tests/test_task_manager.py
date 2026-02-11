# src/tests/test_task_manager.py
from __future__ import annotations

import unittest

from sqlalchemy import select

from src.logica.task_manager import TaskManager
from src.modelo.bd_model import Tarea, Usuario
from src.modelo.conexion import SessionLocal, init_db
from src.modelo.repositorio_tareas import RepositorioTareasSQLite


class TestTaskManagerConDBReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Asegura que existan tablas en DB.sqlite (raíz)
        init_db()

        cls.repo = RepositorioTareasSQLite(session_factory=SessionLocal)
        cls.manager = TaskManager(repositorio=cls.repo)

        cls.username_test = "demo_test"
        cls.password_hash_test = "hash_demo_test"

        # Crear (o recuperar) usuario de pruebas
        with SessionLocal.begin() as session:
            session.query(Usuario).filter(
                Usuario.username == cls.username_test
            ).delete()

            stmt = select(Usuario).where(Usuario.username == cls.username_test)
            usuario = session.execute(stmt).scalar_one_or_none()

            if usuario is None:
                usuario = Usuario(
                    username=cls.username_test,
                    password_hash=cls.password_hash_test,
                )
                session.add(usuario)
                session.flush()

            cls.id_usuario = usuario.id_usuario

    def setUp(self) -> None:
        # Limpia SOLO tareas del usuario de prueba (no toca nada más)
        with SessionLocal.begin() as session:
            session.query(Tarea).filter(Tarea.id_usuario == self.id_usuario).delete()

    # HU02
    def test_crear_tarea_ok(self) -> None:
        tarea = self.manager.crear_tarea(
            self.id_usuario, "Comprar pan", "Ir a la tienda"
        )
        self.assertIsNotNone(tarea)

        tareas = self.manager.listar_tareas(self.id_usuario)
        self.assertEqual(1, len(tareas))
        self.assertEqual("Comprar pan", tareas[0].titulo)

    def test_crear_tarea_titulo_vacio_falla(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.crear_tarea(self.id_usuario, "   ", "x")

    def test_crear_tarea_duplicada_retorna_none(self) -> None:
        t1 = self.manager.crear_tarea(self.id_usuario, "Estudiar", "")
        self.assertIsNotNone(t1)

        t2 = self.manager.crear_tarea(self.id_usuario, "Estudiar", "")
        self.assertIsNone(t2)

    # HU04
    def test_editar_tarea_ok(self) -> None:
        tarea = self.manager.crear_tarea(self.id_usuario, "Original", "A")
        self.assertIsNotNone(tarea)

        ok = self.manager.editar_tarea(self.id_usuario, tarea.id_tarea, "Editada", "B")
        self.assertTrue(ok)

        tareas = self.manager.listar_tareas(self.id_usuario)
        self.assertEqual("Editada", tareas[0].titulo)

    # HU05
    def test_eliminar_tarea_ok(self) -> None:
        tarea = self.manager.crear_tarea(self.id_usuario, "Eliminar", "")
        self.assertIsNotNone(tarea)

        ok = self.manager.eliminar_tarea(self.id_usuario, tarea.id_tarea)
        self.assertTrue(ok)

        tareas = self.manager.listar_tareas(self.id_usuario)
        self.assertEqual(0, len(tareas))

    # HU06
    def test_marcar_completada_ok(self) -> None:
        tarea = self.manager.crear_tarea(self.id_usuario, "Completar", "")
        self.assertIsNotNone(tarea)

        ok = self.manager.marcar_completada(self.id_usuario, tarea.id_tarea, True)
        self.assertTrue(ok)

        tareas = self.manager.listar_tareas(self.id_usuario)
        self.assertTrue(bool(tareas[0].completada))

    # Repositorio sin inyectar
    def test_repo_sin_inyeccion_usa_sessionlocal(self) -> None:
        
        init_db()
        repo = RepositorioTareasSQLite()
        self.assertIs(repo._session_factory, SessionLocal)  # noqa: SLF001

