import os
import csv
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar .env desde la raíz del proyecto
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("❌ No se encontró DATABASE_URL en el .env")

engine = create_engine(DATABASE_URL)

# Ruta al CSV
csv_path = Path(__file__).resolve().parent / "ubigeo.csv"

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    with engine.begin() as conn:
        for row in reader:
            conn.execute(
                text(
                    "INSERT INTO ubigeo (codgeo, departamento, provincia, distrito, capital_legal) "
                    "VALUES (:codgeo, :dep, :prov, :dist, :capital) "
                    "ON CONFLICT (codgeo) DO NOTHING"
                ),
                {
                    "codgeo": row["IDDIST"].strip(),
                    "dep": row["NOMBDEP"].strip(),
                    "prov": row["NOMBPROV"].strip(),
                    "dist": row["NOMBDIST"].strip(),
                    "capital": row["NOM_CAPITAL (LEGAL)"].strip() if "NOM_CAPITAL (LEGAL)" in row else None,
                }
            )

print("✅ Ubigeos cargados correctamente.")