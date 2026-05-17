"""crear_maestro_codigo_turno

Revision ID: bfed1371e8d6
Revises: 357d033a2289
Create Date: 2026-05-16 14:36:08.535841

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfed1371e8d6'
down_revision: Union[str, Sequence[str], None] = '357d033a2289'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'codigo_turno',
        sa.Column('codigo', sa.String(2), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        ('11', 'Sólo en la mañana'),
        ('12', 'Sólo en la tarde'),
        ('13', 'Mañana y tarde'),
        ('14', 'Sólo en la noche'),
        ('15', 'Mañana, tarde y noche'),
        ('16', 'Mañana y noche'),
        ('17', 'Tarde y noche'),
        ('20', 'Discontinuo'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO codigo_turno (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in datos])
        )
    )

def downgrade():
    op.drop_table('codigo_turno')
