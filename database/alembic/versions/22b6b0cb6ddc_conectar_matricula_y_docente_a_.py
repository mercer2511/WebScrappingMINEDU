"""conectar_matricula_y_docente_a_diccionarios

Revision ID: 22b6b0cb6ddc
Revises: 7fc3f3740ae4
Create Date: 2026-05-17 11:39:12.172426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22b6b0cb6ddc'
down_revision: Union[str, Sequence[str], None] = '7fc3f3740ae4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # =========================================================
    # 1. CANDADOS PARA LA TABLA MATRICULA
    # =========================================================
    # Conexión a Cédula
    op.create_foreign_key('fk_matricula_cedula', 'matricula', 'cedula', ['nroced'], ['codigo'])
    # Conexión a Cuadro
    op.create_foreign_key('fk_matricula_cuadro', 'matricula', 'cuadro', ['cuadro'], ['codigo'])
    # CONEXIÓN COMPUESTA A CUADRO_TIPDATO (Candado doble)
    op.create_foreign_key(
        'fk_matricula_cuadro_tipdato', 'matricula', 'cuadro_tipdato',
        ['cuadro', 'tipdato'], ['cuadro_codigo', 'tipdato']
    )

    # =========================================================
    # 2. CANDADOS PARA LA TABLA DOCENTE
    # =========================================================
    # Conexión a Cédula
    op.create_foreign_key('fk_docente_cedula', 'docente', 'cedula', ['nroced'], ['codigo'])
    # Conexión a Cuadro
    op.create_foreign_key('fk_docente_cuadro', 'docente', 'cuadro', ['cuadro'], ['codigo'])
    # CONEXIÓN COMPUESTA A CUADRO_TIPDATO (Candado doble)
    op.create_foreign_key(
        'fk_docente_cuadro_tipdato', 'docente', 'cuadro_tipdato',
        ['cuadro', 'tipdato'], ['cuadro_codigo', 'tipdato']
    )


def downgrade():
    # Retirar candados de docente
    op.drop_constraint('fk_docente_cuadro_tipdato', 'docente', type_='foreignkey')
    op.drop_constraint('fk_docente_cuadro', 'docente', type_='foreignkey')
    op.drop_constraint('fk_docente_cedula', 'docente', type_='foreignkey')

    # Retirar candados de matricula
    op.drop_constraint('fk_matricula_cuadro_tipdato', 'matricula', type_='foreignkey')
    op.drop_constraint('fk_matricula_cuadro', 'matricula', type_='foreignkey')
    op.drop_constraint('fk_matricula_cedula', 'matricula', type_='foreignkey')
