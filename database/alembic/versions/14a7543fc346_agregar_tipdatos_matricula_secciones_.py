"""agregar_tipdatos_matricula_secciones_parte8

Revision ID: 14a7543fc346
Revises: fffa85e6e421
Create Date: 2026-05-16 18:06:26.183674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14a7543fc346'
down_revision: Union[str, Sequence[str], None] = 'fffa85e6e421'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    cuadros_carreras = ["C202", "C203", "C209", "C210", "C216", "C217", "C222", "C223"]

    datos = [
        ("CAT8110093", "MANEJO DE MAQUINARIAS Y EQUIPOS AGRÍCOLAS"),
        ("CAT8116478", "MANEJO POST COSECHA"),
        ("CAT0416463", "MANEJO VEHÍCULAR"),
        ("CAT8116487", "MANEJO Y CRIANZA DE AVES"),
        ("CAT7326242", "MANTENIMIENTO BÁSICO DE CASA Y EDIFICIOS"),
        ("CAT7116324", "MANTENIMIENTO BÁSICO DE INSTALACIONES ELÉCTRICAS"),
        ("CAT7326402", "MANTENIMIENTO BÁSICO EN CARPINTERÍA"),
        ("CAT6126276", "MANTENIMIENTO DE EQUIPO DE CÓMPUTO"),
        ("CAT6125867", "MANTENIMIENTO DE EQUIPOS DE COMPUTO"),
        ("CAT6120043", "MANTENIMIENTO DE EQUIPOS DE CÓMPUTO Y ADMINISTRACIÓN DE REDES"),
        ("CAT5316458", "MANTENIMIENTO DE LABORATORIO QUIMÍCO"),
        ("CAT7116310", "MANTENIMIENTO DE SISTEMAS ELÉCTRICOS"),
        ("CAT7136277", "MANTENIMIENTO DE VEHÍCULO MOTORIZADOS"),
        ("CAT7130043", "MANTENIMIENTO DE VEHÍCULOS"),
        ("CAT7135968", "MANTENIMIENTO MECÁNICO DE MAQUINARIA PESADA"),
        ("CAT2146215", "MANUALIDADES"),
        ("CAT9196499", "MASOTERAPIA"),
        ("CAT7210033", "MATARIFE Y PREPARACIONES CÁRNICAS BÁSICAS"),
        ("CAT7136295", "MECÁNCIA DE MOTOS Y VEHÍCULOS AFINES"),
        ("CAT7136222", "MECÁNICA AUTOMOTRIZ"),
        ("CAT7136228", "MECÁNICA AUTOMOTRIZ Y MOTOS"),
        ("CAT7130073", "MECÁNICA DE BANCO"),
        ("CAT7136381", "MECÁNICA DE METALES"),
        ("CAT7136233", "MECÁNICA DE MOTOCICLETAS"),
        ("CAT7136416", "MECÁNICA DE MOTORES"),
        ("CAT7136069", "MECÁNICA DE MOTORES DE MAQUINARIA PESADA"),
        ("CAT7136243", "MECÁNICA DE MOTORES MENORES"),
        ("CAT7136170", "MECÁNICA DE MOTORES VEHÍCULOS BÁSICA"),
        ("CAT7136516", "MECÁNICA DE MOTORES Y VEHÍCULOS BÁSICA"),
        ("CAT7136380", "MECÁNICA DE MOTOS"),
        ("CAT7136508", "MECÁNICA DE MOTOS Y VEHÍCULOS AFINES"),
        ("CAT7136271", "MECÁNICA DE PRODUCCIÓN"),
        ("CAT7136221", "MECÁNICA EN AUTOMOTRIZ Y MOTOS"),
        ("CAT7136641", "MECÁNICA EN SOLDADURA"),
        ("CAT7136314", "MECÁNICA Y METALES"),
        ("CAT7136216", "MECÁNICA Y METALES -B"),
        ("CAT7136452", "MECÁNICA Y MOTORES"),
        ("CAT7136410", "MECÁNICO TORNERO"),
        ("CAT2156336", "MÚSICA"),
        ("CAT6116370", "OFIMÁTICA"),
        ("CAT2116372", "OFIMÁTICA Y DISEÑO GRÁFICO"),
        ("CAT6126444", "OPERACIÓN DE CENTROS DE CÓMPUTO"),
        ("CAT6116213", "OPERACIÓN DE COMPUTADORAS"),
        ("CAT6116261", "OPERACIÓN DE PROGRAMAS DE COMPUTACIÓN"),
        ("CAT6116536", "OPERACIÓN DE PROGRAMAS DE COMPUTACIÓN E INFORMÁTICA"),
        ("CAT4136460", "OPERACIONES DE ALMACENAMIENTO"),
        ("CAT6116234", "OPERACIONES DE COMPUTADORAS"),
        ("CAT0216414", "OPERACIONES DE LIMPIEZA DE HABITACIONES Y ESPACIOS PÚBLICOS"),
        ("CAT0410033", "OPERADOR DE EQUIPOS PESADOS"),
        ("CAT6116325", "OPERADOR DE PROGRAMAS DE COMPUTACIÓN E INFORMÁTICA"),
        ("CAT6116326", "OPERADOR EN OFIMÁTICA"),
        ("CAT0416349", "OPERATIVIDAD DE MÁQUINA"),
        ("CAT7236450", "OPERATIVIDAD DE MÁQUINAS DE CONFECCIÓN"),
        ("CAT0146427", "ORIENTADOR TURISTICO"),
        ("CATAG99999", "OTROS"),
    ]

    for cuadro in cuadros_carreras:
        for i in range(0, len(datos), 500):
            lote = datos[i:i + 500]
            valores = ", ".join(
                [f"('{cuadro}', '{c}', '{d}')" for c, d in lote]
            )

            op.execute(
                sa.text(
                    f"""
                    INSERT INTO cuadro_tipdato (
                        cuadro_codigo,
                        tipdato,
                        descripcion
                    )
                    VALUES {valores}
                    ON CONFLICT (cuadro_codigo, tipdato) DO NOTHING
                    """
                )
            )


def downgrade():
    pass
