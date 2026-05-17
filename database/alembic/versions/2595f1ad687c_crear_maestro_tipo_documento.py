"""crear_maestro_tipo_documento

Revision ID: 2595f1ad687c
Revises: 6787e235b439
Create Date: 2026-05-16 15:38:48.125458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2595f1ad687c'
down_revision: Union[str, Sequence[str], None] = '6787e235b439'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'tipo_documento',
        sa.Column('codigo', sa.String(2), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        ("01", "Resolución Directoral"),
        ("02", "Resolución Ministerial"),
        ("03", "Decreto Supremo"),
        ("04", "Oficio"),
        ("05", "Resolución Directoral Regional"),
        ("06", "Otro"),
    ]
    valores = ", ".join([f"('{c}', '{d}')" for c, d in datos])
    op.execute(
        sa.text(
            f"INSERT INTO tipo_documento (codigo, descripcion) VALUES {valores}"
        )
    )

def downgrade():
    op.drop_table('tipo_documento')
