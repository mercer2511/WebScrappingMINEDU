"""crear_tabla_docente

Revision ID: 7fc3f3740ae4
Revises: 9d4717fdc4f6
Create Date: 2026-05-17 10:04:12.528130

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fc3f3740ae4'
down_revision: Union[str, Sequence[str], None] = '9d4717fdc4f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Crear la tabla de hechos: Docente
    op.create_table(
        'docente',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cod_mod', sa.String(length=7), nullable=False),
        sa.Column('anexo', sa.String(length=1), nullable=False),
        sa.Column('anio', sa.String(length=4), nullable=False),
        sa.Column('nroced', sa.String(length=10), nullable=True),
        sa.Column('cuadro', sa.String(length=10), nullable=True),
        sa.Column('tipdato', sa.String(length=20), nullable=True),

        # Generar dinámicamente las columnas d01 hasta d32
        *[sa.Column(f'd{str(i).zfill(2)}', sa.Integer(), nullable=True) for i in range(1, 33)]
    )

    # Candado principal: Conexión estricta con el Padrón (Llave compuesta multianual)
    op.create_foreign_key(
        'fk_docente_padron', 'docente', 'padron_ie',
        ['cod_mod', 'anexo', 'anio'], ['cod_mod', 'anexo', 'anio']
    )

    # Índices para consultas analíticas veloces
    op.create_index('ix_docente_padron_keys', 'docente', ['cod_mod', 'anexo', 'anio'])
    op.create_index('ix_docente_cuadro_tipdato', 'docente', ['cuadro', 'tipdato'])


def downgrade():
    op.drop_index('ix_docente_cuadro_tipdato', table_name='docente')
    op.drop_index('ix_docente_padron_keys', table_name='docente')
    op.drop_constraint('fk_docente_padron', 'docente', type_='foreignkey')
    op.drop_table('docente')