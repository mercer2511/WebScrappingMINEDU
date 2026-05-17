"""crear_maestro_cuadro

Revision ID: 4e41d179b1af
Revises: d1bd281c86b4
Create Date: 2026-05-16 15:10:51.303614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e41d179b1af'
down_revision: Union[str, Sequence[str], None] = 'd1bd281c86b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'cuadro',
        sa.Column('codigo', sa.String(10), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    cuadros = [
        ('C101', 'Resultado del ejercicio educativo a diciembre'),
        ('C102', 'Motivo del retiro'),
        ('C201', 'Matrícula por edad/grado/ciclo y sexo según turno'),
        ('C203', 'Matrícula de jóvenes y adultos del CEBA y Periféricos por ciclo, grado y sexo según situación al matricularse'),
        ('C204', 'Matrícula de Círculos de Aprendizaje por ciclo, grado y sexo según situación al matricularse'),
        ('C210', 'Situación al matricularse de estudiantes con otro tipo de NEE o enfermedad (cédula 4AI)'),
        ('C212', 'Situación al matricularse de estudiantes con otro tipo de NEE o enfermedad (cédula 4AA)'),
        ('P101', 'Servicios/niveles educativos que funcionan en el local'),
        ('P102A', 'Horario de clases de los estudiantes'),
        ('P113A', 'Temas de orientación (inicial no escolarizado)'),
        ('P119A', 'Instituciones que organizaron actividad contra la anemia'),
        ('P120A', 'Actividades con familias realizadas'),
        ('P121A', 'Practicantes de universidades o institutos'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO cuadro (codigo, descripcion) VALUES "
            + ", ".join([f"('{c}', '{d}')" for c, d in cuadros])
        )
    )

def downgrade():
    op.drop_table('cuadro')
