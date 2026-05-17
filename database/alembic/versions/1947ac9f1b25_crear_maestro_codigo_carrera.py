"""crear_maestro_codigo_carrera

Revision ID: 1947ac9f1b25
Revises: 7d637b76fd29
Create Date: 2026-05-16 14:32:41.791513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1947ac9f1b25'
down_revision: Union[str, Sequence[str], None] = '7d637b76fd29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'codigo_carrera',
        sa.Column('codigo', sa.String(1), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        ('1', 'Unidocente multigrado'),
        ('2', 'Polidocente multigrado'),
        ('3', 'Polidocente completo'),
        ('a', 'No aplica'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO codigo_carrera (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in datos])
        )
    )

def downgrade():
    op.drop_table('codigo_carrera')
