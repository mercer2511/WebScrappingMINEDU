"""crear_maestro_nivel_modalidad

Revision ID: 25581d793c2e
Revises: 3e254f11b687
Create Date: 2026-05-16 13:02:34.623535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25581d793c2e'
down_revision: Union[str, Sequence[str], None] = '3e254f11b687'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'nivel_modalidad',
        sa.Column('codigo', sa.String(2), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    # Datos consolidados de todas las fuentes
    niveles = [
        ('A1', 'Inicial - Cuna'),
        ('A2', 'Inicial - Jardín'),
        ('A3', 'Inicial – Cuna-jardín'),
        ('A5', 'Inicial – Programa no escolarizado'),
        ('B0', 'Primaria'),
        ('F0', 'Secundaria'),
        ('D1', 'Básica Alternativa – CEBA Inicial e Intermedio'),
        ('D2', 'Básica Alternativa – CEBA Avanzado'),
        ('E0', 'Básica Especial - PRITE'),
        ('E1', 'Básica Especial - Inicial'),
        ('E2', 'Básica Especial - Primaria'),
        ('K0', 'Superior Pedagógica - ISP'),
        ('P0', 'Escuela de Educación Superior Pedagógica - EESP'),
        ('T0', 'Superior Tecnológica - IST'),
        ('S0', 'Escuela de Educación Superior Tecnológica - EEST'),
        ('M0', 'Superior Artística - ESFA'),
        ('L0', 'Técnico Productiva – CETPRO'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO nivel_modalidad (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in niveles])
        )
    )

def downgrade():
    op.drop_table('nivel_modalidad')
