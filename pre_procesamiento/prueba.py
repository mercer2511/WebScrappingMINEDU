from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DIR_PARQUET = BASE_DIR / "parquet" / "2023"

# Buscamos la carpeta que contenga "Resultados_2023" en el nombre
carpetas = [d for d in DIR_PARQUET.iterdir() if d.is_dir() and "resultados_2023" in d.name.lower()]
if not carpetas:
    print("No se encontró la carpeta de Resultados_2023. Carpetas disponibles:")
    for d in sorted(DIR_PARQUET.iterdir()):
        if d.is_dir():
            print(f"  {d.name}")
    exit()

carpeta = carpetas[0]
parquet_file = next(carpeta.glob("*.parquet"), None)
if not parquet_file:
    print(f"No hay .parquet en {carpeta}")
    exit()

print(f"Usando: {parquet_file}")
df = pd.read_parquet(parquet_file)

print(f"\nColumnas ({len(df.columns)}):")
print(list(df.columns))

print("\nValores de TIPDATO:")
print(df["tipdato"].value_counts(dropna=False))

print("\nValores de CUADRO:")
print(df["cuadro"].value_counts(dropna=False))

print("\nMuestra de 3 filas:")
print(df.head(3))