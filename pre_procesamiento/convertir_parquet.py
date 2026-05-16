import re
import shutil
from pathlib import Path

import pandas as pd
from dbfread import DBF

# Rutas
BASE_DIR = Path(__file__).resolve().parent
DIR_EXTRAIDOS = BASE_DIR / "extraidos"
DIR_PARQUET = BASE_DIR / "parquet"

ENCODINGS_DBF = ["utf-8", "latin1", "cp1252"]


def limpiar_nombre_columna(nombre):
    """Normaliza nombres de columnas para análisis, Snowflake y ML."""
    nombre = str(nombre).strip().lower()
    nombre = re.sub(r"[^\w]+", "_", nombre)
    nombre = re.sub(r"_+", "_", nombre)
    nombre = nombre.strip("_")
    return nombre


def normalizar_columnas(df):
    """Aplica limpieza a los nombres de columnas."""
    df = df.copy()
    df.columns = [limpiar_nombre_columna(columna) for columna in df.columns]
    return df


def dbf_a_dataframe(ruta_dbf):
    """Lee un archivo DBF y lo convierte a DataFrame de Pandas."""
    ultimo_error = None

    for encoding in ENCODINGS_DBF:
        try:
            dbf = DBF(ruta_dbf, load=True, encoding=encoding, char_decode_errors="ignore")
            registros = list(dbf)

            if not registros:
                return None, 0, encoding

            df = pd.DataFrame(registros)
            df = normalizar_columnas(df)

            return df, len(df), encoding

        except Exception as error:
            ultimo_error = error

    print(f"    ✗ Error leyendo {ruta_dbf.name}: {ultimo_error}")
    return None, 0, None


def convertir_año(año):
    """Convierte todos los DBF de un año a Parquet."""
    carpeta_origen = DIR_EXTRAIDOS / año
    carpeta_destino = DIR_PARQUET / año

    if not carpeta_origen.exists():
        print(f"⚠️  No existe {carpeta_origen}")
        return 0, 0

    archivos_dbf = sorted(carpeta_origen.rglob("*.dbf"))
    total_convertidos = 0
    total_filas = 0

    for dbf_path in archivos_dbf:
        subcarpeta = dbf_path.parent.name
        nombre_dbf = dbf_path.stem

        destino_subcarpeta = carpeta_destino / subcarpeta
        destino_subcarpeta.mkdir(parents=True, exist_ok=True)

        ruta_parquet = destino_subcarpeta / f"{nombre_dbf}.parquet"

        tamaño_original = dbf_path.stat().st_size

        print(f"  Procesando: {subcarpeta}/{dbf_path.name}...", end=" ")

        df, num_filas, encoding = dbf_a_dataframe(dbf_path)

        if df is None:
            print("(sin datos)")
            continue

        df["anio"] = int(año)
        df["paquete_origen"] = subcarpeta
        df["archivo_origen"] = dbf_path.name

        df.to_parquet(
            ruta_parquet,
            engine="pyarrow",
            compression="snappy",
            index=False,
        )

        tamaño_parquet = ruta_parquet.stat().st_size
        ratio = (1 - tamaño_parquet / tamaño_original) * 100

        print(
            f"✓ {num_filas:,} filas | "
            f"encoding={encoding} | "
            f"{tamaño_original / 1024:.0f} KB → {tamaño_parquet / 1024:.0f} KB "
            f"({ratio:.0f}% compresión)"
        )

        total_convertidos += 1
        total_filas += num_filas

    return total_convertidos, total_filas


def main():
    print("=" * 60)
    print("CONVERSIÓN DBF → PARQUET - MINEDU")
    print("=" * 60)

    if DIR_PARQUET.exists():
        respuesta = input("¿Borrar carpeta 'parquet' anterior y re-generar? (s/n): ")

        if respuesta.lower() == "s":
            shutil.rmtree(DIR_PARQUET)
            print("  ✓ Carpeta anterior eliminada\n")

    DIR_PARQUET.mkdir(parents=True, exist_ok=True)

    total_archivos = 0
    total_filas = 0

    for año in ["2023", "2024", "2025"]:
        print(f"\n📁 Año {año}")
        print("-" * 40)

        convertidos, filas = convertir_año(año)

        total_archivos += convertidos
        total_filas += filas

        print(f"  → {convertidos} archivos convertidos, {filas:,} filas totales")

    print("\n" + "=" * 60)
    print("✅ CONVERSIÓN COMPLETA")
    print(f"   Archivos Parquet generados: {total_archivos}")
    print(f"   Total de filas procesadas: {total_filas:,}")
    print(f"   Origen: {DIR_EXTRAIDOS.resolve()}")
    print(f"   Destino: {DIR_PARQUET.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    main()