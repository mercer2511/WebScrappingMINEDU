import json
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DIR_SALIDA = BASE_DIR / "salidas"

CSV_VALORES_UNICOS = DIR_SALIDA / "valores_unicos_parquet_2023.csv"
SALIDA_JSON = DIR_SALIDA / "diccionario_datos_2023.json"


DICCIONARIOS_MANUALES = {
    "niv_mod": {
        "A1": "Inicial - Cuna",
        "A2": "Inicial - Jardín",
        "A3": "Inicial - Cuna-jardín",
        "A5": "Inicial - Programa no escolarizado",
        "B0": "Primaria",
        "F0": "Secundaria",
        "D1": "Básica Alternativa - CEBA Inicial e Intermedio",
        "D2": "Básica Alternativa - CEBA Avanzado",
        "E0": "Básica Especial - PRITE",
        "E1": "Básica Especial - Inicial",
        "E2": "Básica Especial - Primaria",
        "K0": "Superior Pedagógica - ISP",
        "P0": "Escuela Superior Pedagógica - ESP",
        "T0": "Superior Tecnológica - IST",
        "S0": "Escuela Superior Tecnológica - EST",
        "M0": "Superior Artística - ESFA",
        "L0": "Técnico Productiva - CETPRO",
    },
    "ges_dep": {
        "A1": "Sector Educación",
        "A2": "Otro sector público (FF.AA.)",
        "A3": "Municipalidad",
        "A4": "Entidad privada en convenio con Sector Educación",
        "B1": "Cooperativo",
        "B2": "Comunidad o asociación religiosa",
        "B3": "Comunidad",
        "B4": "Particular",
        "B5": "Empresa fiscalizada",
        "B6": "Asociación civil / Institución benéfica",
    },
    "area_censo": {
        "1": "Urbana",
        "2": "Rural",
    },
    "area_med": {
        "1": "Urbana",
        "2": "Rural",
    },
    "cod_car": {
        "1": "Unidocente multigrado",
        "2": "Polidocente multigrado",
        "3": "Polidocente completo",
        "a": "No aplica",
    },
    "forma": {
        "S": "Escolarizada",
        "N": "No escolarizada",
        "a": "No aplica",
    },
    "tipoprog": {
        "11": "Ciclo I - Entorno familiar",
        "12": "Ciclo I - Entorno comunitario",
        "13": "Ciclo I - SET",
        "14": "Ciclo II - Entorno familiar",
        "15": "Ciclo II - Entorno comunitario",
        "a": "No aplica",
    },
    "gestion": {
        "1": "Pública de gestión directa",
        "2": "Pública de gestión privada",
        "3": "Privada",
    },
    "modalidad": {
        "Presencial": "Presencial",
        "Semi-Presencial": "Semipresencial",
        "A distancia": "A distancia",
        "": "Sin información / No aplica",
    },
    "recibio": {
        "1": "Sí",
        "2": "No",
    },
    "chk": {
        "1": "Sí / Marcado",
        "2": "No / No marcado",
    },
    "chk1": {
        "1": "Sí / Marcado",
        "2": "No / No marcado",
    },
    "chk2": {
        "1": "Sí / Marcado",
        "2": "No / No marcado",
    },
}


DESCRIPCIONES_CAMPOS = {
    "niv_mod": "Nivel educativo y modalidad del servicio educativo.",
    "ges_dep": "Dependencia o entidad que gestiona la institución educativa.",
    "area_censo": "Área geográfica del servicio educativo según el censo.",
    "area_med": "Área geográfica del servicio educativo.",
    "cod_car": "Característica del servicio según relación docente/sección.",
    "forma": "Forma de atención del servicio educativo.",
    "tipoprog": "Tipo de programa no escolarizado.",
    "gestion": "Tipo de gestión de la institución educativa.",
    "tipdato": "Código de categoría, tipo de dato o respuesta según el cuadro.",
    "cuadro": "Código del cuadro o pregunta censal.",
    "nroced": "Número de cédula censal.",
    "modalidad": "Modalidad del servicio educativo.",
    "recibio": "Indica si recibió el material, recurso o servicio.",
    "chk": "Campo de marca o selección.",
    "chk1": "Campo de marca o selección.",
    "chk2": "Campo de marca o selección.",
    "tipo_financ": "Tipo de financiamiento.",
    "tipo_finan": "Tipo de financiamiento.",
    "tipo_reva": "Tipo de documento de revalidación.",
}


def normalizar_valor(valor):
    if pd.isna(valor):
        return ""
    return str(valor).strip()


def crear_diccionario():
    if not CSV_VALORES_UNICOS.exists():
        raise FileNotFoundError(f"No existe el archivo: {CSV_VALORES_UNICOS}")

    df = pd.read_csv(CSV_VALORES_UNICOS, dtype=str, keep_default_na=False)

    resultado = {
        "anio": "2023",
        "fuente": str(CSV_VALORES_UNICOS.relative_to(BASE_DIR)),
        "descripcion": "Diccionario de datos construido desde valores únicos observados en archivos Parquet 2023.",
        "tablas": {},
        "diccionarios_globales": DICCIONARIOS_MANUALES,
    }

    for (tabla, archivo), df_tabla in df.groupby(["tabla", "archivo"], dropna=False):
        tabla_info = {
            "archivo": archivo,
            "campos": {},
        }

        for columna, df_columna in df_tabla.groupby("columna", dropna=False):
            valores_observados = sorted(
                {normalizar_valor(v) for v in df_columna["valor"].tolist()},
                key=lambda x: str(x),
            )

            diccionario_campo = DICCIONARIOS_MANUALES.get(columna, {})

            valores_detallados = {}

            for valor in valores_observados:
                valores_detallados[valor] = {
                    "significado": diccionario_campo.get(valor),
                    "documentado": valor in diccionario_campo,
                }

            tabla_info["campos"][columna] = {
                "descripcion": DESCRIPCIONES_CAMPOS.get(columna),
                "cantidad_valores_unicos": len(valores_observados),
                "valores_observados": valores_observados,
                "valores": valores_detallados,
            }

        resultado["tablas"][tabla] = tabla_info

    return resultado


def main():
    DIR_SALIDA.mkdir(exist_ok=True)

    diccionario = crear_diccionario()

    with SALIDA_JSON.open("w", encoding="utf-8") as archivo:
        json.dump(diccionario, archivo, ensure_ascii=False, indent=2)

    print("=" * 80)
    print("DICCIONARIO DE DATOS JSON GENERADO")
    print("=" * 80)
    print(f"Salida: {SALIDA_JSON}")
    print(f"Tablas procesadas: {len(diccionario['tablas']):,}")


if __name__ == "__main__":
    main()