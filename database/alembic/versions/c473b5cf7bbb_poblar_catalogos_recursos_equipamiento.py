"""poblar_catalogos_recursos_equipamiento

Revision ID: c473b5cf7bbb
Revises: cafaa1106257
Create Date: 2026-05-16 18:41:51.069592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c473b5cf7bbb'
down_revision: Union[str, Sequence[str], None] = 'cafaa1106257'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================================================
    # 1. INSERTAR LOS CUADROS FALTANTES (CON ON CONFLICT)
    # =========================================================
    op.execute("""
        INSERT INTO cuadro (codigo, descripcion) VALUES
        ('C407', '407. Sobre el acceso a internet en las instalaciones'),
        ('C408', '408. Sobre el acceso a internet en el domicilio'),
        ('C409', '409. En el presente año, ¿cuentan con pc o laptop en su domicilio?'),
        ('C411', '411. Nivel de uso de plataformas tecnológicas para clases virtuales'),
        ('C503', '503. Sobre el acceso a internet en las instalaciones'),
        ('C504', '504. Sobre el acceso a internet en el domicilio / instalaciones'),
        ('C505', '505. Sobre el acceso a internet en el domicilio / pc o laptop en domicilio'),
        ('C506', '506. En el presente año, ¿cuentan con pc o laptop en su domicilio?'),
        ('C507', '507. Sobre el acceso a internet en las instalaciones'),
        ('C508', '508. Acceso a internet en domicilio / Uso de plataformas tecnológicas'),
        ('C509', '509. En el presente año, ¿cuentan con pc o laptop en su domicilio?'),
        ('C511', '511. Nivel de uso de plataformas tecnológicas para clases virtuales')
        ON CONFLICT (codigo) DO NOTHING;
    """)

    # =========================================================
    # 2. INSERTAR TIPDATOS - ACTORES (01 al 04)
    # =========================================================
    cuadros_actores = ['C407', 'C408', 'C409', 'C503', 'C504', 'C505', 'C506', 'C507', 'C509']
    for c in cuadros_actores:
        op.execute(f"""
            INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES
            ('{c}', '01', 'Los estudiantes'),
            ('{c}', '02', 'El personal directivo'),
            ('{c}', '03', 'El personal docente'),
            ('{c}', '04', 'El personal administrativo')
            ON CONFLICT (tipdato, cuadro_codigo) DO NOTHING;
        """)

    # =========================================================
    # 3. INSERTAR TIPDATOS - PLATAFORMAS (01 al 10)
    # =========================================================
    # Nota: Asumimos C511 basado en el patrón de C411 y los datos del parquet
    cuadros_plataformas = ['C411', 'C511']
    for c in cuadros_plataformas:
        op.execute(f"""
            INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES
            ('{c}', '01', 'Moodle'),
            ('{c}', '02', 'Canvas'),
            ('{c}', '03', 'Zoom'),
            ('{c}', '04', 'Meet'),
            ('{c}', '05', 'Teams'),
            ('{c}', '06', 'Whatsapp'),
            ('{c}', '07', 'Facebook/Messenger'),
            ('{c}', '08', 'Classroom'),
            ('{c}', '09', 'Otro 1 (Especificar)'),
            ('{c}', '10', 'Otro 2 (Especificar)')
            ON CONFLICT (tipdato, cuadro_codigo) DO NOTHING;
        """)

    # =========================================================
    # 4. MANEJO ESPECIAL PARA C508 (COLISIÓN DE ACTORES Y PLATAFORMAS)
    # =========================================================
    op.execute("""
        INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES
        ('C508', '01', 'Estudiantes / Moodle (Según Cédula)'),
        ('C508', '02', 'Personal directivo / Canvas (Según Cédula)'),
        ('C508', '03', 'Personal docente / Zoom (Según Cédula)'),
        ('C508', '04', 'Personal administrativo / Meet (Según Cédula)'),
        ('C508', '05', 'Teams'),
        ('C508', '06', 'Whatsapp'),
        ('C508', '07', 'Facebook/Messenger'),
        ('C508', '08', 'Classroom'),
        ('C508', '09', 'Otro 1 (Especificar)'),
        ('C508', '10', 'Otro 2 (Especificar)')
        ON CONFLICT (tipdato, cuadro_codigo) DO UPDATE SET descripcion = EXCLUDED.descripcion;
    """)

    # =========================================================
    # 5. INSERTAR TIPDATOS - EQUIPAMIENTO (01 al 13)
    # =========================================================
    cuadros_equip = ['C401', 'C501']
    for c in cuadros_equip:
        op.execute(f"""
            INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES
            ('{c}', '01', 'Televisores'),
            ('{c}', '02', 'Computadoras de escritorio'),
            ('{c}', '03', 'Laptops convencionales'),
            ('{c}', '04', 'Laptop XO'),
            ('{c}', '05', 'Servidores'),
            ('{c}', '06', 'Tablets'),
            ('{c}', '07', 'Proyectores'),
            ('{c}', '08', 'Radiograbadoras'),
            ('{c}', '09', 'DVD o Blue Ray'),
            ('{c}', '10', 'Impresoras'),
            ('{c}', '11', 'Pizarras digitales'),
            ('{c}', '12', 'Modem'),
            ('{c}', '13', 'Servicio de Internet')
            ON CONFLICT (tipdato, cuadro_codigo) DO NOTHING; 
        """)


def downgrade():
    # En caso de revertir, solo eliminamos las llaves numéricas para no borrar CABLEADO_01, etc.
    op.execute("""
        DELETE FROM cuadro_tipdato 
        WHERE tipdato IN ('01','02','03','04','05','06','07','08','09','10','11','12','13')
        AND cuadro_codigo IN ('C407','C408','C409','C411','C503','C504','C505','C506','C507','C508','C509','C511','C401','C501');
    """)
    op.execute("""
        DELETE FROM cuadro WHERE codigo IN ('C407','C408','C409','C411','C503','C504','C505','C506','C507','C508','C509','C511');
    """)
