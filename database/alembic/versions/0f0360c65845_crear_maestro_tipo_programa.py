"""crear_maestro_tipo_programa

Revision ID: 0f0360c65845
Revises: b61612da429f
Create Date: 2026-05-16 14:34:35.581635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f0360c65845'
down_revision: Union[str, Sequence[str], None] = 'b61612da429f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tipo_programa',
        sa.Column('codigo', sa.String(2), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        ('11', 'Ciclo I – Entorno Familiar'),
        ('12', 'Ciclo I – Entorno Comunitario'),
        ('13', 'Ciclo I - Set'),
        ('14', 'Ciclo II – Entorno Familiar'),
        ('15', 'Ciclo II – Entorno Comunitario'),
        ('a', 'No aplica'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO tipo_programa (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in datos])
        )
    )

def downgrade():
    op.drop_table('tipo_programa')
