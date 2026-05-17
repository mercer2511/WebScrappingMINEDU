"""crear_maestro_area_censo

Revision ID: 7d637b76fd29
Revises: f4c14a210332
Create Date: 2026-05-16 13:31:25.095376

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d637b76fd29'
down_revision: Union[str, Sequence[str], None] = 'f4c14a210332'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'area_censo',
        sa.Column('codigo', sa.String(1), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    op.execute(
        sa.text(
            "INSERT INTO area_censo (codigo, descripcion) VALUES "
            "('1', 'Urbana'), "
            "('2', 'Rural')"
        )
    )

def downgrade():
    op.drop_table('area_censo')
