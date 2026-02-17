from src.logica.editar_tarea_logica import EditarTareaLogica
from src.modelo.conexion import SessionLocal
from src.modelo.bd_model import Usuario, Tarea


# =====================================================
# PREPARACIÓN DE DATOS
# =====================================================
def setup_module():
    """
    Crea usuario y tarea de prueba.
    """
    session = SessionLocal()

    # Crear usuario de prueba (SIN login)
    usuario = session.query(Usuario).filter_by(username="editor").first()

    if not usuario:
        usuario = Usuario(
            username="editor",
            password_hash="hash_prueba"
        )
        session.add(usuario)
        session.commit()

    # Crear tarea de prueba
    tarea = session.query(Tarea).filter_by(titulo="Tarea original").first()

    if not tarea:
        tarea = Tarea(
            id_usuario=usuario.id_usuario,
            titulo="Tarea original",
            descripcion="Descripcion original",
        )
        session.add(tarea)
        session.commit()

    session.close()


# =====================================================
# CASOS FELICES
# =====================================================

def test_editar_tarea_titulo():
    logica = EditarTareaLogica()
    session = SessionLocal()

    tarea = session.query(Tarea).filter_by(titulo="Tarea original").first()

    resultado = logica.editar_tarea(
        tarea.id_tarea,
        "Tarea editada",
        "Descripcion nueva",
    )

    assert resultado is True
    session.close()


def test_editar_tarea_solo_descripcion():
    logica = EditarTareaLogica()
    session = SessionLocal()

    tarea = session.query(Tarea).filter_by(titulo="Tarea editada").first()

    resultado = logica.editar_tarea(
        tarea.id_tarea,
        "Tarea editada",
        "Solo cambio descripcion",
    )

    assert resultado is True
    session.close()


def test_editar_tarea_final():
    logica = EditarTareaLogica()
    session = SessionLocal()

    tarea = session.query(Tarea).filter_by(titulo="Tarea editada").first()

    resultado = logica.editar_tarea(
        tarea.id_tarea,
        "Tarea final",
        "Descripcion final",
    )

    assert resultado is True
    session.close()


# =====================================================
# CASOS TRISTES
# =====================================================

def test_editar_tarea_no_existente():
    logica = EditarTareaLogica()
    assert logica.editar_tarea(99999, "Nuevo titulo") is False


def test_editar_tarea_titulo_vacio():
    logica = EditarTareaLogica()
    assert logica.editar_tarea(1, "") is False


def test_editar_tarea_titulo_espacios():
    logica = EditarTareaLogica()
    assert logica.editar_tarea(1, "   ") is False