import pandas as pd
from pathlib import Path

# Ajusta la ruta a tu proyecto
parquet_path = Path("pre_procesamiento/parquet/2023/04_Docentes01/Docente_01.parquet").resolve()
df = pd.read_parquet(parquet_path)
print(df.columns.tolist())