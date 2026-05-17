"""crear_tabla_matricula

Revision ID: 9d4717fdc4f6
Revises: c2541308bd27
Create Date: 2026-05-17 01:43:14.697348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d4717fdc4f6'
down_revision: Union[str, Sequence[str], None] = 'c2541308bd27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Crear la tabla de hechos: Matricula
    op.create_table(
        'matricula',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cod_mod', sa.String(length=7), nullable=False),
        sa.Column('anexo', sa.String(length=1), nullable=False),
        sa.Column('anio', sa.String(length=4), nullable=False),
        sa.Column('nroced', sa.String(length=10), nullable=True),
        sa.Column('cuadro', sa.String(length=10), nullable=True),
        sa.Column('tipdato', sa.String(length=20), nullable=True),
        sa.Column('modalidad', sa.String(length=50), nullable=True),

        # Generar dinámicamente las columnas d01 hasta d30
        *[sa.Column(f'd{str(i).zfill(2)}', sa.Integer(), nullable=True) for i in range(1, 31)]
    )

    # Candado principal: Conexión estricta con el Padrón (Llave compuesta multianual)
    op.create_foreign_key(
        'fk_matricula_padron', 'matricula', 'padron_ie',
        ['cod_mod', 'anexo', 'anio'], ['cod_mod', 'anexo', 'anio']
    )

    # Índices para que los cruces del modelo de Machine Learning sean veloces
    op.create_index('ix_matricula_padron_keys', 'matricula', ['cod_mod', 'anexo', 'anio'])
    op.create_index('ix_matricula_cuadro_tipdato', 'matricula', ['cuadro', 'tipdato'])


def downgrade():
    op.drop_index('ix_matricula_cuadro_tipdato', table_name='matricula')
    op.drop_index('ix_matricula_padron_keys', table_name='matricula')
    op.drop_constraint('fk_matricula_padron', 'matricula', type_='foreignkey')
    op.drop_table('matricula')
