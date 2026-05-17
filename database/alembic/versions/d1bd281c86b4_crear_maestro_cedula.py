"""crear_maestro_cedula

Revision ID: d1bd281c86b4
Revises: ef254d67a353
Create Date: 2026-05-16 14:57:18.432397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1bd281c86b4'
down_revision: Union[str, Sequence[str], None] = 'ef254d67a353'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'cedula',
        sa.Column('codigo', sa.String(3), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    cedulas = [
        ('1A', 'Educación Básica Regular Inicial Escolarizada'),
        ('2A', 'Educación Básica Regular Inicial No Escolarizada'),
        ('3AP', 'Educación Básica Regular Primaria'),
        ('3AS', 'Educación Básica Regular Secundaria'),
        ('4AI', 'Educación Básica Alternativa Inicial e Intermedio'),
        ('4AA', 'Educación Básica Alternativa Avanzado'),
        ('5A', 'Educación Superior Pedagógica'),
        ('6A', 'Educación Superior Tecnológica'),
        ('7A', 'Educación Superior de Formación Artística (ESFA)'),
        ('8A', 'Educación Básica Especial Inicial No Escolarizada'),
        ('8AI', 'Educación Básica Especial Inicial Escolarizada'),
        ('8AP', 'Educación Básica Especial Primaria'),
        ('9A', 'Educación Técnico Productiva'),
        ('1B', 'Cédula de Resultado - Educación Básica Regular Inicial Escolarizada'),
        ('2B', 'Cédula de Resultado - Educación Básica Regular Inicial No Escolarizada'),
        ('3BP', 'Cédula de Resultado - Educación Básica Regular Primaria'),
        ('3BS', 'Cédula de Resultado - Educación Básica Regular Secundaria'),
        ('4BI', 'Cédula de Resultado - Educación Básica Alternativa Inicial e Intermedio'),
        ('4BA', 'Cédula de Resultado - Educación Básica Alternativa Avanzado'),
        ('5B', 'Cédula de Resultado - Educación Superior Pedagógica'),
        ('6B', 'Cédula de Resultado - Educación Superior Tecnológica'),
        ('7B', 'Cédula de Resultado - Educación Superior de Formación Artística (ESFA)'),
        ('8BI', 'Cédula de Resultado - Educación Básica Especial Inicial Escolarizada y No Escolarizada'),
        ('8BP', 'Cédula de Resultado - Educación Básica Especial Primaria'),
        ('9B', 'Cédula de Resultado - Educación Técnico Productiva'),
        ('11', 'Local Educativo: Ficha Unificada de Infraestructura Educativa (FUIE)'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO cedula (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in cedulas])
        )
    )

def downgrade():
    op.drop_table('cedula')
