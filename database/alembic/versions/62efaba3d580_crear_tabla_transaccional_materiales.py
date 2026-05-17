"""crear_tabla_transaccional_materiales

Revision ID: 62efaba3d580
Revises: ff3467c8c74c
Create Date: 2026-05-16 18:28:33.749664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62efaba3d580'
down_revision: Union[str, Sequence[str], None] = 'ff3467c8c74c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'materiales',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),

        # Identificadores de la Institución Educativa (Sin FK por ahora, pero fuertemente indexados)
        sa.Column('cod_mod', sa.String(length=7), nullable=False, index=True),
        sa.Column('anexo', sa.String(length=1), nullable=False, server_default='0'),

        # Llaves Foráneas a tablas maestras simples
        sa.Column('nivel_modalidad_codigo', sa.String(length=2), nullable=True),
        sa.Column('gestion_codigo', sa.String(length=1), nullable=True),
        sa.Column('dependencia_codigo', sa.String(length=2), nullable=True),
        sa.Column('area_censo_codigo', sa.String(length=1), nullable=True),
        sa.Column('cedula_codigo', sa.String(length=3), nullable=True),

        # Componentes de la llave foránea compuesta
        sa.Column('cuadro_codigo', sa.String(length=10), nullable=False),
        sa.Column('tipdato', sa.String(length=20), nullable=False),

        # El valor de la respuesta (Usamos String para evitar fallos de casteo si viene vacío o texto desde el parquet)
        sa.Column('recibio', sa.String(length=1), nullable=True),

        # Definición explícita de Constraints (Llaves Foráneas)
        sa.ForeignKeyConstraint(
            ['nivel_modalidad_codigo'], ['nivel_modalidad.codigo'],
            name='fk_materiales_niv_mod'
        ),
        sa.ForeignKeyConstraint(
            ['gestion_codigo'], ['gestion.codigo'],
            name='fk_materiales_gestion'
        ),
        sa.ForeignKeyConstraint(
            ['dependencia_codigo'], ['dependencia.codigo'],
            name='fk_materiales_dependencia'
        ),
        sa.ForeignKeyConstraint(
            ['area_censo_codigo'], ['area_censo.codigo'],
            name='fk_materiales_area_censo'
        ),
        sa.ForeignKeyConstraint(
            ['cedula_codigo'], ['cedula.codigo'],
            name='fk_materiales_cedula'
        ),

        # La llave foránea compuesta clave, respetando el orden del schema
        sa.ForeignKeyConstraint(
            ['tipdato', 'cuadro_codigo'],
            ['cuadro_tipdato.tipdato', 'cuadro_tipdato.cuadro_codigo'],
            name='fk_materiales_cuadro_tipdato'
        )
    )


def downgrade():
    op.drop_table('materiales')
