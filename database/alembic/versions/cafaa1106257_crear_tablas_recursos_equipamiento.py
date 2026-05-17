"""crear_tablas_recursos_equipamiento

Revision ID: cafaa1106257
Revises: 62efaba3d580
Create Date: 2026-05-16 18:33:03.990046

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cafaa1106257'
down_revision: Union[str, Sequence[str], None] = '62efaba3d580'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================================================
    # TABLA: RECURSOS DE ACCESIBILIDAD (14_Recursos_acce)
    # =========================================================
    op.create_table(
        'recursos_acce',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cod_mod', sa.String(length=7), nullable=False, index=True),
        sa.Column('anexo', sa.String(length=1), nullable=False, server_default='0'),

        sa.Column('nivel_modalidad_codigo', sa.String(length=2), nullable=True),
        sa.Column('gestion_codigo', sa.String(length=1), nullable=True),
        sa.Column('dependencia_codigo', sa.String(length=2), nullable=True),
        sa.Column('area_censo_codigo', sa.String(length=1), nullable=True),
        sa.Column('cedula_codigo', sa.String(length=3), nullable=True),

        sa.Column('cuadro_codigo', sa.String(length=10), nullable=False),
        sa.Column('tipdato', sa.String(length=20), nullable=False),

        # Respuesta (1, 2, 3, 4) - Usamos String para seguridad en la ingesta
        sa.Column('chk', sa.String(length=1), nullable=True),

        sa.ForeignKeyConstraint(['nivel_modalidad_codigo'], ['nivel_modalidad.codigo'], name='fk_recursos_niv_mod'),
        sa.ForeignKeyConstraint(['gestion_codigo'], ['gestion.codigo'], name='fk_recursos_gestion'),
        sa.ForeignKeyConstraint(['dependencia_codigo'], ['dependencia.codigo'], name='fk_recursos_dependencia'),
        sa.ForeignKeyConstraint(['area_censo_codigo'], ['area_censo.codigo'], name='fk_recursos_area_censo'),
        sa.ForeignKeyConstraint(['cedula_codigo'], ['cedula.codigo'], name='fk_recursos_cedula'),
        sa.ForeignKeyConstraint(
            ['tipdato', 'cuadro_codigo'],
            ['cuadro_tipdato.tipdato', 'cuadro_tipdato.cuadro_codigo'],
            name='fk_recursos_cuadro_tipdato'
        )
    )

    # =========================================================
    # TABLA: EQUIPAMIENTO (15_Equipamiento)
    # =========================================================
    op.create_table(
        'equipamiento',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cod_mod', sa.String(length=7), nullable=False, index=True),
        sa.Column('anexo', sa.String(length=1), nullable=False, server_default='0'),

        sa.Column('nivel_modalidad_codigo', sa.String(length=2), nullable=True),
        sa.Column('gestion_codigo', sa.String(length=1), nullable=True),
        sa.Column('dependencia_codigo', sa.String(length=2), nullable=True),
        sa.Column('area_censo_codigo', sa.String(length=1), nullable=True),
        sa.Column('cedula_codigo', sa.String(length=3), nullable=True),

        sa.Column('cuadro_codigo', sa.String(length=10), nullable=False),
        sa.Column('tipdato', sa.String(length=20), nullable=False),

        # Respuestas (1, 2, nulo)
        sa.Column('chk1', sa.String(length=1), nullable=True),
        sa.Column('chk2', sa.String(length=1), nullable=True),

        sa.ForeignKeyConstraint(['nivel_modalidad_codigo'], ['nivel_modalidad.codigo'], name='fk_equipamiento_niv_mod'),
        sa.ForeignKeyConstraint(['gestion_codigo'], ['gestion.codigo'], name='fk_equipamiento_gestion'),
        sa.ForeignKeyConstraint(['dependencia_codigo'], ['dependencia.codigo'], name='fk_equipamiento_dependencia'),
        sa.ForeignKeyConstraint(['area_censo_codigo'], ['area_censo.codigo'], name='fk_equipamiento_area_censo'),
        sa.ForeignKeyConstraint(['cedula_codigo'], ['cedula.codigo'], name='fk_equipamiento_cedula'),
        sa.ForeignKeyConstraint(
            ['tipdato', 'cuadro_codigo'],
            ['cuadro_tipdato.tipdato', 'cuadro_tipdato.cuadro_codigo'],
            name='fk_equipamiento_cuadro_tipdato'
        )
    )


def downgrade():
    op.drop_table('equipamiento')
    op.drop_table('recursos_acce')
