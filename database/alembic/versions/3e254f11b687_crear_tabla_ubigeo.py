"""crear_tabla_ubigeo

Revision ID: 3e254f11b687
Revises: 
Create Date: 2026-05-16 12:47:34.833799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e254f11b687'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'ubigeo',
        sa.Column('codgeo', sa.String(6), primary_key=True),
        sa.Column('departamento', sa.String(60), nullable=False),
        sa.Column('provincia', sa.String(60), nullable=False),
        sa.Column('distrito', sa.String(60), nullable=False),
        sa.Column('capital_legal', sa.String(100)),
    )

def downgrade():
    op.drop_table('ubigeo')
