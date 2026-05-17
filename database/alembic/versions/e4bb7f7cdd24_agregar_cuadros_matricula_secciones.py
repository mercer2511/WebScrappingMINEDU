"""agregar_cuadros_matricula_secciones

Revision ID: e4bb7f7cdd24
Revises: a0dc74ebf80a
Create Date: 2026-05-16 17:13:00.312062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e4bb7f7cdd24'
down_revision: Union[str, Sequence[str], None] = 'a0dc74ebf80a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    cuadros = [
        # Matrícula y Secciones (ESNU)
        ("C201", "Matrícula en carreras de 4+ años, por ciclo y sexo, según edad y modalidad"),
        ("C202", "Matrícula en carreras de 4+ años, por ciclo y sexo, según sede y modalidad"),
        ("C203", "Postulantes e ingresantes en carreras de 4+ años, por sexo, según denominación de carrera"),
        ("C204", "Ingresantes en carreras de 4+ años, por edad, según sexo"),
        ("C205", "Matrícula en carreras de 4+ años, por edad y sexo, según tipo de programa de reparación en educación"),
        ("C206", "Matrícula en carreras de 4+ años, por ciclo y sexo, según lengua materna"),
        ("C207", "Número total de secciones en carreras de 4+ años, por ciclo, según turno"),
        ("C208", "Matrícula en carreras de 3 años, por ciclo y sexo, según edad y modalidad"),
        ("C209", "Matrícula en carreras de 3 años, por ciclo y sexo, según sede y modalidad"),
        ("C210", "Postulantes e ingresantes en carreras de 3 años, por sexo, según denominación de carrera"),
        ("C211", "Ingresantes en carreras de 3 años, por edad, según sexo"),
        ("C212", "Matrícula en carreras de 3 años, por edad y sexo, según tipo de programa de reparación"),
        ("C213", "Matrícula en carreras de 3 años, por ciclo y sexo, según lengua materna"),
        ("C214", "Número total de secciones en carreras de 3 años, por ciclo, según turno"),
        ("C215", "Matrícula en carreras de 2 años, por ciclo y sexo, según edad y modalidad"),
        ("C216", "Matrícula en carreras de 2 años, por ciclo y sexo, según sede y modalidad"),
        ("C217", "Postulantes e ingresantes en carreras de 2 años, por sexo, según denominación de carrera"),
        ("C218", "Ingresantes en carreras de 2 años, por edad, según sexo"),
        ("C219", "Matrícula en carreras de 2 años, por edad y sexo, según tipo de programa de reparación"),
        ("C220", "Matrícula en carreras de 2 años, por ciclo y sexo, según lengua materna"),
        ("C221", "Número total de secciones en carreras de 2 años, por ciclo, según turno"),
        ("C222", "Matrícula por tipo de discapacidad u otra condición y sexo, según carreras (2,3,4+ años)"),
        ("C223", "Ingresantes por tipo de discapacidad u otra condición y sexo, según carreras (2,3,4+ años)"),
        ("C224", "Matrícula en carreras de 2+ años por ciclo y sexo, según año de egreso de la EBR"),
    ]
    valores = ", ".join([f"('{c}', '{d}')" for c, d in cuadros])
    op.execute(
        sa.text(
            f"INSERT INTO cuadro (codigo, descripcion) VALUES {valores} "
            f"ON CONFLICT (codigo) DO NOTHING"
        )
    )

def downgrade():
    for c in [f"C{i}" for i in range(201, 225)]:
        op.execute(sa.text("DELETE FROM cuadro WHERE codigo = :cod"), {"cod": c})
