from src.logica.login_logica import LoginLogica
from src.modelo.conexion import SessionLocal
from src.modelo.bd_model import Usuario


# =====================================================
# PREPARACIÓN DE DATOS (se ejecuta antes de los tests)
# =====================================================
def setup_module():
    """
    Crea usuarios de prueba para los casos felices.
    """
    session = SessionLocal()
    login = LoginLogica()

    usuarios_prueba = [
        ("admin", "1234"),
        ("user1", "abcd"),
        ("tester", "pass123"),
    ]

    for username, password in usuarios_prueba:
        existe = session.query(Usuario).filter_by(username=username).first()

        if not existe:
            nuevo_usuario = Usuario(
                username=username,
                password_hash=login.generar_hash(password),
            )
            session.add(nuevo_usuario)

    session.commit()
    session.close()


# =====================================================
# CASOS FELICES (LOGIN CORRECTO)
# =====================================================

def test_login_correcto_admin():
    login = LoginLogica()
    assert login.login("admin", "1234") is True


def test_login_correcto_user1():
    login = LoginLogica()
    assert login.login("user1", "abcd") is True


def test_login_correcto_tester():
    login = LoginLogica()
    assert login.login("tester", "pass123") is True


# =====================================================
# CASOS TRISTES (LOGIN INCORRECTO)
# =====================================================

def test_login_password_incorrecta():
    login = LoginLogica()
    assert login.login("admin", "wrong") is False


def test_login_usuario_no_existe():
    login = LoginLogica()
    assert login.login("noexiste", "1234") is False


def test_login_usuario_vacio():
    login = LoginLogica()
    assert login.login("", "1234") is False
