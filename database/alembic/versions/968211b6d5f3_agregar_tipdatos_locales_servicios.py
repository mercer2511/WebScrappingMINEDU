"""agregar_tipdatos_locales_servicios

Revision ID: 968211b6d5f3
Revises: 5bfade7fec94
Create Date: 2026-05-16 16:10:19.944673

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '968211b6d5f3'
down_revision: Union[str, Sequence[str], None] = '5bfade7fec94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    datos = [
        # C202 - Procedencia del abastecimiento de agua
        ("C202", "1", "Red pública (agua potable)"),
        ("C202", "2", "Pilón de uso público (agua potable)"),
        ("C202", "3", "Camión cisterna u otro similar"),
        ("C202", "4", "Pozo"),
        ("C202", "5", "Sistema de Captación de agua de lluvia"),
        ("C202", "6", "Río, acequia, manantial u otro"),
        ("C202", "7", "Otro"),
        ("C202", "8", "No tiene"),
        # C206 - Tipo de conexión de desagüe
        ("C206", "1", "Red pública"),
        ("C206", "2", "Río, acequia o canal"),
        ("C206", "3", "Tanque séptico"),
        ("C206", "4", "Biodigestor"),
        ("C206", "5", "Pozo sin tratamiento"),
        ("C206", "6", "Unidades Básicas de Saneamiento con Compostera (UBS-C)"),
        ("C206", "7", "Otro"),
        ("C206", "8", "No tiene"),
        # C207 - Procedencia de la energía eléctrica
        ("C207", "1", "Red pública (de una empresa distribuidora de energía eléctrica)"),
        ("C207", "2", "Generador o motor de municipio"),
        ("C207", "3", "Generador o motor de la comunidad"),
        ("C207", "4", "Generador o motor del local educativo"),
        ("C207", "5", "Panel solar"),
        ("C207", "6", "Energía eólica"),
        ("C207", "7", "Otro"),
        ("C207", "8", "No tiene"),
        # C2223 - Internet: tipo de conexión
        ("C2223", "TIPO_CONEXION_01", "Red Cableada - ADSL-P (Cable telefónico)"),
        ("C2223", "TIPO_CONEXION_02", "Red Cableada - FTTH (Fibra óptica)"),
        ("C2223", "TIPO_CONEXION_03", "Red Cableada - HFC (Híbrido de fibra+coaxial)"),
        ("C2223", "TIPO_CONEXION_04", "Red Cableada - Cable (Cable coaxial)"),
        ("C2223", "TIPO_CONEXION_05", "Internet Satelital"),
        ("C2223", "TIPO_CONEXION_06", "Red Inalámbrica por WIFI"),
        ("C2223", "TIPO_CONEXION_07", "Red Inalámbrica por Internet Portátil/USB Modem"),
        ("C2223", "TIPO_CONEXION_08", "Red Inalámbrica por Radioenlace"),
        ("C2223", "TIPO_CONEXION_09", "Otro"),
        # C2223 - Internet: empresa operadora
        ("C2223", "OPERADOR_01", "Movistar/Telefónica Movistar del Perú S.A.A."),
        ("C2223", "OPERADOR_02", "Claro"),
        ("C2223", "OPERADOR_03", "Entel"),
        ("C2223", "OPERADOR_04", "BITEL/VIETTEL PERU S.A.C"),
        ("C2223", "OPERADOR_05", "VSAT/MINEDU"),
        ("C2223", "OPERADOR_06", "LEVEL3"),
        ("C2223", "OPERADOR_07", "WIN"),
        ("C2223", "OPERADOR_08", "Otro"),
        # C2223 - Internet: entidad que financia
        ("C2223", "FINANCIA_01", "MINEDU"),
        ("C2223", "FINANCIA_02", "Unidad Ejecutora/UGEL/DRE"),
        ("C2223", "FINANCIA_03", "Gobierno Regional"),
        ("C2223", "FINANCIA_04", "Gobierno Local/Municipal"),
        ("C2223", "FINANCIA_05", "MTC (Concesión/Convenio)"),
        ("C2223", "FINANCIA_06", "Comunidad"),
        ("C2223", "FINANCIA_07", "Recursos propios de la IE/Autofinanciado por la IE"),
        ("C2223", "FINANCIA_08", "APAFA/Padres de familia"),
        ("C2223", "FINANCIA_09", "Personal de la I.E."),
        ("C2223", "FINANCIA_10", "Empresa Privada u Organización"),
        ("C2223", "FINANCIA_11", "Otro"),
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
