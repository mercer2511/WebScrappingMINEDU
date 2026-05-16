from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DIR_PARQUET_2023 = BASE_DIR / "parquet" / "2023"
DIR_SALIDA = BASE_DIR / "salidas"
DIR_SALIDA.mkdir(exist_ok=True)

COLUMNAS_INTERES = [
    "niv_mod",
    "ges_dep",
    "area_med",
    "area_censo",
    "cod_car",
    "forma",
    "tipoprog",
    "gestion",
    "tipdato",
    "cuadro",
    "nroced",
    "modalidad",
    "recibio",
    "chk",
    "chk1",
    "chk2",
    "tipo_financ",
    "tipo_finan",
    "tipo_reva",
]

MAX_VALORES_A_MOSTRAR = 100


def ordenar_valores(valores):
    """Ordena valores únicos convirtiéndolos a texto para evitar errores entre tipos mixtos."""
    return sorted(valores, key=lambda x: str(x))


def obtener_valores_unicos(df, columna):
    """Obtiene valores únicos no nulos de una columna."""
    valores = df[columna].dropna().unique()
    return ordenar_valores(valores)


def analizar_parquet(ruta_parquet):
    print("\n" + "=" * 100)
    print(f"ARCHIVO: {ruta_parquet.relative_to(BASE_DIR)}")

    df = pd.read_parquet(ruta_parquet)

    print(f"Filas: {len(df):,}")
    print(f"Columnas: {len(df.columns):,}")

    print("\nColumnas:")
    for columna in df.columns:
        print(f"  - {columna}")

    print("\nValores únicos de columnas de interés:")
    columnas_encontradas = [col for col in COLUMNAS_INTERES if col in df.columns]

    if not columnas_encontradas:
        print("  No se encontraron columnas de interés en este archivo.")
        return []

    registros_resumen = []

    for columna in columnas_encontradas:
        valores = obtener_valores_unicos(df, columna)

        print(f"\n  {columna} ({len(valores):,} valores únicos):")

        for valor in valores[:MAX_VALORES_A_MOSTRAR]:
            print(f"    {repr(valor)}")

        if len(valores) > MAX_VALORES_A_MOSTRAR:
            print(f"    ... {len(valores) - MAX_VALORES_A_MOSTRAR:,} valores más")

        for valor in valores:
            registros_resumen.append(
                {
                    "archivo": str(ruta_parquet.relative_to(BASE_DIR)),
                    "tabla": ruta_parquet.parent.name,
                    "columna": columna,
                    "valor": valor,
                }
            )

    return registros_resumen


def main():
    if not DIR_PARQUET_2023.exists():
        print(f"No existe la carpeta: {DIR_PARQUET_2023}")
        return

    archivos_parquet = sorted(DIR_PARQUET_2023.rglob("*.parquet"))

    if not archivos_parquet:
        print(f"No se encontraron archivos parquet en: {DIR_PARQUET_2023}")
        return

    print("=" * 100)
    print("ANÁLISIS DE COLUMNAS Y VALORES ÚNICOS - PARQUET 2023")
    print("=" * 100)
    print(f"Carpeta: {DIR_PARQUET_2023}")
    print(f"Archivos encontrados: {len(archivos_parquet):,}")

    resumen = []

    for ruta_parquet in archivos_parquet:
        try:
            resumen.extend(analizar_parquet(ruta_parquet))
        except Exception as error:
            print("\n" + "!" * 100)
            print(f"Error procesando {ruta_parquet}: {error}")

    if resumen:
        df_resumen = pd.DataFrame(resumen)
        ruta_salida = DIR_SALIDA / "valores_unicos_parquet_2023.csv"
        df_resumen.to_csv(ruta_salida, index=False, encoding="utf-8-sig")

        print("\n" + "=" * 100)
        print("RESUMEN GUARDADO")
        print("=" * 100)
        print(f"Archivo CSV: {ruta_salida}")
        print(f"Registros guardados: {len(df_resumen):,}")


if __name__ == "__main__":
    main()