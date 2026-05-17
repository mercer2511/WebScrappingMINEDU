"""agregar_tipdatos_locales_materiales

Revision ID: a0dc74ebf80a
Revises: 968211b6d5f3
Create Date: 2026-05-16 16:16:17.965392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0dc74ebf80a'
down_revision: Union[str, Sequence[str], None] = '968211b6d5f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    datos = [
        # ===== C302 - Cerco Perimétrico =====
        # Tipo de Lindero (Tabla 01)
        ("C302", "LINDERO_01", "Frente"),
        ("C302", "LINDERO_02", "Derecho"),
        ("C302", "LINDERO_03", "Fondo"),
        ("C302", "LINDERO_04", "Izquierdo"),
        # Material predominante del tramo (Tabla 02)
        ("C302", "MATERIAL_TRAMO_01", "Ladrillo/Similar/Bloque de cemento"),
        ("C302", "MATERIAL_TRAMO_02", "Adobe/Tapia/Quincha/Piedra con barro"),
        ("C302", "MATERIAL_TRAMO_03", "Piedra en bloque"),
        ("C302", "MATERIAL_TRAMO_04", "Madera"),
        ("C302", "MATERIAL_TRAMO_05", "Alambre"),
        ("C302", "MATERIAL_TRAMO_06", "Malla metálica"),
        ("C302", "MATERIAL_TRAMO_07", "Cerco prefabricado"),
        ("C302", "MATERIAL_TRAMO_08", "Estera"),
        ("C302", "MATERIAL_TRAMO_09", "Drywall"),
        ("C302", "MATERIAL_TRAMO_10", "Calaminas"),
        ("C302", "MATERIAL_TRAMO_11", "Cerco vivo"),
        # Estado de conservación del tramo (Tabla 03 - Numeral 7)
        ("C302", "ESTADO_TRAMO_01", "Sin daño"),
        ("C302", "ESTADO_TRAMO_02", "Fisuras leves"),
        ("C302", "ESTADO_TRAMO_03", "Fisuras moderadas o ataques de sales"),
        ("C302", "ESTADO_TRAMO_04", "Agrietamiento o colapso"),
        # Entidad Ejecutora (Tabla 04)
        ("C302", "ENTIDAD_01", "Gobierno Nacional"),
        ("C302", "ENTIDAD_02", "Gobierno Regional"),
        ("C302", "ENTIDAD_03", "APAFA"),
        ("C302", "ENTIDAD_04", "Entidades Cooperantes"),
        ("C302", "ENTIDAD_05", "Empresa Privada"),
        ("C302", "ENTIDAD_06", "Otro"),
        # Tipo de Acceso en el Tramo (Tabla 05)
        ("C302", "ACCESO_01", "Acceso plano"),
        ("C302", "ACCESO_02", "Sólo escalera y rampa"),
        ("C302", "ACCESO_03", "Sólo rampa (con una pequeña inclinación)"),
        # Estructura de portada de ingreso (Tabla 06)
        ("C302", "PORTADA_01", "Concreto armado"),
        ("C302", "PORTADA_02", "Metálico"),
        ("C302", "PORTADA_03", "Concreto Simple"),
        ("C302", "PORTADA_04", "Madera"),
        ("C302", "PORTADA_05", "Piedra"),
        ("C302", "PORTADA_06", "Otro"),
        # Material del Portón (Tabla 07)
        ("C302", "MATERIAL_PORTON_01", "Madera"),
        ("C302", "MATERIAL_PORTON_02", "Mallas Metálicas"),
        ("C302", "MATERIAL_PORTON_03", "Rejas Metálicas"),
        ("C302", "MATERIAL_PORTON_04", "Planchas Metálicas"),
        ("C302", "MATERIAL_PORTON_05", "Drywall"),
        ("C302", "MATERIAL_PORTON_06", "Otro"),
        # Estado de conservación del portón (Tabla 03 - Numeral 15)
        ("C302", "ESTADO_PORTON_01", "Buen estado"),
        ("C302", "ESTADO_PORTON_02", "Regular estado"),
        ("C302", "ESTADO_PORTON_03", "Mal estado"),
        # Sistema Estructural del Muro de Contención (Tabla 08)
        ("C302", "MURO_01", "Concreto reforzado"),
        ("C302", "MURO_02", "Concreto Simple"),
        ("C302", "MURO_03", "Concreto Ciclópeo"),
        ("C302", "MURO_04", "Concreto Ciclópeo con columnas de refuerzo"),
        ("C302", "MURO_05", "Mampostería o bloques de roca pegados con concreto"),
        ("C302", "MURO_06", "Muros de gravedad flexible (gaviones, prefabricados, etc.)"),
        ("C302", "MURO_07", "Otro"),

        # ===== C303 - Otros Elementos =====
        ("C303", "1", "Tanque Elevado"),
        ("C303", "2", "Tanque Cisterna"),
        ("C303", "3", "Bomba Sumergible"),
        ("C303", "4", "Tanque Séptico"),
        ("C303", "5", "Tanque Séptico Mejorado"),
        ("C303", "6", "Pararrayos"),
        ("C303", "7", "Sistemas de Paneles Solares"),
        ("C303", "8", "Pozos a Tierra"),
        ("C303", "9", "Cámaras de Videovigilancia"),
        ("C303", "10", "Monitores de Videovigilancia"),
        ("C303", "11", "Grupo Electrógeno"),

        # ===== C401 - Edificaciones =====
        # Finalidad del uso del módulo prefabricado (Tabla 01)
        ("C401", "FINALIDAD_01", "Emergencia (ante desastres)"),
        ("C401", "FINALIDAD_02", "Temporal (durante la ejecución de una inversión)"),
        ("C401", "FINALIDAD_03", "Permanentes"),
        # Tipo de Entidad Ejecutora (Tabla 02)
        ("C401", "ENTIDAD_01", "Gobierno Nacional / Proyecto Especial"),
        ("C401", "ENTIDAD_02", "Gobierno Regional / Local"),
        ("C401", "ENTIDAD_03", "APAFA / Autoconstrucción"),
        ("C401", "ENTIDAD_04", "Entidades Cooperantes / ONGs"),
        ("C401", "ENTIDAD_05", "Empresa Privada"),
        ("C401", "ENTIDAD_06", "No Especifica"),
        # Sistema Estructural Predominante (Tabla 03)
        ("C401", "SISTEMA_01", "Concreto armado – Tipo dual"),
        ("C401", "SISTEMA_02", "Concreto armado – Tipo aporticado"),
        ("C401", "SISTEMA_03", "Albañilería confinada"),
        ("C401", "SISTEMA_04", "Albañilería sin confinar"),
        ("C401", "SISTEMA_05", "Adobe / Tapial"),
        ("C401", "SISTEMA_06", "Madera Estructural"),
        ("C401", "SISTEMA_07", "Acero Estructural"),
        ("C401", "SISTEMA_08", "Módulo prefabricado - PRONIED"),
        ("C401", "SISTEMA_09", "Módulo prefabricado - Otro"),
        ("C401", "SISTEMA_10", "Precario"),
        ("C401", "SISTEMA_11", "Otro"),
        ("C401", "SISTEMA_12", "No Tiene pero lo Requiere"),
        ("C401", "SISTEMA_13", "No Tiene pero No lo Requiere"),
        # Estado de Conservación (Tabla 04)
        ("C401", "ESTADO_01", "Buen Estado"),
        ("C401", "ESTADO_02", "Regular Estado"),
        ("C401", "ESTADO_03", "Mal Estado"),
        ("C401", "ESTADO_04", "No Aplica"),
        # Material predominante de la Cobertura de los Techos (Tabla 05)
        ("C401", "COBERTURA_01", "Concreto"),
        ("C401", "COBERTURA_02", "Madera"),
        ("C401", "COBERTURA_03", "Teja"),
        ("C401", "COBERTURA_04", "Fibra de cemento"),
        ("C401", "COBERTURA_05", "Calamina"),
        ("C401", "COBERTURA_06", "Calaminón"),
        ("C401", "COBERTURA_07", "Caña con barro"),
        ("C401", "COBERTURA_08", "Lata o latón"),
        ("C401", "COBERTURA_09", "Otro"),
        ("C401", "COBERTURA_10", "No Tiene pero lo Requiere"),
        ("C401", "COBERTURA_11", "No Tiene pero No lo Requiere"),
        # Tipo de Conexión Interna en un mismo piso (Tabla 06)
        ("C401", "CONEXION_01", "Directo sin desnivel"),
        ("C401", "CONEXION_02", "Gradas"),
        ("C401", "CONEXION_03", "Rampas"),
        ("C401", "CONEXION_04", "Otros"),
        # Tipo de Instalación de Cableado (Tabla 07)
        ("C401", "CABLEADO_01", "Circuito canalizado"),
        ("C401", "CABLEADO_02", "Circuito sin canalizar o sin conductor adecuado"),
        ("C401", "CABLEADO_03", "No especifica"),

        # ===== C501 - Aulas =====
        # Niveles Educativos (Tabla 01)
        ("C501", "NIV_A1", "Inicial Cuna"),
        ("C501", "NIV_A2", "Inicial Jardín"),
        ("C501", "NIV_A3", "Inicial Cuna Jardín"),
        ("C501", "NIV_B0", "Primaria"),
        ("C501", "NIV_F0", "Secundaria"),
        ("C501", "NIV_D1", "EBA – Inicial e Intermedio"),
        ("C501", "NIV_D2", "EBA - Avanzado"),
        ("C501", "NIV_E0", "Programa de Intervención temprana (PRITE)"),
        ("C501", "NIV_E1", "Inicial – Educación Básico Especial (EBE)"),
        ("C501", "NIV_E2", "Primaria – Educación Básico Especial (EBE)"),
        ("C501", "NIV_L0", "Centro de Educación Técnico Productiva (CETPRO)"),
        ("C501", "NIV_K0", "Instituto de Educación Superior Pedagógico"),
        ("C501", "NIV_T0", "Instituto de Educación Superior Tecnológico"),
        ("C501", "NIV_M0", "Escuela Superior de Formación Artística"),
        ("C501", "NIV_P0", "Escuela de Educación Superior Pedagógica"),
        ("C501", "NIV_S0", "Escuela de Educación Superior Tecnológica"),
        # Material predominante de puertas (Tabla 02)
        ("C501", "PUERTA_01", "Madera"),
        ("C501", "PUERTA_02", "Mallas metálicas"),
        ("C501", "PUERTA_03", "Rejas metálicas"),
        ("C501", "PUERTA_04", "Planchas metálicas"),
        ("C501", "PUERTA_05", "Drywall"),
        ("C501", "PUERTA_06", "Vidrio"),
        ("C501", "PUERTA_07", "Otro"),
        ("C501", "PUERTA_08", "No Tiene pero lo Requiere"),
        ("C501", "PUERTA_09", "No Tiene pero No lo Requiere"),
        # Material predominante del marco de la ventana (Tabla 03)
        ("C501", "VENTANA_01", "Carpintería metálica (fierro, acero, aluminio, etc.)"),
        ("C501", "VENTANA_02", "Carpintería de madera"),
        ("C501", "VENTANA_03", "Carpintería de PVC"),
        ("C501", "VENTANA_04", "Carpintería mixta (varios materiales)"),
        ("C501", "VENTANA_05", "Otro"),
        ("C501", "VENTANA_06", "No Tiene pero lo Requiere"),
        ("C501", "VENTANA_07", "No Tiene pero No lo Requiere"),
        # Material predominante de paredes (Tabla 04)
        ("C501", "PARED_01", "Ladrillo o concreto"),
        ("C501", "PARED_02", "Adobe o tapial"),
        ("C501", "PARED_03", "Quincha"),
        ("C501", "PARED_04", "Piedra con barro, cal o cemento"),
        ("C501", "PARED_05", "Madera"),
        ("C501", "PARED_06", "Triplay"),
        ("C501", "PARED_07", "Eternit o fibra de concreto"),
        ("C501", "PARED_08", "Estera, cartón o plástico"),
        ("C501", "PARED_09", "Otro"),
        # Material predominante de techos (Tabla 05)
        ("C501", "TECHO_01", "Concreto armado"),
        ("C501", "TECHO_02", "Madera"),
        ("C501", "TECHO_03", "Teja"),
        ("C501", "TECHO_04", "Fibra de cemento"),
        ("C501", "TECHO_05", "Calamina"),
        ("C501", "TECHO_06", "Calaminón"),
        ("C501", "TECHO_07", "Eternit"),
        ("C501", "TECHO_08", "Caña con barro"),
        ("C501", "TECHO_09", "Lata o latón"),
        ("C501", "TECHO_10", "Otro"),
        # Material predominante de pisos (Tabla 06)
        ("C501", "PISO_01", "Parquet o madera pulida"),
        ("C501", "PISO_02", "Vinílico, pisopak o similar"),
        ("C501", "PISO_03", "Loseta, cerámico o similar"),
        ("C501", "PISO_04", "Cemento"),
        ("C501", "PISO_05", "Madera entablada"),
        ("C501", "PISO_06", "Tierra"),
        ("C501", "PISO_07", "Otro"),
        # Estado de conservación (Tabla 07)
        ("C501", "ESTADO_01", "Buen estado"),
        ("C501", "ESTADO_02", "Regular estado"),
        ("C501", "ESTADO_03", "Mal estado"),
        ("C501", "ESTADO_04", "No Aplica"),

        # ===== C601 - Otros espacios educativos =====
        ("C601", "ESPACIO_001", "Aula de clase"),
        ("C601", "ESPACIO_002", "Sala o aula de psicomotricidad"),
        ("C601", "ESPACIO_003", "Aula vivencial (CEBE)"),
        ("C601", "ESPACIO_004", "Sala educativa (PRITE)"),
        ("C601", "ESPACIO_005", "Sala de usos múltiples (SUM)"),
        ("C601", "ESPACIO_006", "Auditorio"),
        ("C601", "ESPACIO_007", "Sala de danza"),
        ("C601", "ESPACIO_008", "Sala de música"),
        ("C601", "ESPACIO_011", "Biblioteca Tipo I – 75 m2 o menos"),
        ("C601", "ESPACIO_012", "Biblioteca Tipo II – 90 m2"),
        ("C601", "ESPACIO_013", "Biblioteca Tipo III – 120 m2 o más"),
        ("C601", "ESPACIO_015", "Aula de Innovación Pedagógica"),
        ("C601", "ESPACIO_020", "Laboratorio de Ciencia y Tecnología"),
        ("C601", "ESPACIO_021", "Taller Creativo"),
        ("C601", "ESPACIO_024", "Taller de Educación para el Trabajo"),
        ("C601", "ESPACIO_028", "Laboratorio de Idiomas"),
        ("C601", "ESPACIO_029", "Laboratorio de Ciencias"),
        ("C601", "ESPACIO_036", "Taller de Informática"),
        ("C601", "ESPACIO_044", "Taller de Cocina"),
        ("C601", "ESPACIO_063", "Gimnasio"),
        ("C601", "ESPACIO_068", "Quiosco"),
        ("C601", "ESPACIO_069", "Cafetería"),
        ("C601", "ESPACIO_070", "Comedor"),
        ("C601", "ESPACIO_071", "Cocina"),
        ("C601", "ESPACIO_072", "Tópico"),
        ("C601", "ESPACIO_085", "Almacén General"),
        ("C601", "ESPACIO_086", "Depósito General"),
        ("C601", "ESPACIO_087", "Vigilancia o Caseta de Control"),
        ("C601", "ESPACIO_088", "Cuarto de Máquinas y Cisternas"),
        ("C601", "ESPACIO_094", "Módulo de Conectividad"),
        ("C601", "ESPACIO_099", "Dirección / Dirección General"),
        ("C601", "ESPACIO_100", "Subdirección"),
        ("C601", "ESPACIO_101", "Administración / Área Administrativa"),
        ("C601", "ESPACIO_105", "Sala de Docentes"),
        ("C601", "ESPACIO_106", "Sala de Reuniones"),

        # ===== C605 - Espacios deportivos abiertos =====
        ("C605", "115", "Losa multiuso tipo I 15x28"),
        ("C605", "116", "Losa multiuso tipo II 20x40"),
        ("C605", "117", "Pista de velocidad y saltos (80 a 120 m)"),
        ("C605", "118", "Piscina semiolímpica sin techar"),
        ("C605", "119", "Piscina olímpica sin techar"),
        ("C605", "120", "Campo de fútbol y campo atlético"),
        ("C605", "121", "Solo campo de fútbol"),
        ("C605", "122", "Solo campo atlético"),
        ("C605", "123", "Otro espacio deportivo abierto"),
        ("C605", "124", "Área de ingreso"),
        ("C605", "125", "Pasadizos y circulaciones"),
        ("C605", "126", "Patio"),
        ("C605", "127", "Área de recreación (Ed. Física)"),
        ("C605", "128", "Áreas verdes y jardines"),
        ("C605", "129", "Espacio de cultivo"),
        ("C605", "130", "Espacio de crianza de animales"),
        ("C605", "131", "Tribuna / Gradería"),
        ("C605", "132", "Otro espacio exterior y de relación"),

        # ===== C701 - Servicios Higiénicos =====
        ("C701", "133", "SS.HH. para estudiantes"),
        ("C701", "134", "SS.HH. para docentes"),
        ("C701", "135", "SS.HH. para estudiantes y docentes"),
        ("C701", "136", "SS.HH. para personal administrativo"),
        ("C701", "137", "SS.HH. para Adultos"),
        ("C701", "138", "SS.HH. para personal de Servicio"),
        ("C701", "139", "Vestidores para estudiantes"),
        ("C701", "140", "Vestidores para personal de Servicio"),

        # ===== C801 - Recursos Tecnológicos =====
        ("C801", "01", "PC de escritorio"),
        ("C801", "02", "Laptop Convencional"),
        ("C801", "03", "Laptop XO"),
        ("C801", "04", "Servidor"),
        ("C801", "05", "Microservidor o Habilitador"),
        ("C801", "06", "Tablet - Aprendo en casa"),
        ("C801", "07", "Tablet - PRONATEL"),
        ("C801", "08", "Tablet - Otros"),
        ("C801", "09", "Proyector multimedia"),
        ("C801", "10", "Pizarra interactiva"),
        ("C801", "11", "Consola de audio para laboratorio de idiomas"),
        ("C801", "12", "Auriculares con audífonos y micrófono"),

        # ===== C802 - Equipamiento =====
        ("C802", "01", "TV"),
        ("C802", "02", "DVD / BLUERAY"),
        ("C802", "03", "Radio, minicomponente"),
        ("C802", "04", "Equipo de sonido (consolas separadas)"),
        ("C802", "05", "Parlante portátil"),
        ("C802", "06", "Parlante pasivo"),
        ("C802", "07", "Sólo fotocopiadora"),
        ("C802", "08", "Sólo escáner"),
        ("C802", "09", "Sólo impresora"),
        ("C802", "10", "Multifuncional (fotocopia, escanea e imprime)"),
        ("C802", "11", "Pantalla de proyección ECRAN"),
        ("C802", "12", "Kits de robótica educativa"),
        ("C802", "13", "Equipos de talleres ligeros"),
        ("C802", "14", "Equipos de talleres pesados"),
        ("C802", "15", "Equipos de aire acondicionado y/o climatización"),
        ("C802", "16", "Extractores de aire"),

        # ===== C803 - Equipos de Interconexión =====
        ("C803", "01", "Switch para pared"),
        ("C803", "02", "Modem"),
        ("C803", "03", "Router"),
        ("C803", "04", "Access Point"),
        ("C803", "05", "UPS"),
        ("C803", "06", "Estabilizadores"),

        # ===== C901 - Espacios educativos y/o administrativos =====
        ("C901", "001", "Aula de clase"),
        ("C901", "005", "Sala de usos múltiples (SUM)"),
        ("C901", "006", "Auditorio"),
        ("C901", "011", "Biblioteca Tipo I"),
        ("C901", "015", "Aula de Innovación Pedagógica"),
        ("C901", "020", "Laboratorio de Ciencia y Tecnología"),
        ("C901", "024", "Taller de Educación para el Trabajo"),
        ("C901", "036", "Taller de Informática"),
        ("C901", "044", "Taller de Cocina"),
        ("C901", "063", "Gimnasio"),
        ("C901", "068", "Quiosco"),
        ("C901", "069", "Cafetería"),
        ("C901", "070", "Comedor"),
        ("C901", "071", "Cocina"),
        ("C901", "072", "Tópico"),
        ("C901", "085", "Almacén General"),
        ("C901", "087", "Vigilancia o Caseta de Control"),
        ("C901", "094", "Módulo de Conectividad"),
        ("C901", "099", "Dirección / Dirección General"),
        ("C901", "100", "Subdirección"),
        ("C901", "101", "Administración / Área Administrativa"),
        ("C901", "105", "Sala de Docentes"),
        ("C901", "106", "Sala de Reuniones"),
        ("C901", "126", "Patio"),
        ("C901", "128", "Áreas verdes y jardines"),
        ("C901", "133", "SS.HH. para estudiantes"),
        ("C901", "134", "SS.HH. para docentes"),
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