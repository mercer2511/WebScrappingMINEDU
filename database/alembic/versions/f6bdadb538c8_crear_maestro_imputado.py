"""crear_maestro_imputado

Revision ID: f6bdadb538c8
Revises: bfed1371e8d6
Create Date: 2026-05-16 14:36:46.966730

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6bdadb538c8'
down_revision: Union[str, Sequence[str], None] = 'bfed1371e8d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'imputado',
        sa.Column('codigo', sa.String(1), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        ('1', 'Declarado'),
        ('2', 'Imputado total'),
        ('3', 'Imputado parcial'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO imputado (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in datos])
        )
    )

def downgrade():
    op.drop_table('imputado')
