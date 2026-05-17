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
    __file__).resolve().parent.parent / "pre_procesamiento" / "parquet" / "2023" / "01_Matricula01" / "Matricula_01.parquet"
anio_carpeta = parquet_path.parent.parent.name

print(f"📥 Leyendo {parquet_path.name} (Año: {anio_carpeta})...")
df = pd.read_parquet(parquet_path)
df.columns = df.columns.str.lower()

# 3. Transformaciones
print("⚙️ Limpiando datos...")
if 'modalidad' in df.columns:
    df['modalidad'] = df['modalidad'].replace({'': None})

# Generar lista de columnas 'd01' a 'd30' que existan en el df
d_cols = [f'd{str(i).zfill(2)}' for i in range(1, 31)]

# Rellenar NaNs con None
df = df.where(pd.notnull(df), None)

# 4. Inserción
# Construimos el SQL dinámico para incluir d01-d30
d_cols_sql = ", ".join(d_cols)
d_params_sql = ", ".join([f":{col}" for col in d_cols])

insert_query = text(f"""
    INSERT INTO matricula (
        cod_mod, anexo, anio, nroced, cuadro, tipdato, modalidad, {d_cols_sql}
    ) VALUES (
        :cod_mod, :anexo, :anio, :nroced, :cuadro, :tipdato, :modalidad, {d_params_sql}
    )
""")

chunk_size = 10000
records = df.to_dict(orient='records')
total_records = len(records)

print(f"🚀 Iniciando inserción de {total_records} registros en la tabla matricula...")

with engine.begin() as conn:
    for i in range(0, total_records, chunk_size):
        chunk = records[i:i + chunk_size]

        params = []
        for r in chunk:
            row_dict = {
                "cod_mod": r.get("cod_mod"),
                "anexo": r.get("anexo", "0"),
                "anio": anio_carpeta,
                "nroced": r.get("nroced"),
                "cuadro": r.get("cuadro"),
                "tipdato": r.get("tipdato"),
                "modalidad": r.get("modalidad")
            }
            # Cargar los valores d01-d30 castéandolos a entero si existen
            for col in d_cols:
                val = r.get(col)
                row_dict[col] = int(val) if val is not None else None

            params.append(row_dict)

        conn.execute(insert_query, params)
        print(f"✅ Cargados {min(i + chunk_size, total_records)} / {total_records}")

print("🎉 ¡Carga de Matrículas completada con éxito!")