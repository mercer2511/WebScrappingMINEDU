"""crear_maestro_tipo_sexo

Revision ID: 357d033a2289
Revises: c3c8334e3982
Create Date: 2026-05-16 14:35:39.044115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '357d033a2289'
down_revision: Union[str, Sequence[str], None] = 'c3c8334e3982'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tipo_sexo',
        sa.Column('codigo', sa.String(1), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        ('1', 'Varones'),
        ('2', 'Mujeres'),
        ('3', 'Mixto'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO tipo_sexo (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in datos])
        )
    )

def downgrade():
    op.drop_table('tipo_sexo')
