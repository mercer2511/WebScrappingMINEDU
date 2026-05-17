"""agregar_cuadros_locales

Revision ID: 5bfade7fec94
Revises: 8ff6b283f057
Create Date: 2026-05-16 16:07:42.601951

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bfade7fec94'
down_revision: Union[str, Sequence[str], None] = '8ff6b283f057'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    cuadros = [
        ("C106", "Área techada por terreno, edificación y piso"),
        ("C107", "Levantamiento Topográfico"),
        ("C108", "Condición de tenencia del terreno (Saneamiento Físico Legal)"),
        ("C114", "Tramos del perímetro del terreno"),
        ("C202", "Procedencia del abastecimiento de agua"),
        ("C206", "Tipo de conexión de desagüe"),
        ("C207", "Procedencia de la energía eléctrica"),
        ("C302", "Características del cerco perimétrico"),
        ("C303", "Otros elementos en el local educativo"),
        ("C401", "Edificaciones en el local educativo"),
        ("C501", "Aulas o espacios acondicionados como aulas"),
        ("C601", "Otros espacios educativos y de soporte distintos al aula"),
        ("C605", "Espacios deportivos abiertos y exteriores"),
        ("C701", "Servicios higiénicos"),
        ("C801", "Recursos Tecnológicos"),
        ("C802", "Equipamiento"),
        ("C803", "Equipos de interconexión y Protección de energía"),
        ("C901", "Espacios educativos y/o administrativos"),
        ("C1171", "Trayectos desde la UGEL al Local Educativo"),
        ("C1173", "Trayectos desde la capital distrital al local educativo"),
        ("C2223", "Líneas de internet contratadas en el local educativo"),
        ("P101", "Servicios/niveles educativos que funcionan en el local"),
    ]
    valores = ", ".join([f"('{c}', '{d}')" for c, d in cuadros])
    op.execute(
        sa.text(
            f"INSERT INTO cuadro (codigo, descripcion) VALUES {valores} "
            f"ON CONFLICT (codigo) DO NOTHING"
        )
    )

def downgrade():
    codigos = ["C106","C107","C108","C114","C202","C206","C207","C302","C303",
               "C401","C501","C601","C605","C701","C801","C802","C803","C901",
               "C1171","C1173","C2223","P101"]
    for c in codigos:
        op.execute(sa.text("DELETE FROM cuadro WHERE codigo = :cod"), {"cod": c})
