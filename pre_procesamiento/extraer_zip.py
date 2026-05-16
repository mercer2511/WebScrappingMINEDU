import shutil
import zipfile
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
DIR_DESCARGAS = PROJECT_DIR / "minedu" / "descargas"
DIR_EXTRAIDOS = BASE_DIR / "extraidos"

# Extensiones que nos interesan
EXTENSIONES_VALIDAS = {".csv", ".txt", ".xlsx", ".xls", ".dbf", ".sav", ".dta"}


def es_archivo_valido(nombre_archivo):
    """Valida si un archivo dentro del ZIP debe extraerse."""
    ruta = Path(nombre_archivo)
    partes = ruta.parts

    if nombre_archivo.endswith("/"):
        return False

    if ruta.is_absolute():
        return False

    if ".." in partes:
        return False

    if "__MACOSX" in partes:
        return False

    if any(parte.startswith(".") for parte in partes):
        return False

    return ruta.suffix.lower() in EXTENSIONES_VALIDAS


def extraer_archivo_seguro(zf, archivo, destino_zip):
    """Extrae un archivo evitando rutas peligrosas dentro del ZIP."""
    ruta_relativa = Path(archivo)
    ruta_destino = destino_zip / ruta_relativa

    ruta_destino.parent.mkdir(parents=True, exist_ok=True)

    with zf.open(archivo) as origen, open(ruta_destino, "wb") as destino:
        shutil.copyfileobj(origen, destino)

    return ruta_destino


def extraer_zip_año(año):
    """Extrae todos los ZIP de un año en extraidos/{año}/"""
    carpeta_zip = DIR_DESCARGAS / año
    carpeta_destino = DIR_EXTRAIDOS / año

    if not carpeta_zip.exists():
        print(f"⚠️  No existe la carpeta {carpeta_zip}")
        return 0, 0

    archivos_zip = sorted(carpeta_zip.glob("*.zip"))
    total_zips_procesados = 0
    total_archivos = 0

    for zip_path in archivos_zip:
        nombre_zip = zip_path.stem
        destino_zip = carpeta_destino / nombre_zip

        if destino_zip.exists():
            shutil.rmtree(destino_zip)

        destino_zip.mkdir(parents=True, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                archivos_validos = [
                    archivo
                    for archivo in zf.namelist()
                    if es_archivo_valido(archivo)
                ]

                for archivo in archivos_validos:
                    extraer_archivo_seguro(zf, archivo, destino_zip)
                    total_archivos += 1

                if archivos_validos:
                    print(f"  ✓ {nombre_zip}.zip → {len(archivos_validos)} archivos")
                else:
                    print(f"  ⚠ {nombre_zip}.zip → sin archivos válidos")

        except zipfile.BadZipFile:
            print(f"  ✗ {nombre_zip}.zip → archivo corrupto")
            continue
        except Exception as error:
            print(f"  ✗ {nombre_zip}.zip → error: {error}")
            continue

        total_zips_procesados += 1

    return total_zips_procesados, total_archivos


def main():
    print("=" * 60)
    print("EXTRACCIÓN DE ARCHIVOS ZIP - MINEDU")
    print("=" * 60)

    # Limpiar carpeta de extraídos si existe
    if DIR_EXTRAIDOS.exists():
        respuesta = input("¿Borrar carpeta 'extraidos' anterior y re-extraer? (s/n): ")
        if respuesta.lower() == "s":
            shutil.rmtree(DIR_EXTRAIDOS)
            print("  ✓ Carpeta anterior eliminada")

    DIR_EXTRAIDOS.mkdir(parents=True, exist_ok=True)

    total_zips = 0
    total_archivos = 0

    for año in ["2023", "2024", "2025"]:
        print(f"\n📁 Procesando año {año}...")
        zips, archivos = extraer_zip_año(año)
        total_zips += zips
        total_archivos += archivos

    print("\n" + "=" * 60)
    print(f"✅ EXTRACCIÓN COMPLETA")
    print(f"   ZIPs procesados: {total_zips}")
    print(f"   Archivos extraídos: {total_archivos}")
    print(f"   Origen: {DIR_DESCARGAS.resolve()}")
    print(f"   Destino: {DIR_EXTRAIDOS.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    main()