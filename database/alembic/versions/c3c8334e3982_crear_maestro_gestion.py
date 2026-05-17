"""crear_maestro_gestion

Revision ID: c3c8334e3982
Revises: 0f0360c65845
Create Date: 2026-05-16 14:35:04.768051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3c8334e3982'
down_revision: Union[str, Sequence[str], None] = '0f0360c65845'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'gestion',
        sa.Column('codigo', sa.String(1), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        ('1', 'Pública de Gestión Directa'),
        ('2', 'Pública de Gestión Privada'),
        ('3', 'Privada'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO gestion (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in datos])
        )
    )

def downgrade():
    op.drop_table('gestion')
