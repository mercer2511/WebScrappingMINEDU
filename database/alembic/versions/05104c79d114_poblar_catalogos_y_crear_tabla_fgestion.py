"""poblar_catalogos_y_crear_tabla_fgestion

Revision ID: 05104c79d114
Revises: 680135b4bad2
Create Date: 2026-05-16 19:03:32.574615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05104c79d114'
down_revision: Union[str, Sequence[str], None] = '680135b4bad2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================================================
    # 1. INSERTAR LOS CUADROS FALTANTES (CON ON CONFLICT)
    # =========================================================
    op.execute("""
               INSERT INTO cuadro (codigo, descripcion)
               VALUES ('C402', '402. Frecuencia con la que el gobierno local ayuda o interviene'),
                      ('C417', '417. Capacitación en materia de gestión integral del riesgo'),
                      ('C418', '418. Experiencia exitosa o buena práctica docente'),
                      ('C420', '420. Capacitación en materia de gestión integral del riesgo'),
                      ('C421', '421. Experiencia exitosa o buena práctica docente'),
                      ('C502', '502. Frecuencia con la que el gobierno local ayuda o interviene'),
                      ('C520', '520. Capacitación en materia de gestión integral del riesgo'),
                      ('C521', '521. Experiencia exitosa o buena práctica docente'),
                      ('C602', '602. Frecuencia con la que el gobierno local ayuda o interviene'),
                      ('C615', '615. Personal administrativo que labora en el servicio'),
                      ('C630', '630. Capacitación en materia de gestión integral del riesgo'),
                      ('C631', '631. Experiencia exitosa o buena práctica docente'),
                      ('C702', '702. Frecuencia con la que el gobierno local ayuda o interviene'),
                      ('C715', '715. Personal administrativo que labora en el servicio'),
                      ('C730', '730. Capacitación en materia de gestión integral del riesgo'),
                      ('C731', '731. Experiencia exitosa o buena práctica docente'),
                      ('C732', '732. Capacitación en materia de gestión integral del riesgo'),
                      ('C733', '733. Experiencia exitosa o buena práctica docente')
               ON CONFLICT (codigo) DO NOTHING;
               """)

    # =========================================================
    # 2. INSERTAR TIPDATOS POR CATEGORÍAS
    # =========================================================

    # --- CATEGORÍA A: Frecuencia de ayuda Gobierno Local (20 ítems) ---
    cuadros_gob_20 = ['C402', 'C502']
    for c in cuadros_gob_20:
        op.execute(f"""
            INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES
            ('{c}', '01', 'Infraestructura - Proyecto inversión mejoramiento'),
            ('{c}', '02', 'Infraestructura - Apoyo recursos mantenimiento preventivo'),
            ('{c}', '03', 'Infraestructura - Gestiones servicios básicos'),
            ('{c}', '04', 'Infraestructura - Adquisición mobiliario y equipamiento'),
            ('{c}', '05', 'Aprendizajes - Proyecto inversión mejora aprendizajes'),
            ('{c}', '06', 'Aprendizajes - Programas de Reforzamiento Escolar'),
            ('{c}', '07', 'Aprendizajes - Apoyo con material educativo'),
            ('{c}', '08', 'Docentes - Contratación de docentes'),
            ('{c}', '09', 'Docentes - Talleres o cursos de capacitación'),
            ('{c}', '10', 'No Docentes - Contratación de no docentes'),
            ('{c}', '11', 'No Docentes - Talleres o cursos de capacitación'),
            ('{c}', '12', 'Gestión - Articulación local actores públicos/privados'),
            ('{c}', '13', 'Gestión - Atención de casos en DEMUNA'),
            ('{c}', '14', 'Gestión - Articulación con UGEL y DRE'),
            ('{c}', '15', 'Gestión - Gestiones instalación conectividad'),
            ('{c}', '16', 'Gestión - Apoyo alimentación estudiantes'),
            ('{c}', '17', 'Gestión - Vivienda y alimentación docentes'),
            ('{c}', '18', 'Gestión - Apoyo movilidad local estudiantes/docentes'),
            ('{c}', '19', 'Recuperación - Promoción acciones estudiantes interrumpen'),
            ('{c}', '20', 'Recuperación - Impulso registro nominal Alerta Escuela')
            ON CONFLICT (tipdato, cuadro_codigo) DO NOTHING;
        """)

    # --- CATEGORÍA B: Frecuencia de ayuda Gobierno Local (18 ítems - sin No Docentes) ---
    cuadros_gob_18 = ['C602', 'C702']
    for c in cuadros_gob_18:
        op.execute(f"""
            INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES
            ('{c}', '01', 'Infraestructura - Proyecto inversión mejoramiento'),
            ('{c}', '02', 'Infraestructura - Apoyo recursos mantenimiento preventivo'),
            ('{c}', '03', 'Infraestructura - Gestiones servicios básicos'),
            ('{c}', '04', 'Infraestructura - Adquisición mobiliario y equipamiento'),
            ('{c}', '05', 'Aprendizajes - Proyecto inversión mejora aprendizajes'),
            ('{c}', '06', 'Aprendizajes - Programas de Reforzamiento Escolar'),
            ('{c}', '07', 'Aprendizajes - Apoyo con material educativo'),
            ('{c}', '08', 'Docentes - Contratación de docentes'),
            ('{c}', '09', 'Docentes - Talleres o cursos de capacitación'),
            ('{c}', '10', 'Gestión - Articulación local actores públicos/privados'),
            ('{c}', '11', 'Gestión - Atención de casos en DEMUNA'),
            ('{c}', '12', 'Gestión - Articulación con UGEL y DRE'),
            ('{c}', '13', 'Gestión - Gestiones instalación conectividad'),
            ('{c}', '14', 'Gestión - Apoyo alimentación estudiantes'),
            ('{c}', '15', 'Gestión - Vivienda y alimentación docentes'),
            ('{c}', '16', 'Gestión - Apoyo movilidad local estudiantes/docentes'),
            ('{c}', '17', 'Recuperación - Promoción acciones estudiantes interrumpen'),
            ('{c}', '18', 'Recuperación - Impulso registro nominal Alerta Escuela')
            ON CONFLICT (tipdato, cuadro_codigo) DO NOTHING;
        """)

    # --- CATEGORÍA C: Capacitación GRD (06 ítems) ---
    cuadros_grd = ['C417', 'C420', 'C520', 'C630', 'C730', 'C732']
    for c in cuadros_grd:
        op.execute(f"""
            INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES
            ('{c}', '01', 'Curso'),
            ('{c}', '02', 'Taller'),
            ('{c}', '03', 'Charla'),
            ('{c}', '04', 'Seminario'),
            ('{c}', '05', 'Webinar'),
            ('{c}', '06', 'Otro (especificar)')
            ON CONFLICT (tipdato, cuadro_codigo) DO NOTHING;
        """)

    # --- CATEGORÍA D: Experiencia Exitosa (04 ítems) ---
    cuadros_exp = ['C418', 'C421', 'C521', 'C631', 'C731', 'C733']
    for c in cuadros_exp:
        op.execute(f"""
            INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES
            ('{c}', '01', 'Gestión del Riesgo de Desastres'),
            ('{c}', '02', 'Adaptación al cambio climático'),
            ('{c}', '03', 'Seguridad y Defensa Nacional'),
            ('{c}', '04', 'Otro (especificar)')
            ON CONFLICT (tipdato, cuadro_codigo) DO NOTHING;
        """)

    # --- CATEGORÍA E: Personal Administrativo (07 ítems) ---
    cuadros_admin = ['C615', 'C715']
    for c in cuadros_admin:
        op.execute(f"""
            INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) VALUES
            ('{c}', '01', 'Coordinador/Administrativo'),
            ('{c}', '02', 'Secretaria (o)'),
            ('{c}', '03', 'Oficinista'),
            ('{c}', '04', 'Guardianía y/o vigilancia'),
            ('{c}', '05', 'Limpieza y mantenimiento'),
            ('{c}', '06', 'Auxiliar de biblioteca'),
            ('{c}', '07', 'Auxiliar de laboratorio')
            ON CONFLICT (tipdato, cuadro_codigo) DO NOTHING;
        """)

    # =========================================================
    # 3. CREAR TABLA TRANSACCIONAL FGESTION
    # =========================================================
    op.create_table(
        'fgestion',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cod_mod', sa.String(length=7), nullable=False, index=True),
        sa.Column('anexo', sa.String(length=1), nullable=False, server_default='0'),

        sa.Column('nivel_modalidad_codigo', sa.String(length=2), sa.ForeignKey('nivel_modalidad.codigo'),
                  nullable=True),
        sa.Column('cedula_codigo', sa.String(length=3), sa.ForeignKey('cedula.codigo'), nullable=True),

        sa.Column('cuadro_codigo', sa.String(length=10), nullable=False),
        sa.Column('tipdato', sa.String(length=20), nullable=False),

        # Múltiples variables de respuesta según el diccionario CE
        sa.Column('chk1', sa.String(length=5), nullable=True),
        sa.Column('chk2', sa.String(length=5), nullable=True),
        sa.Column('chk3', sa.String(length=5), nullable=True),
        sa.Column('chk4', sa.String(length=5), nullable=True),
        sa.Column('chk5', sa.String(length=10), nullable=True),
        sa.Column('d01', sa.String(length=10), nullable=True),
        sa.Column('d02', sa.String(length=10), nullable=True),
        sa.Column('d03', sa.String(length=10), nullable=True),
        sa.Column('d04', sa.String(length=10), nullable=True),

        sa.ForeignKeyConstraint(
            ['tipdato', 'cuadro_codigo'],
            ['cuadro_tipdato.tipdato', 'cuadro_tipdato.cuadro_codigo'],
            name='fk_fgestion_cuadro_tipdato'
        )
    )


def downgrade():
    op.drop_table('fgestion')
    # No eliminamos los registros insertados en cuadro_tipdato en el downgrade por seguridad.
