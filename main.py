from __future__ import annotations

from pathlib import Path
import sqlite3

from src.modelo.conexion import crear_db_sqlite, init_db


def cargar_bd_sql(db_path: Path, sql_path: Path) -> None:
    """
    Ejecuta BD.sql en DB.sqlite usando sqlite3.

    Args:
        db_path: Ruta de DB.sqlite.
        sql_path: Ruta de BD.sql.
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


def mostrar_resumen(db_path: Path) -> None:
    """Imprime un resumen simple de tablas y cantidad de filas."""
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [row[0] for row in cur.fetchall()]

        print("\n📌 Tablas detectadas:")
        for tabla in tablas:
            print(f" - {tabla}")

        print("\n📊 Filas por tabla:")
        for tabla in tablas:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {tabla};")
                total = cur.fetchone()[0]
                print(f"✅ {tabla}: {total} filas")
            except sqlite3.Error:
                continue


def main() -> None:
    """
    Flujo:
    1) Crear/verificar DB.sqlite
    2) Crear/verificar tablas ORM (usuarios, tareas)
    3) Cargar datos de BD.sql
    4) Mostrar resumen
    """
    db_path = Path("DB.sqlite")
    sql_path = Path("BD.sql")

    crear_db_sqlite()
    print("✅ Archivo DB.sqlite creado/verificado.")

    init_db()
    print("✅ Tablas creadas/verificadas (SQLAlchemy).")

    cargar_bd_sql(db_path=db_path, sql_path=sql_path)
    print("✅ BD.sql ejecutado correctamente.")

    mostrar_resumen(db_path=db_path)


if __name__ == "__main__":
    main()
