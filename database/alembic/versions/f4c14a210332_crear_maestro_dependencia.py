"""crear_maestro_dependencia

Revision ID: f4c14a210332
Revises: 25581d793c2e
Create Date: 2026-05-16 13:13:44.756744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4c14a210332'
down_revision: Union[str, Sequence[str], None] = '25581d793c2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'dependencia',
        sa.Column('codigo', sa.String(2), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        ('A1', 'Sector Educación'),
        ('A2', 'Otro sector público (FF.AA.)'),
        ('A3', 'Municipalidad'),
        ('A4', 'Entidad privada en convenio con Sector Educación'),
        ('B1', 'Cooperativo'),
        ('B2', 'Comunidad o asociación religiosa'),
        ('B3', 'Comunidad'),
        ('B4', 'Particular'),
        ('B5', 'Empresa (Fiscalizado)'),
        ('B6', 'Asociación civil / Institución benéfica'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO dependencia (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in datos])
        )
    )

def downgrade():
    op.drop_table('dependencia')
