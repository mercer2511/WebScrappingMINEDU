"""crear_caracteristica_y_sellar_padron

Revision ID: c2541308bd27
Revises: 71c11294a538
Create Date: 2026-05-17 01:32:00.427385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2541308bd27'
down_revision: Union[str, Sequence[str], None] = '71c11294a538'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================================================
    # 1. CREAR TABLA CARACTERÍSTICA IE Y POBLARLA
    # =========================================================
    op.create_table(
        'caracteristica_ie',
        sa.Column('codigo', sa.String(length=1), primary_key=True),
        sa.Column('descripcion', sa.String(length=50), nullable=False)
    )

    op.execute("""
               INSERT INTO caracteristica_ie (codigo, descripcion)
               VALUES ('1', 'Unidocente multigrado'),
                      ('2', 'Polidocente multigrado'),
                      ('3', 'Polidocente completo'),
                      ('a', 'No aplica');
               """)

    # =========================================================
    # 2. LIMPIEZA PRE-CANDADO (Prevenir el error del string vacío)
    # =========================================================
    op.execute("""
               UPDATE padron_ie
               SET tipoprog_codigo = NULL
               WHERE tipoprog_codigo = '';
               """)

    # =========================================================
    # 3. CREAR LAS LLAVES FORÁNEAS (CANDADOS FINALES)
    # =========================================================
    # Candado para Característica
    op.create_foreign_key(
        'fk_padron_caracteristica', 'padron_ie', 'caracteristica_ie',
        ['cod_car'], ['codigo']
    )

    # Candado para Tipo de Programa
    op.create_foreign_key(
        'fk_padron_tipoprog', 'padron_ie', 'tipo_programa',
        ['tipoprog_codigo'], ['codigo']
    )


def downgrade():
    op.drop_constraint('fk_padron_tipoprog', 'padron_ie', type_='foreignkey')
    op.drop_constraint('fk_padron_caracteristica', 'padron_ie', type_='foreignkey')
    op.drop_table('caracteristica_ie')
