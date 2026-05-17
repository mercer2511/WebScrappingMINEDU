"""agregar_cuadros_turnos_secciones

Revision ID: ee1783a77b72
Revises: a914162c67f7
Create Date: 2026-05-16 15:30:45.103563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee1783a77b72'
down_revision: Union[str, Sequence[str], None] = 'a914162c67f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    nuevos = [
        ("C005", "Turnos por día de la semana (cédulas 6A, 9A)"),
        ("C006", "Días de la semana según turno que brinda el servicio de enseñanza"),
        ("C208", "Número total de secciones por ciclo, según turno (cédula 9A)"),
    ]
    valores = ", ".join([f"('{c}', '{d}')" for c, d in nuevos])
    op.execute(
        sa.text(
            f"INSERT INTO cuadro (codigo, descripcion) VALUES {valores} "
            f"ON CONFLICT (codigo) DO NOTHING"
        )
    )

def downgrade():
    for cod in ['C005', 'C006', 'C208']:
        op.execute(sa.text("DELETE FROM cuadro WHERE codigo = :cod"), {"cod": cod})
