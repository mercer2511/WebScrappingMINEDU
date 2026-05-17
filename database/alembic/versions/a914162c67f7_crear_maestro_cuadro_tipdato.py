"""crear_maestro_cuadro_tipdato

Revision ID: a914162c67f7
Revises: 4e41d179b1af
Create Date: 2026-05-16 15:11:21.692912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a914162c67f7'
down_revision: Union[str, Sequence[str], None] = '4e41d179b1af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'cuadro_tipdato',
        sa.Column('cuadro_codigo', sa.String(10), sa.ForeignKey('cuadro.codigo'), primary_key=True),
        sa.Column('tipdato', sa.String(20), primary_key=True),
        sa.Column('descripcion', sa.Text, nullable=False),
    )
    datos = [
        # C101 - Situación del ejercicio
        ('C101', '01', 'Promovidos'),
        ('C101', '02', 'Trasladados a otros SS.EE.'),
        ('C101', '03', 'Retirados'),
        ('C101', '04', 'Fallecidos'),
        # C102 - Motivo del retiro
        ('C102', '01', 'Situación económica'),
        ('C102', '02', 'Violencia'),
        ('C102', '03', 'Enfermedad'),
        ('C102', '04', 'Otro'),
        # C203 - Situación al matricularse (CEBA/Periféricos, cédula 4AI)
        ('C203', '01', 'INGRESANTES (Cursan por primera vez el 1° grado en el ciclo de la EBA)'),
        ('C203', '02', 'PROMOVIDOS del mismo CEBA Referencial (Aprobaron el periodo anterior)'),
        ('C203', '03', 'PROMOVIDOS de otro CEBA (Aprobaron el periodo anterior en otro CEBA)'),
        ('C203', '04', 'PERMANECE EN EL GRADO EN EL MISMO CEBA Referencial o Periférico (Repetidor)'),
        ('C203', '05', 'PERMANECE EN EL GRADO PROVENIENTE DE OTRO CEBA (Repetidor)'),
        ('C203', '06', 'REENTRANTES (Dejaron de estudiar más de un periodo promocional en la EBA)'),
        # C204 - Situación al matricularse (Círculos de Aprendizaje, 4AI)
        ('C204', '01', 'INGRESANTES (Cursan por primera vez el 1° grado en el ciclo de la EBA)'),
        ('C204', '02', 'PROMOVIDOS del mismo Círculo de Aprendizaje'),
        ('C204', '03', 'PROMOVIDOS de otro CEBA'),
        ('C204', '04', 'PERMANECE EN EL GRADO EN EL MISMO Círculo de Aprendizaje (Repetidor)'),
        ('C204', '05', 'PERMANECE EN EL GRADO PROVENIENTE DE OTRO CEBA (Repetidor)'),
        ('C204', '06', 'REENTRANTES'),
        # C210 - NEE o enfermedad (4AI)
        ('C210', '01', 'N° de estudiantes con otro tipo de NEE o enfermedad que desertaron o se retiraron'),
        ('C210', '02', 'N° de estudiantes con otro tipo de NEE o enfermedad que promovieron de grado'),
        # C212 - NEE o enfermedad (4AA)
        ('C212', '01', 'N° de estudiantes con otro tipo de NEE o enfermedad que desertaron o se retiraron'),
        ('C212', '02', 'N° de estudiantes con otro tipo de NEE o enfermedad que promovieron de grado'),
        # P113A - Temas de orientación
        ('P113A', '01', 'APRENDIZAJES'),
        ('P113A', '02', 'PAUTA DE CRIANZA'),
        ('P113A', '03', 'VIOLENCIA'),
        ('P113A', '04', 'INCLUSIÓN'),
        ('P113A', '05', 'ALIMENTACIÓN Y HÁBITOS DE HIGIENE'),
        ('P113A', '06', 'OTRO'),
        # P119A - Entidades contra la anemia
        ('P119A', '01', 'Servicio/Nivel educativo'),
        ('P119A', '02', 'UGEL/DRE'),
        ('P119A', '03', 'Establecimiento de salud'),
        ('P119A', '04', 'Municipalidad'),
        ('P119A', '05', 'Organización No Gubernamental (ONG)'),
        ('P119A', '06', 'Otro'),
        # P120A - Actividades con familias
        ('P120A', '01', 'Jornadas con familias'),
        ('P120A', '02', 'Encuentros familiares'),
        ('P120A', '03', 'Reuniones informativas con familias'),
        ('P120A', '04', 'Talleres con familias'),
        # P121A - Practicantes
        ('P121A', '01', 'De universidad'),
        ('P121A', '02', 'De instituto'),
        ('P121A', '03', 'Ninguno'),
    ]
    op.execute(
        sa.text(
            "INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES "
            + ", ".join([f"('{c}', '{t}', '{d}')" for c, t, d in datos])
        )
    )

def downgrade():
    op.drop_table('cuadro_tipdato')
