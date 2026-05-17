import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Configuración de Entorno y Base de Datos
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ No se encontró DATABASE_URL en el .env")

engine = create_engine(DATABASE_URL)

# 2. Rutas del Parquet
parquet_path = Path(__file__).resolve().parent.parent / "pre_procesamiento" / "parquet" / "2023" / "00_Padron" / "Padron.parquet"

# Extraer el año dinámicamente de la ruta de carpetas
anio_carpeta = parquet_path.parent.parent.name
print(f"📅 Año detectado: {anio_carpeta}")

print(f"📥 Leyendo archivo Parquet: {parquet_path.name}...")
df = pd.read_parquet(parquet_path)

# Convertir todos los nombres de columnas a minúsculas
df.columns = df.columns.str.lower()

# Función antibalas para limpiar strings (Evita el error 'nan' de 3 caracteres)
def clean_str(val):
    if pd.isna(val):  # Atrapa verdaderos nulos, np.nan, math.nan
        return None
    s = str(val).strip()
    if s == "" or s.lower() == "nan" or s.lower() == "<na>":
        return None
    return s

# 3. Preparar la Inserción
insert_query = text("""
                    INSERT INTO padron_ie (cod_mod, anexo, anio, codlocal, cen_edu, niv_mod_codigo, cod_car,
                                           forma_codigo,
                                           tipoprog_codigo, gestion_codigo, dependencia_codigo, tipsexo_codigo,
                                           cod_tur_codigo, director, telefono, email, pagweb, direccion, localidad,
                                           referencia, codgeo, codooii, dre_ugel, region_edu, codcp_inei, codcp_med,
                                           cen_pob, area_censo_codigo, dis_vraem_codigo, dis_front_codigo, region_nat,
                                           nlat_ie, nlong_ie, altitud, imputado_codigo)
                    VALUES (:cod_mod, :anexo, :anio, :codlocal, :cen_edu, :niv_mod, :cod_car, :forma,
                            :tipoprog, :gestion_codigo, :dependencia_codigo, :tipsexo,
                            :cod_tur, :director, :telefono, :email, :pagweb, :direccion, :localidad,
                            :referencia, :codgeo, :codooii, :dre_ugel, :region_edu, :codcp_inei, :codcp_med,
                            :cen_pob, :area_censo, :dis_vraem, :dis_front, :region_nat,
                            :nlat_ie, :nlong_ie, :altitud, :imputado)
                    ON CONFLICT (cod_mod, anexo, anio) DO NOTHING
                    """)

# 4. Inserción por lotes
chunk_size = 5000
records = df.to_dict(orient='records')
total_records = len(records)

print(f"🚀 Iniciando inserción de {total_records} registros en padron_ie...")

with engine.begin() as conn:
    for i in range(0, total_records, chunk_size):
        chunk = records[i:i + chunk_size]

        params = []
        for r in chunk:
            gestion_val = r.get("gestión") if r.get("gestión") is not None else r.get("gestion")

            params.append({
                "cod_mod": clean_str(r.get("cod_mod")),
                "anexo": clean_str(r.get("anexo")) or "0",
                "anio": anio_carpeta,
                "codlocal": clean_str(r.get("codlocal")),
                "cen_edu": clean_str(r.get("cen_edu")),
                "niv_mod": clean_str(r.get("niv_mod")),
                "cod_car": clean_str(r.get("cod_car")),
                "forma": clean_str(r.get("forma")),
                "tipoprog": clean_str(r.get("tipoprog")),
                "gestion_codigo": clean_str(gestion_val),
                "dependencia_codigo": clean_str(r.get("ges_dep")),
                "tipsexo": clean_str(r.get("tipssexo") or r.get("tipsexo")),
                "cod_tur": clean_str(r.get("cod_tur")),
                "director": clean_str(r.get("director")),
                "telefono": clean_str(r.get("telefono")),
                "email": clean_str(r.get("email")),
                "pagweb": clean_str(r.get("pagweb")),
                "direccion": clean_str(r.get("direccion")),
                "localidad": clean_str(r.get("localidad")),
                "referencia": clean_str(r.get("referencia")),
                "codgeo": clean_str(r.get("codgeo")),
                "codooii": clean_str(r.get("codooii")),
                "dre_ugel": clean_str(r.get("dre_ugel")),
                "region_edu": clean_str(r.get("region_edu")),
                "codcp_inei": clean_str(r.get("codcp_inei")),
                "codcp_med": clean_str(r.get("codcp_med")),
                "cen_pob": clean_str(r.get("cen_pob")),
                "area_censo": clean_str(r.get("area_censo")),
                "dis_vraem": clean_str(r.get("dis_vraem")),
                "dis_front": clean_str(r.get("dis_front")),
                "region_nat": clean_str(r.get("region_nat")),
                # Numéricos directos
                "nlat_ie": r.get("nlat_ie") if not pd.isna(r.get("nlat_ie")) else None,
                "nlong_ie": r.get("nlong_ie") if not pd.isna(r.get("nlong_ie")) else None,
                "altitud": r.get("altitud") if not pd.isna(r.get("altitud")) else None,
                "imputado": clean_str(r.get("imputado"))
            })

        conn.execute(insert_query, params)
        print(f"✅ Cargados {min(i + chunk_size, total_records)} / {total_records}")

print("🎉 ¡Carga del Padrón completada con éxito!")