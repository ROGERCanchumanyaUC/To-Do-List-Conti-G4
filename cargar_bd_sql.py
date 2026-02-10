from __future__ import annotations

from pathlib import Path
import sqlite3


def cargar_script_sql(db_path: Path, sql_path: Path) -> None:
    """
    Ejecuta un script SQL (.sql) sobre una base de datos SQLite.

    Args:
        db_path: Ruta del archivo DB.sqlite.
        sql_path: Ruta del archivo BD.sql.

    Raises:
        FileNotFoundError: Si no existe DB.sqlite o BD.sql.
        sqlite3.Error: Si el script SQL tiene errores.
    """
    if not db_path.exists():
        raise FileNotFoundError(
            f"No existe {db_path.name} en la raíz del proyecto: {db_path.resolve()}"
        )

    if not sql_path.exists():
        raise FileNotFoundError(
            f"No existe {sql_path.name} en la raíz del proyecto: {sql_path.resolve()}"
        )

    script_sql = sql_path.read_text(encoding="utf-8")

    with sqlite3.connect(db_path) as con:
        con.executescript(script_sql)
        con.commit()


def main() -> None:
    """Punto de entrada para cargar BD.sql en DB.sqlite."""
    db_path = Path("DB.sqlite")
    sql_path = Path("BD.sql")

    cargar_script_sql(db_path=db_path, sql_path=sql_path)
    print("✅ BD.sql ejecutado correctamente en DB.sqlite")


if __name__ == "__main__":
    main()