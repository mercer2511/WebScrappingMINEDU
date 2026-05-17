"""crear_tabla_sec100_matrices

Revision ID: 680135b4bad2
Revises: c473b5cf7bbb
Create Date: 2026-05-16 18:53:33.952455

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '680135b4bad2'
down_revision: Union[str, Sequence[str], None] = 'c473b5cf7bbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'sec100_matrices',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),

        # Identificadores de IE
        sa.Column('cod_mod', sa.String(length=7), nullable=False, index=True),
        sa.Column('anexo', sa.String(length=1), nullable=False, server_default='0'),
        sa.Column('codugel', sa.String(length=6), nullable=True),

        # Llaves foráneas maestras
        sa.Column('nivel_modalidad_codigo', sa.String(length=2), nullable=True),
        sa.Column('cedula_codigo', sa.String(length=3), nullable=True),

        # Detalle de la matriz
        sa.Column('pregunta', sa.String(length=20), nullable=True),
        sa.Column('numero', sa.String(length=10), nullable=True),
        sa.Column('descrip', sa.Text(), nullable=True),

        # Respuestas (Todo en String para evitar problemas de casteo de nulos/vacíos en la ingesta)
        sa.Column('chk1', sa.String(length=2), nullable=True),
        sa.Column('chk2', sa.String(length=2), nullable=True),
        sa.Column('d01', sa.String(length=10), nullable=True),
        sa.Column('d02', sa.String(length=10), nullable=True),
        sa.Column('d03', sa.String(length=10), nullable=True),
        sa.Column('frecuencia', sa.String(length=50), nullable=True),
        sa.Column('fecha', sa.String(length=20), nullable=True),
        sa.Column('anio', sa.String(length=4), nullable=True),

        # Constraints
        sa.ForeignKeyConstraint(
            ['nivel_modalidad_codigo'], ['nivel_modalidad.codigo'],
            name='fk_sec100_niv_mod'
        ),
        sa.ForeignKeyConstraint(
            ['cedula_codigo'], ['cedula.codigo'],
            name='fk_sec100_cedula'
        )
    )


def downgrade():
    op.drop_table('sec100_matrices')