"""crear_tabla_maestra_padron_ie

Revision ID: 4c05aec392ee
Revises: 05104c79d114
Create Date: 2026-05-16 19:07:16.772084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c05aec392ee'
down_revision: Union[str, Sequence[str], None] = '05104c79d114'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'padron_ie',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('cod_mod', sa.String(length=7), nullable=False),
        sa.Column('anexo', sa.String(length=1), nullable=False, server_default='0'),
        sa.Column('codlocal', sa.String(length=6), nullable=True),
        sa.Column('cen_edu', sa.String(length=150), nullable=True),

        # --- Identificadores y Características ---
        sa.Column('niv_mod_codigo', sa.String(length=2), nullable=True),
        sa.Column('cod_car', sa.String(length=1), nullable=True),  # Unidocente, Polidocente
        sa.Column('forma_codigo', sa.String(length=1), nullable=True),
        sa.Column('tipoprog_codigo', sa.String(length=2), nullable=True),
        sa.Column('gestion_codigo', sa.String(length=1), nullable=True),
        sa.Column('dependencia_codigo', sa.String(length=2), nullable=True),
        sa.Column('tipsexo_codigo', sa.String(length=1), nullable=True),
        sa.Column('cod_tur_codigo', sa.String(length=2), nullable=True),

        # --- Contacto y Director ---
        sa.Column('director', sa.String(length=150), nullable=True),
        sa.Column('telefono', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('pagweb', sa.String(length=150), nullable=True),

        # --- Localización Geográfica / Administrativa ---
        sa.Column('direccion', sa.String(length=250), nullable=True),
        sa.Column('localidad', sa.String(length=100), nullable=True),
        sa.Column('referencia', sa.String(length=250), nullable=True),
        sa.Column('codgeo', sa.String(length=6), nullable=True),  # Ubigeo
        sa.Column('codooii', sa.String(length=6), nullable=True),
        sa.Column('dre_ugel', sa.String(length=100), nullable=True),
        sa.Column('region_edu', sa.String(length=100), nullable=True),
        sa.Column('codcp_inei', sa.String(length=15), nullable=True),
        sa.Column('codcp_med', sa.String(length=10), nullable=True),
        sa.Column('cen_pob', sa.String(length=150), nullable=True),

        # --- Variables Censales ---
        sa.Column('area_censo_codigo', sa.String(length=1), nullable=True),
        sa.Column('dis_vraem_codigo', sa.String(length=1), nullable=True),
        sa.Column('dis_front_codigo', sa.String(length=1), nullable=True),
        sa.Column('region_nat', sa.String(length=15), nullable=True),

        # --- Coordenadas Georreferenciales ---
        sa.Column('nlat_ie', sa.Numeric(precision=12, scale=6), nullable=True),
        sa.Column('nlong_ie', sa.Numeric(precision=12, scale=6), nullable=True),
        sa.Column('altitud', sa.Numeric(precision=12, scale=6), nullable=True),

        # --- Metadatos ---
        sa.Column('imputado_codigo', sa.String(length=1), nullable=True),

        # =========================================================
        # RESTRICCIONES Y LLAVES FORÁNEAS
        # =========================================================

        # Restricción Única (Un Padrón no puede tener el mismo cod_mod y anexo duplicado)
        sa.UniqueConstraint('cod_mod', 'anexo', name='uq_padron_cod_mod_anexo'),

        # Llaves foráneas verificadas
        sa.ForeignKeyConstraint(['niv_mod_codigo'], ['nivel_modalidad.codigo'], name='fk_padron_niv_mod'),
        sa.ForeignKeyConstraint(['gestion_codigo'], ['gestion.codigo'], name='fk_padron_gestion'),
        sa.ForeignKeyConstraint(['dependencia_codigo'], ['dependencia.codigo'], name='fk_padron_dependencia'),
        sa.ForeignKeyConstraint(['area_censo_codigo'], ['area_censo.codigo'], name='fk_padron_area_censo')
    )

    # Índices para acelerar las búsquedas (vital para la generación sintética)
    op.create_index('ix_padron_cod_mod', 'padron_ie', ['cod_mod'])
    op.create_index('ix_padron_codgeo', 'padron_ie', ['codgeo'])
    op.create_index('ix_padron_codooii', 'padron_ie', ['codooii'])


def downgrade():
    op.drop_index('ix_padron_codooii', table_name='padron_ie')
    op.drop_index('ix_padron_codgeo', table_name='padron_ie')
    op.drop_index('ix_padron_cod_mod', table_name='padron_ie')
    op.drop_table('padron_ie')
