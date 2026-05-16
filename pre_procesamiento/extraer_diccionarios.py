import json
import re
from pathlib import Path

import pdfplumber

BASE_DIR = Path(__file__).resolve().parent
DIR_DESCARGAS = BASE_DIR.parent / "minedu" / "descargas"
DIR_DICCIONARIOS = BASE_DIR / "diccionarios"
DIR_DICCIONARIOS.mkdir(exist_ok=True)

AÑOS = ["2023", "2024", "2025"]


def limpiar_nombre_archivo(nombre):
    """Convierte el nombre del PDF en un nombre seguro para archivos de salida."""
    nombre = nombre.lower()
    nombre = nombre.replace(".pdf", "")
    nombre = re.sub(r"\W+", "_", nombre, flags=re.UNICODE)
    nombre = re.sub(r"_+", "_", nombre)
    nombre = nombre.strip("_")
    return nombre


def buscar_pdfs_diccionario(año):
    """Busca PDFs de diccionario dentro de la carpeta de descargas de un año."""
    carpeta_año = DIR_DESCARGAS / año

    if not carpeta_año.exists():
        print(f"⚠️  No existe la carpeta {carpeta_año}")
        return []

    pdfs = sorted(
        ruta
        for ruta in carpeta_año.glob("*.pdf")
        if "diccionario" in ruta.name.lower()
    )

    return pdfs


def extraer_texto_y_tablas(año, ruta_pdf):
    print(f"\n📄 Procesando {año} | {ruta_pdf.name}")

    texto_completo = []
    tablas_extraidas = []

    with pdfplumber.open(ruta_pdf) as pdf:
        total_paginas = len(pdf.pages)

        for numero_pagina, page in enumerate(pdf.pages, start=1):
            texto = page.extract_text()

            if texto:
                texto_completo.append(
                    {
                        "pagina": numero_pagina,
                        "texto": texto,
                    }
                )

            tablas = page.extract_tables()

            for numero_tabla, tabla in enumerate(tablas, start=1):
                if not tabla:
                    continue

                tablas_extraidas.append(
                    {
                        "año": año,
                        "pdf": ruta_pdf.name,
                        "pagina": numero_pagina,
                        "tabla": numero_tabla,
                        "filas": tabla,
                    }
                )

    nombre_salida = limpiar_nombre_archivo(ruta_pdf.name)

    ruta_txt = guardar_texto(año, nombre_salida, texto_completo)
    ruta_json = guardar_tablas(año, nombre_salida, tablas_extraidas)

    resumen = {
        "año": año,
        "pdf": ruta_pdf.name,
        "ruta_pdf": str(ruta_pdf),
        "paginas_pdf": total_paginas,
        "paginas_con_texto": len(texto_completo),
        "tablas_detectadas": len(tablas_extraidas),
        "salida_texto": str(ruta_txt),
        "salida_tablas": str(ruta_json),
    }

    print(f"  ✓ Páginas PDF: {total_paginas}")
    print(f"  ✓ Páginas con texto: {len(texto_completo)}")
    print(f"  ✓ Tablas detectadas: {len(tablas_extraidas)}")
    print(f"  ✓ Texto guardado: {ruta_txt.name}")
    print(f"  ✓ Tablas guardadas: {ruta_json.name}")

    return resumen


def guardar_texto(año, nombre_salida, texto_completo):
    carpeta_año = DIR_DICCIONARIOS / año
    carpeta_año.mkdir(parents=True, exist_ok=True)

    salida_txt = carpeta_año / f"{nombre_salida}.txt"

    texto_final = "\n\n".join(
        f"--- PÁGINA {item['pagina']} ---\n{item['texto']}"
        for item in texto_completo
    )

    with open(salida_txt, "w", encoding="utf-8") as archivo:
        archivo.write(texto_final)

    return salida_txt


def guardar_tablas(año, nombre_salida, tablas_extraidas):
    carpeta_año = DIR_DICCIONARIOS / año
    carpeta_año.mkdir(parents=True, exist_ok=True)

    salida_json = carpeta_año / f"{nombre_salida}_tablas.json"

    with open(salida_json, "w", encoding="utf-8") as archivo:
        json.dump(tablas_extraidas, archivo, ensure_ascii=False, indent=2)

    return salida_json


def guardar_manifest(resumenes):
    salida_manifest = DIR_DICCIONARIOS / "manifest_diccionarios.json"

    with open(salida_manifest, "w", encoding="utf-8") as archivo:
        json.dump(resumenes, archivo, ensure_ascii=False, indent=2)

    print(f"\n📌 Manifest guardado: {salida_manifest}")


def main():
    print("=" * 60)
    print("EXTRACCIÓN DE DICCIONARIOS PDF - MINEDU")
    print("=" * 60)

    resumenes = []

    for año in AÑOS:
        print(f"\n📁 Buscando PDFs de diccionario para {año}...")

        pdfs = buscar_pdfs_diccionario(año)

        if not pdfs:
            print(f"  ⚠ No se encontraron PDFs de diccionario para {año}")
            continue

        print(f"  ✓ PDFs encontrados: {len(pdfs)}")

        for ruta_pdf in pdfs:
            try:
                resumen = extraer_texto_y_tablas(año, ruta_pdf)
                resumenes.append(resumen)

            except Exception as error:
                print(f"  ✗ Error procesando {ruta_pdf.name}: {error}")
                resumenes.append(
                    {
                        "año": año,
                        "pdf": ruta_pdf.name,
                        "ruta_pdf": str(ruta_pdf),
                        "error": str(error),
                    }
                )

    guardar_manifest(resumenes)

    print("\n" + "=" * 60)
    print("✅ EXTRACCIÓN COMPLETADA")
    print(f"   PDFs procesados: {len(resumenes)}")
    print(f"   Destino: {DIR_DICCIONARIOS.resolve()}")
    print("=" * 60)


if __name__ == "__main__":
    main()