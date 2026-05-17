"""agregar_cuadros_docentes

Revision ID: d036099a3ef2
Revises: 2595f1ad687c
Create Date: 2026-05-16 15:49:01.242151

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd036099a3ef2'
down_revision: Union[str, Sequence[str], None] = '2595f1ad687c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    cuadros = [
        ("C301", "Docentes - Fuente de financiamiento"),
        ("C302", "Docentes - Jornada laboral"),
        ("C303", "Docentes - Género"),
        ("C304", "Docentes - Condición laboral"),
        ("C305", "Docentes - Máximo nivel educativo alcanzado"),
        ("C306", "Docentes - Estudios de posgrado en pedagogía / Área curricular a cargo"),
        ("C307", "Docentes - Escala magisterial"),
        ("C308", "Docentes - Situación en el cargo directivo"),
        ("C309", "Docentes - Especialidad del título pedagógico optado"),
        ("C310", "Docentes - Modalidad de contrato"),
        ("C311", "Docentes - Modalidad de contrato / Rango de edad"),
        ("C312", "Docentes - Rango de tiempo de servicio en años (nombrados)"),
        ("C313", "Docentes - Rango de tiempo de experiencia laboral en años"),
        ("C314", "Docentes - Conocimiento en inglés"),
        ("C315", "Docentes - Certificación en inglés"),
        ("C316", "Docentes - Tipo de institución donde estudió la carrera pedagógica"),
        ("C317", "Docentes - Atención a estudiantes con NEE asociadas a discapacidad / Tipo de discapacidad"),
        ("C318", "Docentes - Lengua originaria que domina"),
        ("C319", "Docentes - Conocimiento de la lengua originaria que domina"),
        ("C320", "Docentes - Situación atravesada con respecto a la lengua originaria que domina"),
        ("C321", "Docentes - Tipo de estudios en EIB"),
        ("C322", "Docentes - Pregunta específica"),
        ("C323", "Docentes - Temas que recibió asistencia técnica en el marco de refuerzo escolar"),
        ("C324", "Docentes - Actividad que le genere ingresos económicos"),
        ("C325", "Docentes - Actividad permanente / Ocupación que desempeña / Frecuencia"),
        ("C326", "Docentes - Asistencia y orientación por el SAEV / Conocimiento en TICs"),
    ]
    valores = ", ".join([f"('{c}', '{d}')" for c, d in cuadros])
    op.execute(
        sa.text(
            f"INSERT INTO cuadro (codigo, descripcion) VALUES {valores} "
            f"ON CONFLICT (codigo) DO NOTHING"
        )
    )

def downgrade():
    for c in [f"C{i}" for i in range(301, 327)]:
        op.execute(sa.text("DELETE FROM cuadro WHERE codigo = :cod"), {"cod": c})
