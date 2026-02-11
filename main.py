from __future__ import annotations

from pathlib import Path
import sqlite3

from src.modelo.conexion import DB_PATH, crear_db_sqlite, init_db


def cargar_bd_sql(db_path: Path, sql_path: Path) -> None:
    """
    Ejecuta BD.sql en DB.sqlite usando sqlite3.
    Si el archivo no existe, NO revienta (solo avisa).
    """
    if not sql_path.exists():
        print(f"ℹ️ No existe {sql_path.name}. Se omite carga de datos.")
        return

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
    print("🚀 Iniciando OOPRA (main.py) ...")

    # ✅ usa la misma ruta canónica del proyecto (conexion.py)
    db_path = DB_PATH
    sql_path = Path("BD.sql")

    crear_db_sqlite()
    print(f"✅ DB creada/verificada en: {db_path.resolve()}")

    init_db()
    print("✅ Tablas ORM creadas/verificadas (usuarios, tareas)")

    cargar_bd_sql(db_path=db_path, sql_path=sql_path)

    mostrar_resumen(db_path=db_path)

    print("\n✅ Proceso finalizado.")


if __name__ == "__main__":
    main()
