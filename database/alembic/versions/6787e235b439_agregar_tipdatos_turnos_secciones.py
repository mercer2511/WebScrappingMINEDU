"""agregar_tipdatos_turnos_secciones

Revision ID: 6787e235b439
Revises: ee1783a77b72
Create Date: 2026-05-16 15:38:19.681303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6787e235b439'
down_revision: Union[str, Sequence[str], None] = 'ee1783a77b72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    datos = [
        ("C006", "01", "MAÑANA"),
        ("C006", "02", "TARDE"),
        ("C006", "03", "NOCHE"),
        ("C208", "01", "MAÑANA"),
        ("C208", "02", "TARDE"),
        ("C208", "03", "NOCHE"),
    ]
    valores = ", ".join([f"('{c}', '{t}', '{d}')" for c, t, d in datos])
    op.execute(
        sa.text(
            f"INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) "
            f"VALUES {valores} ON CONFLICT (cuadro_codigo, tipdato) DO NOTHING"
        )
    )

def downgrade():
    pass
