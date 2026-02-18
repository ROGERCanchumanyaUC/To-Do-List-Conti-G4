import hashlib

from src.modelo.conexion import SessionLocal
from src.modelo.bd_model import Usuario


class LoginLogica:
    """Lógica de autenticación (HU001 Login)."""

    @staticmethod
    def generar_hash(password: str) -> str:
        """
        Genera hash SHA256 de la contraseña.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username: str, password: str) -> bool:
        """
        Valida usuario y contraseña contra la base de datos.
        """

        session = SessionLocal()

        try:
            usuario = (
                session.query(Usuario)
                .filter_by(username=username)
                .first()
            )

            if usuario is None:
                return False

            password_hash = self.generar_hash(password)

            return usuario.password_hash == password_hash

        finally:
            session.close()
