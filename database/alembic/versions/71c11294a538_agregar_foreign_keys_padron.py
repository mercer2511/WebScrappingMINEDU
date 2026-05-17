"""agregar_foreign_keys_padron

Revision ID: 71c11294a538
Revises: 88583c88b508
Create Date: 2026-05-17 01:20:04.114044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '71c11294a538'
down_revision: Union[str, Sequence[str], None] = '88583c88b508'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Candado para Ubigeo
    op.create_foreign_key('fk_padron_ubigeo', 'padron_ie', 'ubigeo', ['codgeo'], ['codgeo'])

    # Candado para Turnos
    op.create_foreign_key('fk_padron_turno', 'padron_ie', 'codigo_turno', ['cod_tur_codigo'], ['codigo'])

    # Candado para Tipo de Sexo
    op.create_foreign_key('fk_padron_sexo', 'padron_ie', 'tipo_sexo', ['tipsexo_codigo'], ['codigo'])

    # Candado para Forma de Atención
    op.create_foreign_key('fk_padron_forma', 'padron_ie', 'forma_atencion', ['forma_codigo'], ['codigo'])


def downgrade():
    op.drop_constraint('fk_padron_forma', 'padron_ie', type_='foreignkey')
    op.drop_constraint('fk_padron_sexo', 'padron_ie', type_='foreignkey')
    op.drop_constraint('fk_padron_turno', 'padron_ie', type_='foreignkey')
    op.drop_constraint('fk_padron_ubigeo', 'padron_ie', type_='foreignkey')
