"""crear_maestros_vraem_frontera_region

Revision ID: ef254d67a353
Revises: f6bdadb538c8
Create Date: 2026-05-16 14:37:29.994755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef254d67a353'
down_revision: Union[str, Sequence[str], None] = 'f6bdadb538c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'vraem',
        sa.Column('codigo', sa.String(1), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    op.create_table(
        'zona_frontera',
        sa.Column('codigo', sa.String(1), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    op.create_table(
        'region_natural',
        sa.Column('codigo', sa.String(1), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )

    op.execute(
        sa.text(
            "INSERT INTO vraem (codigo, descripcion) VALUES "
            "('0', 'No VRAEM'), ('1', 'Sí VRAEM - Directa'), ('2', 'Sí VRAEM - influencia')"
        )
    )
    op.execute(
        sa.text(
            "INSERT INTO zona_frontera (codigo, descripcion) VALUES "
            "('0', 'No'), ('1', 'Sí')"
        )
    )
    # La región natural según los datos podría no ser numérica; aquí usamos '1','2','3' si aparece así en los datos.
    # Si los datos usan texto como 'Costa', 'Sierra', 'Selva', debemos ajustarlo.
    # Por ahora asumamos códigos cortos, pero tú lo confirmarás.
    op.execute(
        sa.text(
            "INSERT INTO region_natural (codigo, descripcion) VALUES "
            "('1', 'Costa'), ('2', 'Sierra'), ('3', 'Selva')"
        )
    )


def downgrade():
    op.drop_table('region_natural')
    op.drop_table('zona_frontera')
    op.drop_table('vraem')
