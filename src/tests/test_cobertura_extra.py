# src/tests/test_cobertura_extra.py
from __future__ import annotations

import runpy
import unittest
from unittest.mock import MagicMock, patch

from src.modelo import conexion as conexion_module
from src.modelo.bd_model import Tarea, Usuario
from src.modelo.conexion import Base, SessionLocal, init_db
from src.modelo.repositorio_tareas import RepositorioTareasSQLite


class TestCoberturaExtra(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Asegura tablas en la BD real (DB.sqlite)
        init_db()

        # Usuario fijo para pruebas de repo (evita depender de otros tests)
        cls.username = "cobertura_user"
        cls.password_hash = "hash_cobertura"

        with SessionLocal.begin() as session:
            # Deja el estado consistente (no toca otros usuarios)
            session.query(Usuario).filter(Usuario.username == cls.username).delete()

            usuario = Usuario(username=cls.username, password_hash=cls.password_hash)
            session.add(usuario)
            session.flush()
            cls.id_usuario = usuario.id_usuario

        cls.repo = RepositorioTareasSQLite(session_factory=SessionLocal)

    def setUp(self) -> None:
        # Limpia SOLO tareas del usuario de cobertura
        with SessionLocal.begin() as session:
            session.query(Tarea).filter(Tarea.id_usuario == self.id_usuario).delete()

    # -------------------------
    # conexion.py
    # -------------------------
    def test_crear_db_sqlite_devuelve_path_existente(self) -> None:
        path = conexion_module.crear_db_sqlite()
        self.assertTrue(path.exists())

    def test_create_engine_privado_crea_engine(self) -> None:
        engine = conexion_module._create_engine(echo=False)  # noqa: SLF001
        self.assertIsNotNone(engine)
        engine.dispose()

    def test_pragmas_aplicados_en_conexion(self) -> None:
        # Verifica que PRAGMA foreign_keys y journal_mode se aplican
        with conexion_module.ENGINE.connect() as con:
            fk = con.exec_driver_sql("PRAGMA foreign_keys;").scalar_one()
            jm = con.exec_driver_sql("PRAGMA journal_mode;").scalar_one()

        self.assertEqual(1, int(fk))
        # En conexion.py dejaste DELETE para evitar -wal/-shm
        self.assertEqual("delete", str(jm).lower())

    def test_get_session_cierra_sesion(self) -> None:
        fake_session = MagicMock()

        # Parcheamos SessionLocal para controlar close()
        with patch("src.modelo.conexion.SessionLocal", return_value=fake_session):
            with conexion_module.get_session() as session:
                self.assertIs(session, fake_session)

        fake_session.close.assert_called_once()

    def test_conexion_run_as_main(self) -> None:
        # Ejecuta el módulo como script para cubrir el bloque __main__
        # Puede aparecer un RuntimeWarning de runpy (no es fallo).
        runpy.run_module("src.modelo.conexion", run_name="__main__")

    # -------------------------
    # bd_model.py
    # -------------------------
    def test_repr_usuario_y_tarea(self) -> None:
        u = Usuario(id_usuario=1, username="demo", password_hash="x")  # type: ignore[arg-type]
        t = Tarea(  # type: ignore[call-arg]
            id_tarea=10,
            id_usuario=1,
            titulo="T",
            descripcion=None,
            completada=False,
        )
        self.assertIn("Usuario(", repr(u))
        self.assertIn("Tarea(", repr(t))

    def test_constraints_creados_en_metadata(self) -> None:
        # Asegura que el metadata tiene tablas y algunos índices
        self.assertIn("usuarios", Base.metadata.tables)
        self.assertIn("tareas", Base.metadata.tables)

        tareas_table = Base.metadata.tables["tareas"]
        self.assertGreaterEqual(len(tareas_table.indexes), 1)

    # -------------------------
    # repositorio_tareas.py
    # -------------------------
    def test_repo_crear_tarea_titulo_vacio(self) -> None:
        tarea, msg = self.repo.crear_tarea(self.id_usuario, "   ", "x")
        self.assertIsNone(tarea)
        self.assertIn("título", msg.lower())

    def test_repo_crear_tarea_usuario_no_existe(self) -> None:
        tarea, msg = self.repo.crear_tarea(999999, "Algo", "x")
        self.assertIsNone(tarea)
        self.assertIn("usuario no existe", msg.lower())

    def test_repo_obtener_tarea_none(self) -> None:
        tarea = self.repo.obtener_tarea(self.id_usuario, 999999)
        self.assertIsNone(tarea)

    def test_repo_editar_no_existe(self) -> None:
        res = self.repo.editar_tarea(self.id_usuario, 999999, "Nuevo", "x")
        self.assertFalse(res.ok)

    def test_repo_eliminar_no_existe(self) -> None:
        res = self.repo.eliminar_tarea(self.id_usuario, 999999)
        self.assertFalse(res.ok)

    def test_repo_marcar_no_existe(self) -> None:
        res = self.repo.marcar_completada(self.id_usuario, 999999, True)
        self.assertFalse(res.ok)

    def test_repo_editar_titulo_vacio(self) -> None:
        res = self.repo.editar_tarea(self.id_usuario, 1, "   ", "x")
        self.assertFalse(res.ok)
        self.assertIn("título", res.mensaje.lower())

    def test_repo_editar_duplicado_dispara_integrity(self) -> None:
        # Crea dos tareas diferentes
        t1, _ = self.repo.crear_tarea(self.id_usuario, "A", "")
        t2, _ = self.repo.crear_tarea(self.id_usuario, "B", "")
        self.assertIsNotNone(t1)
        self.assertIsNotNone(t2)

        # Fuerza duplicate (B -> A). Debe devolver mensaje elegante
        # (internamente cae en IntegrityError)
        res = self.repo.editar_tarea(
            self.id_usuario,
            t2.id_tarea,  # type: ignore[union-attr]
            "A",
            "",
        )
        self.assertFalse(res.ok)

    def test_repo_init_sin_sessionlocal_lanza_error(self) -> None:
        # Cubre el branch de error cuando SessionLocal no existe
        with patch("src.modelo.repositorio_tareas.SessionLocal", None):
            with self.assertRaises(RuntimeError):
                RepositorioTareasSQLite(session_factory=None)

    def test_repo_sin_inyeccion_usa_sessionlocal(self) -> None:
        # Cubre la línea: asigna SessionLocal por defecto
        init_db()
        repo = RepositorioTareasSQLite()
        self.assertIs(repo._session_factory, SessionLocal)  # noqa: SLF001

    @classmethod
    def tearDownClass(cls) -> None:
        # Libera conexiones del pool (reduce warnings en Windows)
        conexion_module.ENGINE.dispose()
