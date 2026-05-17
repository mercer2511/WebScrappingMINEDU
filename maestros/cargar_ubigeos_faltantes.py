import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Configuración
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
engine = create_engine(os.getenv("DATABASE_URL"))

# 2. Leer Parquet
parquet_path = Path(
    __file__).resolve().parent.parent / "pre_procesamiento" / "parquet" / "2023" / "00_Padron" / "Padron.parquet"
df = pd.read_parquet(parquet_path)
df.columns = df.columns.str.lower()

# 3. Ubigeos huérfanos que detectamos
ubigeos_faltantes = [
    '080915', '180107', '250307', '090724', '050512', '221006',
    '250306', '050513', '050514', '030612', '050515', '080918',
    '050413', '090725', '080917', '080916'
]

# Filtrar para quedarse solo con esos 16 códigos y obtener valores únicos
df_faltantes = df[df['codgeo'].isin(ubigeos_faltantes)][['codgeo', 'dpto', 'prov', 'dist']].drop_duplicates()

# 4. Insertar en la base de datos
print("🚀 Insertando ubigeos históricos recuperados...")
with engine.begin() as conn:
    for index, row in df_faltantes.iterrows():
        conn.execute(text("""
                          INSERT INTO ubigeo (codgeo, departamento, provincia, distrito)
                          VALUES (:codgeo, :dpto, :prov, :dist)
                          ON CONFLICT (codgeo) DO NOTHING
                          """), {
                         "codgeo": row['codgeo'],
                         "dpto": row['dpto'].strip() if row['dpto'] else None,
                         "prov": row['prov'].strip() if row['prov'] else None,
                         "dist": row['dist'].strip() if row['dist'] else None
                     })
        print(f"✅ Ubigeo {row['codgeo']}: {row['dpto']} - {row['prov']} - {row['dist']}")

print("🎉 ¡Ubigeos históricos recuperados e insertados con éxito!")