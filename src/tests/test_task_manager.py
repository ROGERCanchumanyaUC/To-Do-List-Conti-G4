import pytest
from src.logica.task_manager import TaskManager
from src.modelo.modelo import Base, engine


@pytest.fixture(scope="function")
def task_manager():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return TaskManager()


def test_crear_tarea(task_manager):
    tarea = task_manager.crear_tarea("Estudiar Python")
    assert tarea.descripcion == "Estudiar Python"
    assert tarea.completada is False


def test_listar_tareas(task_manager):
    task_manager.crear_tarea("Tarea 1")
    tareas = task_manager.listar_tareas()
    assert len(tareas) == 1


def test_editar_tarea(task_manager):
    tarea = task_manager.crear_tarea("Vieja")
    tarea_editada = task_manager.editar_tarea(tarea.id, "Nueva")
    assert tarea_editada.descripcion == "Nueva"


def test_eliminar_tarea(task_manager):
    tarea = task_manager.crear_tarea("Eliminar")
    task_manager.eliminar_tarea(tarea.id)
    assert task_manager.listar_tareas() == []


def test_marcar_completada(task_manager):
    tarea = task_manager.crear_tarea("Completar")
    tarea = task_manager.marcar_completada(tarea.id)
    assert tarea.completada is True
