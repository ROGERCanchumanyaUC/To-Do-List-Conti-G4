# src/modelo/bd_model.py
from __future__ import annotations

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.modelo.conexion import Base


class Usuario(Base):
    """Tabla usuarios (HU01: login básico)."""

    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    activo: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("1"),
    )
    creado_en: Mapped[object] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    tareas: Mapped[list["Tarea"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    __table_args__ = (
        CheckConstraint("activo IN (0, 1)", name="ck_usuarios_activo_bool"),
    )

    def __repr__(self) -> str:
        return f"Usuario(id_usuario={self.id_usuario}, username={self.username!r})"


class Tarea(Base):
    """Tabla tareas (HU02–HU06: CRUD + marcar completada)."""

    __tablename__ = "tareas"

    id_tarea: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    id_usuario: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "usuarios.id_usuario",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    titulo: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # En SQLite se maneja como 0/1 (Integer).
    completada: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0"),
    )

    creada_en: Mapped[object] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    actualizada_en: Mapped[object] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=func.current_timestamp(),
    )

    usuario: Mapped["Usuario"] = relationship(back_populates="tareas")

    __table_args__ = (
        # Validaciones desde BD
        CheckConstraint(
            "length(trim(titulo)) > 0",
            name="ck_tareas_titulo_no_vacio",
        ),
        CheckConstraint(
            "completada IN (0, 1)",
            name="ck_tareas_completada_bool",
        ),
        # Recomendado: evita duplicados de título por usuario (apoya HU02)
        UniqueConstraint(
            "id_usuario",
            "titulo",
            name="uq_tareas_usuario_titulo",
        ),
        # Índices para listar rápido (HU03)
        Index("ix_tareas_usuario_completada", "id_usuario", "completada"),
        Index("ix_tareas_usuario_creada", "id_usuario", "creada_en"),
    )

    def __repr__(self) -> str:
        return (
            "Tarea("
            f"id_tarea={self.id_tarea}, "
            f"id_usuario={self.id_usuario}, "
            f"titulo={self.titulo!r}, "
            f"completada={self.completada}"
            ")"
        )
