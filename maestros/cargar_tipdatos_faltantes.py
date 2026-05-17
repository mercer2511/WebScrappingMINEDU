import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Configuración
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)
engine = create_engine(os.getenv("DATABASE_URL"))

# 2. Rutas a los parquets (Ahora apuntamos a Docentes)
base_path = Path(__file__).resolve().parent.parent / "pre_procesamiento" / "parquet" / "2023"
archivos_parquet = [
    base_path / "04_Docentes01" / "Docente_01.parquet",
    base_path / "05_Docentes02" / "Docente_02.parquet",
    base_path / "06_Docentes03" / "Docente_03.parquet",
    base_path / "07_Docentes04" / "Docente_04.parquet"
]

# 3. Extraer combinaciones únicas de los Parquets
print("🔍 Escaneando archivos Parquet en busca de combinaciones (cuadro, tipdato)...")
pares_unicos = set()
cuadros_unicos = set()


def clean_str(val):
    if pd.isna(val): return None
    s = str(val).strip()
    return None if s == "" or s.lower() == "nan" else s


for ruta in archivos_parquet:
    if ruta.exists():
        print(f"   -> Leyendo {ruta.name}...")
        df = pd.read_parquet(ruta, columns=['cuadro', 'tipdato'])

        # Limpiar y extraer
        for idx, row in df.drop_duplicates().iterrows():
            cuadro = clean_str(row['cuadro'])
            tipdato = clean_str(row['tipdato'])
            if cuadro and tipdato:
                pares_unicos.add((cuadro, tipdato))
                cuadros_unicos.add(cuadro)

print(f"📊 Se encontraron {len(pares_unicos)} combinaciones únicas en los Parquets.")

# 4. Insertar primero los 'cuadros' maestros faltantes (El Padre)
print("🛡️ Verificando e insertando CUADROS maestros faltantes...")
with engine.begin() as conn:
    result_cuadros = conn.execute(text("SELECT codigo FROM cuadro"))
    existentes_cuadros = set(row[0] for row in result_cuadros.fetchall())

    cuadros_faltantes = cuadros_unicos - existentes_cuadros

    if cuadros_faltantes:
        print(f"   -> Insertando {len(cuadros_faltantes)} cuadros nuevos...")
        insert_c_query = text("""
                              INSERT INTO cuadro (codigo, descripcion)
                              VALUES (:codigo, 'CUADRO RECUPERADO DE PARQUET 2023')
                              ON CONFLICT (codigo) DO NOTHING
                              """)
        params_c = [{"codigo": c} for c in cuadros_faltantes]
        conn.execute(insert_c_query, params_c)

# 5. Insertar las combinaciones (El Hijo)
print("🛡️ Verificando e insertando combinaciones CUADRO_TIPDATO faltantes...")
with engine.begin() as conn:
    result_pares = conn.execute(text("SELECT cuadro_codigo, tipdato FROM cuadro_tipdato"))
    existentes_pares = set((row[0], row[1]) for row in result_pares.fetchall())

    pares_faltantes = pares_unicos - existentes_pares

    if pares_faltantes:
        print(f"   -> Insertando {len(pares_faltantes)} combinaciones nuevas...")
        insert_p_query = text("""
                              INSERT INTO cuadro_tipdato (cuadro_codigo, tipdato, descripcion)
                              VALUES (:cuadro, :tipdato, 'RECUPERADO DE PARQUET 2023')
                              ON CONFLICT (cuadro_codigo, tipdato) DO NOTHING
                              """)
        params_p = [{"cuadro": c, "tipdato": t} for c, t in pares_faltantes]
        conn.execute(insert_p_query, params_p)

print("🎉 ¡Diccionarios de Matrícula actualizados con éxito!")