"""agregar_anio_a_tablas_transaccionales

Revision ID: 88583c88b508
Revises: 4c05aec392ee
Create Date: 2026-05-16 19:19:16.681589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88583c88b508'
down_revision: Union[str, Sequence[str], None] = '4c05aec392ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Eliminar la restricción única estática del Padrón
    op.drop_constraint('uq_padron_cod_mod_anexo', 'padron_ie', type_='unique')

    # 2. Agregar la columna 'anio' a todas las tablas transaccionales
    tablas = ['padron_ie', 'materiales', 'equipamiento', 'recursos_acce', 'fgestion']

    for tabla in tablas:
        op.add_column(tabla, sa.Column('anio', sa.String(length=4), nullable=False, server_default='2023'))

    # 3. Crear la nueva restricción multianual en el Padrón
    op.create_unique_constraint('uq_padron_cod_mod_anexo_anio', 'padron_ie', ['cod_mod', 'anexo', 'anio'])

    # 4. Índice para el año, vital para consultas de Machine Learning
    op.create_index('ix_padron_anio', 'padron_ie', ['anio'])


def downgrade():
    op.drop_index('ix_padron_anio', table_name='padron_ie')
    op.drop_constraint('uq_padron_cod_mod_anexo_anio', 'padron_ie', type_='unique')

    tablas = ['padron_ie', 'materiales', 'equipamiento', 'recursos_acce', 'fgestion']
    for tabla in tablas:
        op.drop_column(tabla, 'anio')

    op.create_unique_constraint('uq_padron_cod_mod_anexo', 'padron_ie', ['cod_mod', 'anexo'])
