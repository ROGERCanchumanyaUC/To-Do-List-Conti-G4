# src/tests/test_cobertura_extra.py
from __future__ import annotations

import runpy
import unittest



from src.modelo import conexion as conexion_module
from src.modelo.bd_model import Tarea, Usuario
from src.modelo.conexion import SessionLocal, crear_db_sqlite, get_session, init_db
from src.modelo.repositorio_tareas import RepositorioTareasSQLite


class TestCoberturaExtra(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        init_db()
        cls.repo = RepositorioTareasSQLite(session_factory=SessionLocal)

        cls.username = "demo_cov"
        cls.password_hash = "hash_cov"

        with SessionLocal.begin() as session:
            # asegura usuario de cobertura
            session.query(Usuario).filter(Usuario.username == cls.username).delete()
            usuario = Usuario(username=cls.username, password_hash=cls.password_hash)
            session.add(usuario)
            session.flush()
            cls.id_usuario = usuario.id_usuario

    def setUp(self) -> None:
        with SessionLocal.begin() as session:
            session.query(Tarea).filter(Tarea.id_usuario == self.id_usuario).delete()

    # -------------------------
    # bd_model.py -> cubrir __repr__
    # -------------------------
    def test_repr_usuario_y_tarea(self) -> None:
        with SessionLocal.begin() as session:
            usuario = session.get(Usuario, self.id_usuario)
            self.assertIsNotNone(usuario)
            _ = repr(usuario)

            tarea = Tarea(id_usuario=self.id_usuario, titulo="X", descripcion=None)
            session.add(tarea)
            session.flush()
            _ = repr(tarea)

    # -------------------------
    # conexion.py -> cubrir crear_db_sqlite, get_session y __main__
    # -------------------------
    def test_crear_db_sqlite(self) -> None:
        path = crear_db_sqlite()
        self.assertTrue(path.exists())

    def test_get_session_cierra_sesion(self) -> None:
        gen = get_session()
        session = next(gen)
        self.assertIsNotNone(session)
        gen.close()  # ejecuta finally -> session.close()

    def test_create_engine_privado(self) -> None:
        # Cubre _create_engine y el listener de PRAGMAs
        engine = conexion_module._create_engine(echo=False)  # noqa: SLF001
        engine.dispose()

    def test_conexion_run_as_main(self) -> None:
        # Cubre if __name__ == "__main__"
        mod = runpy.run_module("src.modelo.conexion", run_name="__main__")
        engine = mod.get("ENGINE")
        if engine is not None:
            engine.dispose()

    # -------------------------
    # repositorio_tareas.py -> cubrir ramas faltantes
    # -------------------------
    def test_repo_crear_tarea_titulo_vacio(self) -> None:
        tarea, msg = self.repo.crear_tarea(self.id_usuario, "   ", "")
        self.assertIsNone(tarea)
        self.assertIn("título", msg.lower())

    def test_repo_crear_tarea_usuario_no_existe(self) -> None:
        tarea, msg = self.repo.crear_tarea(999999, "Hola", "")
        self.assertIsNone(tarea)
        self.assertIn("usuario", msg.lower())

    def test_repo_obtener_tarea_none(self) -> None:
        tarea = self.repo.obtener_tarea(self.id_usuario, 999999)
        self.assertIsNone(tarea)

    def test_repo_editar_titulo_vacio(self) -> None:
        r = self.repo.editar_tarea(self.id_usuario, 1, "   ", "")
        self.assertFalse(r.ok)

    def test_repo_editar_no_existe(self) -> None:
        r = self.repo.editar_tarea(self.id_usuario, 999999, "A", "")
        self.assertFalse(r.ok)

    def test_repo_editar_duplicado_dispara_integrity(self) -> None:
        t1, _ = self.repo.crear_tarea(self.id_usuario, "T1", "")
        self.assertIsNotNone(t1)
        t2, _ = self.repo.crear_tarea(self.id_usuario, "T2", "")
        self.assertIsNotNone(t2)

        # intentar renombrar T2 a T1 -> UniqueConstraint
        r = self.repo.editar_tarea(self.id_usuario, t2.id_tarea, "T1", "")
        self.assertFalse(r.ok)

    def test_repo_eliminar_no_existe(self) -> None:
        r = self.repo.eliminar_tarea(self.id_usuario, 999999)
        self.assertFalse(r.ok)

    def test_repo_marcar_no_existe(self) -> None:
        r = self.repo.marcar_completada(self.id_usuario, 999999, True)
        self.assertFalse(r.ok)

    def test_repo_init_sin_sessionlocal_lanza_error(self) -> None:
        # Cubre la rama RuntimeError si SessionLocal no existe
        import src.modelo.repositorio_tareas as repo_mod

        original = repo_mod.SessionLocal
        repo_mod.SessionLocal = None
        try:
            with self.assertRaises(RuntimeError):
                RepositorioTareasSQLite()
        finally:
            repo_mod.SessionLocal = original
