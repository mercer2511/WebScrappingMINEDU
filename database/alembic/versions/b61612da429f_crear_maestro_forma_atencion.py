"""crear_maestro_forma_atencion

Revision ID: b61612da429f
Revises: 1947ac9f1b25
Create Date: 2026-05-16 14:33:59.841272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b61612da429f'
down_revision: Union[str, Sequence[str], None] = '1947ac9f1b25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'forma_atencion',
        sa.Column('codigo', sa.String(1), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        ('S', 'Escolarizada'),
        ('N', 'No escolarizada'),
        ('a', 'No aplica'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO forma_atencion (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in datos])
        )
    )

def downgrade():
    op.drop_table('forma_atencion')
