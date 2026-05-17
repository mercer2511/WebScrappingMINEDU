"""agregar_tipdatos_docentes

Revision ID: 8ff6b283f057
Revises: d036099a3ef2
Create Date: 2026-05-16 15:49:54.869339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ff6b283f057'
down_revision: Union[str, Sequence[str], None] = 'd036099a3ef2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    datos = [
        # C301 - Fuente de financiamiento
        ("C301", "01", "Sector Educación"),
        ("C301", "02", "Otro sector público (FF.AA., salud u otro)"),
        ("C301", "03", "Municipalidad"),
        ("C301", "04", "Gobierno Regional"),
        ("C301", "05", "APAFA"),
        ("C301", "06", "Otra fuente Privada"),
        # C302 - Jornada laboral
        ("C302", "01", "Gestión Pública - 40 horas"),
        ("C302", "02", "Gestión Pública - 30 horas"),
        ("C302", "03", "Gestión Pública - 24 horas"),
        ("C302", "04", "Gestión Pública - 20 horas"),
        ("C302", "05", "Gestión Pública - Menos 20 horas"),
        ("C302", "06", "Gestión Privada"),
        # C303 - Género
        ("C303", "01", "Hombre"),
        ("C303", "02", "Mujer"),
        # C304 - Condición laboral
        ("C304", "01", "Nombrado"),
        ("C304", "02", "Contratado"),
        # C305 - Máximo nivel educativo alcanzado
        ("C305", "01", "Total Estudios Pedagógicos"),
        ("C305", "02", "Estudios Pedagógicos Concluidos con título"),
        ("C305", "03", "Estudios Pedagógicos Concluidos sin título"),
        ("C305", "04", "Estudios Pedagógicos No concluidos"),
        ("C305", "05", "Total Estudios No Pedagógicos"),
        ("C305", "06", "Estudios No Pedagógicos Concluidos con título"),
        ("C305", "07", "Estudios No Pedagógicos Concluidos sin título"),
        ("C305", "08", "Estudios No Pedagógicos No concluidos"),
        ("C305", "09", "Secundaria"),
        ("C305", "10", "Primaria"),
        # C306 - Estudios de postgrado en pedagogía
        ("C306", "01", "Maestría concluida con grado"),
        ("C306", "02", "Maestría concluida sin grado"),
        ("C306", "03", "Maestría en proceso"),
        ("C306", "04", "Doctorado concluida con grado"),
        ("C306", "05", "Doctorado concluida sin grado"),
        ("C306", "06", "Doctorado en proceso"),
        ("C306", "07", "Sin Postgrado"),
        # C307 - Escala magisterial
        ("C307", "01", "Primera"),
        ("C307", "02", "Segunda"),
        ("C307", "03", "Tercera"),
        ("C307", "04", "Cuarta"),
        ("C307", "05", "Quinta"),
        ("C307", "06", "Sexta"),
        ("C307", "07", "Séptima"),
        ("C307", "08", "Octava"),
        ("C307", "09", "Sin Escala Magisterial"),
        # C308 - Situación en el cargo directivo
        ("C308", "01", "Titular ratificado por evaluación excepcional 2014"),
        ("C308", "02", "Titular designado por evaluación de acceso 2015"),
        ("C308", "03", "Titular otro"),
        ("C308", "04", "Encargado por función, sin documento formal de la encargatura"),
        ("C308", "05", "Encargado"),
        # C309 - Especialidad del título pedagógico optado
        ("C309", "01", "Educación Inicial"),
        ("C309", "02", "Educación Primaria"),
        ("C309", "03", "E.I. Intercultural Bilingüe"),
        ("C309", "04", "E.P. Intercultural Bilingüe"),
        ("C309", "05", "Educación Básica Alternativa"),
        ("C309", "06", "Educación Especial"),
        ("C309", "07", "Educación Física"),
        ("C309", "08", "Educación Artística"),
        ("C309", "09", "E.S. Lengua y Literatura"),
        ("C309", "10", "E.S. Comunicación"),
        ("C309", "11", "E.S. Matemática y Física"),
        ("C309", "12", "E.S. Matemática"),
        ("C309", "13", "E.S. CCSS y Filosofía"),
        ("C309", "14", "E.S. Ciencias Sociales"),
        ("C309", "15", "E.S. Ciencias Naturales"),
        ("C309", "16", "E.S. Ciencia Tecnología y Ambiente"),
        ("C309", "17", "E.S. Alimentación y Nutrición"),
        ("C309", "18", "E.S. Biología y Química"),
        ("C309", "19", "E.S. Historia y Geografía"),
        ("C309", "20", "E.S. CC.HH. Sociales"),
        ("C309", "21", "E.S. Idioma Inglés"),
        ("C309", "22", "Educación Religiosa"),
        ("C309", "23", "E.S. Educación Familiar"),
        ("C309", "24", "E.T. Artes Industriales"),
        ("C309", "25", "E.T. Artesanía"),
        ("C309", "26", "E.T. Agropecuaria"),
        ("C309", "27", "E.T. Construcción en madera"),
        ("C309", "28", "E.T. Computación e Informática"),
        ("C309", "29", "E.T. Carpintería/Ebanistería"),
        ("C309", "30", "E.T. Electricidad"),
        ("C309", "31", "E.T. Electrónica"),
        ("C309", "32", "E.T. Ebanistería"),
        ("C309", "33", "E.T. Industria del Vestido"),
        ("C309", "34", "E.T. Industria del Vestido Alimentación y Alta Costura"),
        ("C309", "35", "E.T. en Industria del Vestido y Alta Costura"),
        ("C309", "36", "E.T.Técnica Esp. Ind. del Vestido Ind. Alimentaria y Artes"),
        ("C309", "37", "E.T. Industria Alimentaria"),
        ("C309", "38", "E.T. Mecánica Automotriz"),
        ("C309", "39", "E.T. Mecánica de Producción"),
        ("C309", "40", "E.T. Mecánica de Producción y Soldadura"),
        ("C309", "41", "E.T. Textilería"),
        ("C309", "42", "Otra pedagógica"),
        # C310 - Modalidad de contrato
        ("C310", "01", "Contrato Público - A plazo fijo D. Leg. 728"),
        ("C310", "02", "Contrato Público - Locación de Serv. / Honorarios"),
        ("C310", "03", "Contrato Público - CAS - D. Leg. 1057"),
        ("C310", "04", "Contrato Público - Contrato D. Leg. 276"),
        ("C310", "05", "Contrato Público - Contrato Ley 30328"),
        ("C310", "06", "Contrato Público - Contrato Ley 30512"),
        ("C310", "07", "Contrato Público - Otra modalidad"),
        ("C310", "08", "Contrato Privado - A plazo indefinido (Permanente)"),
        ("C310", "09", "Contrato Privado - Plazo fijo (Tiempo determinado)"),
        ("C310", "10", "Contrato Privado - A tiempo parcial (por horas)"),
        ("C310", "11", "Contrato Privado - Locación de Serv. / Honorarios"),
        ("C310", "12", "Contrato Privado - Otra modalidad"),
        # C311 - Rango de edad en años cumplidos
        ("C311", "01", "de 20 y menos años"),
        ("C311", "02", "21 - 25 años"),
        ("C311", "03", "26 - 30 años"),
        ("C311", "04", "31 - 35 años"),
        ("C311", "05", "36 - 40 años"),
        ("C311", "06", "41 - 45 años"),
        ("C311", "07", "46 - 50 años"),
        ("C311", "08", "51 - 55 años"),
        ("C311", "09", "56 - 60 años"),
        ("C311", "10", "61 - 65 años"),
        ("C311", "11", "66 - 70 años"),
        ("C311", "12", "de 71 años a más"),
        # C312 - Rango de tiempo de servicio en años (nombrados)
        ("C312", "01", "00 - 05 años"),
        ("C312", "02", "06 - 10 años"),
        ("C312", "03", "11 - 15 años"),
        ("C312", "04", "16 - 20 años"),
        ("C312", "05", "21 - 25 años"),
        ("C312", "06", "26 - 30 años"),
        ("C312", "07", "31 - 35 años"),
        ("C312", "08", "36 - 40 años"),
        ("C312", "09", "de 41 años a más"),
        # C313 - Rango de tiempo de experiencia laboral en años
        ("C313", "01", "00 - 05 años"),
        ("C313", "02", "06 - 10 años"),
        ("C313", "03", "11 - 15 años"),
        ("C313", "04", "16 - 20 años"),
        ("C313", "05", "21 - 25 años"),
        ("C313", "06", "26 - 30 años"),
        ("C313", "07", "31 - 35 años"),
        ("C313", "08", "36 - 40 años"),
        ("C313", "09", "de 41 años a más"),
        # C314 - Conocimiento en inglés
        ("C314", "01", "No Sabe"),
        ("C314", "02", "Sólo Habla"),
        ("C314", "03", "Sólo Lee"),
        ("C314", "04", "Sólo Escribe"),
        ("C314", "05", "Habla, Lee y Escribe"),
        ("C314", "06", "Habla y Lee"),
        ("C314", "07", "Habla y Escribe"),
        ("C314", "08", "Lee y Escribe"),
        # C315 - Certificación en inglés
        ("C315", "01", "No tiene"),
        ("C315", "02", "Si Tiene - Nacional"),
        ("C315", "03", "Si Tiene - Internacional"),
        ("C315", "04", "Si Tiene - Nacional e Internacional"),
        # C316 - Tipo de institución donde estudió
        ("C316", "01", "Universidad Pública"),
        ("C316", "02", "Universidad Privada"),
        ("C316", "03", "Instituto de Educación Superior Pedagógico Público"),
        ("C316", "04", "Instituto de Educación Superior Pedagógico Privado"),
        ("C316", "05", "Sin Formación Pedagógica"),
        # C317 - Atención a estudiantes con NEE asociadas a discapacidad
        ("C317", "01", "¿Atiende a estudiantes con NEE asociadas a discapacidad? - SI"),
        ("C317", "02", "¿Atiende a estudiantes con NEE asociadas a discapacidad? - NO"),
        # C318 - Tipo de discapacidad (docentes)
        ("C318", "01", "Discapacidad - Auditiva"),
        ("C318", "02", "Discapacidad - Visual"),
        ("C318", "03", "Discapacidad - Física o Motora"),
        ("C318", "04", "Discapacidad - Otro tipo"),
        ("C318", "05", "Ninguna discapacidad"),
        # C319 - Lengua originaria que domina
        ("C319", "01", "Achuar"),
        ("C319", "02", "Aimara"),
        ("C319", "03", "Amahuaca"),
        ("C319", "04", "Arabela"),
        ("C319", "05", "Asháninka"),
        ("C319", "06", "Asheninka"),
        ("C319", "07", "Awajún"),
        ("C319", "08", "Bora"),
        ("C319", "09", "Kapanawa"),
        ("C319", "10", "Cashinahua"),
        ("C319", "11", "Kawki"),
        ("C319", "12", "Chamikuro"),
        ("C319", "13", "Ese eja"),
        ("C319", "14", "Harakbut"),
        ("C319", "15", "Iñapari"),
        ("C319", "16", "Ikuitu"),
        ("C319", "17", "Iskonawa"),
        ("C319", "18", "Jaqaru"),
        ("C319", "19", "Kakataibo"),
        ("C319", "20", "Kakinte (caquinte)"),
        ("C319", "21", "Kandozi (Chapra)"),
        ("C319", "22", "Kandozi (Kandozi)"),
        ("C319", "23", "Kukama-kukamiria"),
        ("C319", "24", "Madija (culina)"),
        ("C319", "25", "Maijiki"),
        ("C319", "26", "Matsés"),
        ("C319", "27", "Matsigenka"),
        ("C319", "28", "Munichi"),
        ("C319", "29", "Murui-muinani"),
        ("C319", "30", "Matsigenka-montetokunirira"),
        ("C319", "31", "Nomatsigenga"),
        ("C319", "32", "Ocaina"),
        ("C319", "33", "Omagua"),
        ("C319", "34", "Quechua amazónico (Kichwa)"),
        ("C319", "35", "Quechua central (Ancash)"),
        ("C319", "36", "Quechua central (Huánuco)"),
        ("C319", "37", "Quechua central (Wanka)"),
        ("C319", "38", "Quechua central (Pasco)"),
        ("C319", "39", "Quechua norteño (Cajamarca)"),
        ("C319", "40", "Quechua norteño (Inkawasi Kañaris)"),
        ("C319", "41", "Quechua sureño (Chanka)"),
        ("C319", "42", "Quechua sureño (Collao)"),
        ("C319", "43", "Resígaro"),
        ("C319", "44", "Secoya"),
        ("C319", "45", "Sharanahua"),
        ("C319", "46", "Shawi"),
        ("C319", "47", "Shipibo-Konibo"),
        ("C319", "48", "Shiwilu"),
        ("C319", "49", "Taushiro"),
        ("C319", "50", "Ticuna"),
        ("C319", "51", "Urarina"),
        ("C319", "52", "Wampis"),
        ("C319", "53", "Yagua"),
        ("C319", "54", "Yaminahua"),
        ("C319", "55", "Yanesha"),
        ("C319", "56", "Yine"),
        ("C319", "57", "Nahua"),
        ("C319", "58", "Otra lengua originaria"),
        # C320 - Conocimiento de la lengua originaria que domina
        ("C320", "01", "Sólo Habla"),
        ("C320", "02", "Sólo Lee"),
        ("C320", "03", "Sólo Escribe"),
        ("C320", "04", "Habla, Lee y Escribe"),
        ("C320", "05", "Habla y Lee"),
        ("C320", "06", "Habla y Escribe"),
        ("C320", "07", "Lee y Escribe"),
        # C321 - Situación atravesada con respecto a la lengua originaria que domina
        ("C321", "01", "¿Cuenta con estudios de Educación Intercultural Bilingüe? - SI"),
        ("C321", "02", "¿Cuenta con estudios de Educación Intercultural Bilingüe? - NO"),
        ("C321", "03", "¿Ha recibido capacitación en EIB? - SI"),
        ("C321", "04", "¿Ha recibido capacitación en EIB? - NO"),
        ("C321", "05", "¿El docente enseña en lengua originaria? - SI"),
        ("C321", "06", "¿El docente enseña en lengua originaria? - NO"),
        ("C321", "07", "¿El material recibido coincide con la lengua originaria que enseña? - SI"),
        ("C321", "08", "¿El material recibido coincide con la lengua originaria que enseña? - NO"),
        ("C321", "09", "En la actualidad el Docente, ¿se encuentra en el registro de Docentes Bilingües? - SI"),
        ("C321", "10", "En la actualidad el Docente, ¿se encuentra en el registro de Docentes Bilingües? - NO"),
        # C322 - Tipo de estudios en EIB
        ("C322", "01", "Doctorado"),
        ("C322", "02", "Maestría"),
        ("C322", "03", "Segunda especialidad"),
        ("C322", "04", "Especialización"),
        ("C322", "05", "Actualización"),
        ("C322", "06", "Otro"),
        # C323 - Pregunta específica
        ("C323", "01", "¿Ha recibido asistencia y orientación para la atención educativa de estudiantes con discapacidad del equipo SAEV? - SI"),
        ("C323", "02", "¿Ha recibido asistencia y orientación para la atención educativa de estudiantes con discapacidad del equipo SAEV? - NO"),
        # C324 - Condición laboral (personal administrativo y de servicio)
        ("C324", "01", "Nombrado"),
        ("C324", "02", "Contratado"),
    ]

    valores = ", ".join([f"('{c}', '{t}', '{d}')" for c, t, d in datos])
    op.execute(
        sa.text(
            f"INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion) "
            f"VALUES {valores} ON CONFLICT (cuadro_codigo, tipdato) DO NOTHING"
        )
    )

def downgrade():
    # No es necesario borrar; con deshacer la migración anterior se limpia
    pass
