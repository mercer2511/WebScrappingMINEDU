"""
Normaliza los diccionarios de datos del Censo Educativo MINEDU 2023
(archivos TXT extraídos de PDF con pdfplumber) y produce un catálogo
JSON estructurado para el modelo de predicción de abandono escolar.

Salida:
    diccionarios/2023/catalogo_abandono_2023.json

Solo se incluyen las tablas listadas en TABLAS_INTERES (las que existen
como Parquet en el proyecto) y un bloque "campos_generales" con las
variables de identificación comunes a todas las tablas.
"""

import json
import re
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuración                                                                #
# --------------------------------------------------------------------------- #

BASE_DIR = Path(__file__).resolve().parent
DICC_DIR = BASE_DIR / "diccionarios" / "2023"
PARQUET_DIR = BASE_DIR / "parquet" / "2023"

ARCHIVO_MARCO = DICC_DIR / "00_diccionario_marco_censal_2023.txt"
ARCHIVO_CE = DICC_DIR / "00_diccionario_de_datos_ce_2023.txt"
ARCHIVO_RES = DICC_DIR / "00_diccionario_de_datos_ce_2023_resultados.txt"
ARCHIVO_LE = DICC_DIR / "00_diccionario_de_datos_le_2023.txt"

SALIDA = DICC_DIR / "catalogo_abandono_2023.json"


def descubrir_tablas_parquet():
    """Escanea parquet/2023/*/*.parquet y devuelve un dict
    {clave_lower: nombre_canonico} donde nombre_canonico es el nombre del
    archivo .parquet sin extensión (que coincide con el nombre del DBF
    original usado en los TXT del diccionario)."""
    mapeo = {}
    if not PARQUET_DIR.exists():
        return mapeo
    for sub in sorted(PARQUET_DIR.iterdir()):
        if not sub.is_dir():
            continue
        for pq in sub.glob("*.parquet"):
            nombre = pq.stem  # p.ej. "Loc_P222_Inter", "Resultados_2023"
            mapeo[nombre.lower()] = nombre
    return mapeo


# Tablas de interés: se descubren dinámicamente desde el directorio parquet/2023
# para garantizar alineamiento 1:1 entre catálogo y datos disponibles.
TABLAS_INTERES = descubrir_tablas_parquet()

# Alias: nombre_parquet_lower -> lista de nombres alternativos que pueden
# aparecer en los TXT del diccionario (ej. los parquet "Docente_01" están
# documentados en el TXT como "Docentes_01").
ALIAS_TABLAS = {
    "docente_01": ["docentes_01"],
    "docente_02": ["docentes_02"],
    "docente_03": ["docentes_03"],
    "docente_04": ["docentes_04"],
}

# --------------------------------------------------------------------------- #
# Utilidades de texto                                                          #
# --------------------------------------------------------------------------- #

RE_MARCADOR_PAGINA = re.compile(r"^--- PÁGINA \d+ ---\s*$")
RE_PIE_PAGINA = re.compile(r"^MINISTERIO DE EDUCACIÓN.*$|^\s*\d+\s*$")
RE_FRASES_AÑO = re.compile(
    r'^\s*[“"].*(decenio|año del|año de la).*[”"]?\s*$', re.IGNORECASE
)

# Patrones de cabecera/inicio de tabla
RE_NOMBRE_TABLA = re.compile(
    r"^\s*(?:NOMBRE DE TABLA|Archivo(?:\s+de\s+datos)?)\s*:?\s*([A-Za-z0-9_]+)\.dbf",
    re.IGNORECASE,
)
RE_DESC_TABLA = re.compile(r"^\s*DESCRIPCIÓN DE TABLA\s*:?\s*(.*)$", re.IGNORECASE)
RE_PREGUNTA = re.compile(r"^\s*PREGUNTA\s*:?\s*(.*)$", re.IGNORECASE)

# Encabezados de columnas de una tabla
RE_HDR_VARFORMATO = re.compile(
    r"^\s*(?:Variable|Campo)\s+Formato\s+Descripci[oó]n\s+de\s+variable\s+Valor\s+de\s+variable",
    re.IGNORECASE,
)
RE_HDR_VARTIPO = re.compile(
    r"^\s*VARIABLE\s+TIPO\s+LON[G]?\s+ETIQUETA\s+VALORES",
    re.IGNORECASE,
)

# Línea de campo con formato "C (n)" / "N (n)" / "N (n,m)"
RE_CAMPO_FORMATO = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+([CN])\s*\(\s*(\d+(?:\s*,\s*\d+)?)\s*\)\s+(.*)$"
)
# Línea de campo con formato "C n" / "N n" (marco censal)
RE_CAMPO_TIPO_LONG = re.compile(
    r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+([CN])\s+(\d+)\s+(.*)$"
)

# Valor codificado "codigo: descripción" o "“codigo” : descripción"
RE_VALOR_CODIGO = re.compile(
    r'[“"]?([A-Za-z0-9]{1,6})[”"]?\s*[:\-]\s*(.+?)\s*$'
)

PLACEHOLDERS = {"999999", "999999.99999999", "Texto", "(*)", ""}


def limpiar_lineas(texto: str):
    """Devuelve la lista de líneas del texto eliminando marcadores de página,
    pies repetidos y frases protocolares."""
    salida = []
    for linea in texto.splitlines():
        if RE_MARCADOR_PAGINA.match(linea):
            continue
        if RE_PIE_PAGINA.match(linea):
            continue
        if RE_FRASES_AÑO.match(linea):
            continue
        if linea.strip() == "":
            continue
        salida.append(linea.rstrip())
    return salida


def leer(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


# --------------------------------------------------------------------------- #
# Parseo del bloque de campos de una tabla                                     #
# --------------------------------------------------------------------------- #

def _parsear_valores(texto_valor: str):
    """Convierte el contenido bruto de 'valor de variable' en dict {cod: desc}
    si encuentra el patrón 'codigo: descripcion'. Si no, devuelve el string
    limpio o None si es placeholder."""
    if not texto_valor:
        return None

    # Normalizar comillas tipográficas
    t = texto_valor.replace("“", '"').replace("”", '"').replace("’", "'")
    t = re.sub(r"\s+", " ", t).strip()

    # Intentar romper por líneas-código múltiples: separar por patrones "xx:"
    # buscando todas las apariciones de cod:desc
    codigos = {}
    # Patrón global: captura "cod" : "desc" hasta el siguiente código o fin
    matches = list(
        re.finditer(
            r'(?:"([A-Za-z0-9]{1,6})"|\b([A-Za-z0-9]{1,4}))\s*[:\-]\s*'
            r'(?=\S)',
            t,
        )
    )
    if len(matches) >= 2:
        for i, m in enumerate(matches):
            cod = m.group(1) or m.group(2)
            ini = m.end()
            fin = matches[i + 1].start() if i + 1 < len(matches) else len(t)
            desc = t[ini:fin].strip().strip('"').strip(",;").strip()
            if cod and desc:
                codigos[cod] = desc
        if codigos:
            return codigos

    # Caso simple de una sola línea "cod: desc"
    m = RE_VALOR_CODIGO.match(t)
    if m and ":" in t:
        return {m.group(1): m.group(2).strip()}

    if t in PLACEHOLDERS:
        return None
    return t or None


def _consolidar_campo(nombre, formato, descripcion, valor):
    descripcion = re.sub(r"\s+", " ", descripcion).strip()
    return {
        "formato": formato,
        "descripcion": descripcion,
        "valores": _parsear_valores(valor),
    }


def parsear_bloque_campos(lineas, formato_marco=False):
    """
    A partir de una lista de líneas (correspondientes al contenido de una tabla
    a partir de su encabezado de columnas), devuelve un dict {nombre_campo: {...}}.

    Las líneas que no inicien con un campo nuevo se acumulan en la descripción
    y el valor del último campo. Heurística simple: dividir la línea adicional
    por la primera ocurrencia que parezca un código (cod:desc) para enviar
    el lado izquierdo a la descripción y el derecho a los valores.
    """
    campos = {}
    orden = []
    actual = None  # (nombre, formato_str, [descripciones], [valores])

    def flush():
        if actual is None:
            return
        nombre, fmt, descs, vals = actual
        if nombre in campos:
            return
        desc = " ".join(d for d in descs if d).strip()
        val = "\n".join(v for v in vals if v).strip()
        campos[nombre] = _consolidar_campo(nombre, fmt, desc, val)
        orden.append(nombre)

    patron = RE_CAMPO_TIPO_LONG if formato_marco else RE_CAMPO_FORMATO

    for linea in lineas:
        m = patron.match(linea)
        if m:
            flush()
            nombre = m.group(1).upper()
            tipo = m.group(2).upper()
            longitud = re.sub(r"\s+", "", m.group(3))
            resto = m.group(4).rstrip()
            fmt = f"{tipo}({longitud})"

            # Repartir resto entre descripción y valores: heurística → si hay
            # un patrón "cod:" en la línea, el valor empieza ahí.
            desc, val = _separar_desc_valor(resto)
            actual = (nombre, fmt, [desc], [val])
        else:
            # Línea de continuación: si contiene "cod:" pertenece a valores;
            # si no, a la descripción.
            if actual is None:
                continue
            desc, val = _separar_desc_valor(linea.strip())
            if desc:
                actual[2].append(desc)
            if val:
                actual[3].append(val)

    flush()
    return campos


def _separar_desc_valor(texto):
    """Heurística que reparte una línea entre 'descripción' y 'valor'.
    Si en la línea aparece un patrón tipo `“cod” : desc` o `cod:desc`, todo
    lo que está desde ese punto se considera valor."""
    if not texto:
        return "", ""
    # Buscar primer patrón de valor codificado
    m = re.search(
        r'(?:[“"][A-Za-z0-9]{1,6}[”"]\s*:|^\s*[A-Za-z0-9]{1,4}\s*:\s)',
        texto,
    )
    if m and m.start() > 0:
        return texto[: m.start()].rstrip(), texto[m.start():].strip()
    if m and m.start() == 0:
        return "", texto.strip()
    return texto.strip(), ""


# --------------------------------------------------------------------------- #
# Extracción de tablas a partir del texto completo                             #
# --------------------------------------------------------------------------- #

def extraer_tablas_de_texto(texto: str, formato_marco=False):
    """Itera sobre 'texto' identificando bloques de tablas DBF.
    Devuelve dict {nombre_dbf_sin_ext: {descripcion, pregunta, campos}}.
    Si una misma tabla aparece varias veces, fusiona los campos (sin
    sobreescribir los ya existentes)."""
    lineas = limpiar_lineas(texto)

    tablas = {}
    i = 0
    n = len(lineas)

    # Estado actual
    nombre_actual = None
    descripcion_actual = ""
    pregunta_actual = ""
    buffer_campos = []
    en_tabla = False  # True después de haber leído el encabezado de columnas

    def cerrar_tabla():
        nonlocal nombre_actual, descripcion_actual, pregunta_actual
        nonlocal buffer_campos, en_tabla
        if nombre_actual and buffer_campos:
            campos = parsear_bloque_campos(buffer_campos, formato_marco=formato_marco)
            slot = tablas.setdefault(
                nombre_actual,
                {"descripcion": "", "pregunta": "", "campos": {}},
            )
            if descripcion_actual and not slot["descripcion"]:
                slot["descripcion"] = descripcion_actual.strip()
            if pregunta_actual and not slot["pregunta"]:
                slot["pregunta"] = pregunta_actual.strip()
            for k, v in campos.items():
                slot["campos"].setdefault(k, v)
        buffer_campos = []
        en_tabla = False

    while i < n:
        linea = lineas[i]

        m = RE_NOMBRE_TABLA.match(linea)
        if m:
            cerrar_tabla()
            nombre_actual = m.group(1)
            descripcion_actual = ""
            pregunta_actual = ""
            i += 1
            continue

        if nombre_actual is None:
            i += 1
            continue

        m = RE_DESC_TABLA.match(linea)
        if m and not en_tabla:
            descripcion_actual = m.group(1).strip()
            # Continuar añadiendo líneas hasta encontrar 'PREGUNTA' o encabezado
            j = i + 1
            while j < n:
                nxt = lineas[j]
                if (
                    RE_PREGUNTA.match(nxt)
                    or RE_HDR_VARFORMATO.match(nxt)
                    or RE_HDR_VARTIPO.match(nxt)
                    or RE_NOMBRE_TABLA.match(nxt)
                ):
                    break
                descripcion_actual += " " + nxt.strip()
                j += 1
            i = j
            continue

        m = RE_PREGUNTA.match(linea)
        if m and not en_tabla:
            pregunta_actual = m.group(1).strip()
            i += 1
            continue

        if RE_HDR_VARFORMATO.match(linea) or RE_HDR_VARTIPO.match(linea):
            en_tabla = True
            i += 1
            continue

        if en_tabla:
            buffer_campos.append(linea)

        i += 1

    cerrar_tabla()
    return tablas


# --------------------------------------------------------------------------- #
# Campos generales                                                             #
# --------------------------------------------------------------------------- #

def extraer_campos_generales_marco(texto_marco: str):
    """En el marco censal, la tabla PADRON.dbf (encabezado
    VARIABLE TIPO LON ETIQUETA VALORES FTE) reúne las variables generales."""
    tablas = extraer_tablas_de_texto(texto_marco, formato_marco=True)
    padron = tablas.get("PADRON") or tablas.get("Padron") or {}
    return padron.get("campos", {}), padron


# --------------------------------------------------------------------------- #
# Construcción del catálogo                                                    #
# --------------------------------------------------------------------------- #

def construir_catalogo():
    txt_marco = leer(ARCHIVO_MARCO)
    txt_ce = leer(ARCHIVO_CE)
    txt_res = leer(ARCHIVO_RES)
    txt_le = leer(ARCHIVO_LE)

    # Campos generales: del marco censal (sólo las variables comunes a la
    # identificación del servicio educativo).
    campos_generales, padron_marco = extraer_campos_generales_marco(txt_marco)

    # Extraer tablas de cada documento. Para el marco censal, formato distinto.
    tablas_marco = extraer_tablas_de_texto(txt_marco, formato_marco=True)
    tablas_ce = extraer_tablas_de_texto(txt_ce, formato_marco=False)
    tablas_res = extraer_tablas_de_texto(txt_res, formato_marco=False)
    tablas_le = extraer_tablas_de_texto(txt_le, formato_marco=False)

    # Fusionar resultados, priorizando: específico > marco
    fuentes = [tablas_marco, tablas_ce, tablas_res, tablas_le]

    tablas_finales = {}
    for clave_parquet, nombre_canonico in TABLAS_INTERES.items():
        claves_busqueda = {clave_parquet, *ALIAS_TABLAS.get(clave_parquet, [])}
        encontrada = None
        for fuente in fuentes:
            # buscar por coincidencia case-insensitive
            for k, v in fuente.items():
                if k.lower() in claves_busqueda:
                    if encontrada is None:
                        encontrada = {
                            "descripcion": v.get("descripcion", ""),
                            "pregunta": v.get("pregunta", ""),
                            "campos": dict(v.get("campos", {})),
                        }
                    else:
                        if v.get("descripcion") and not encontrada["descripcion"]:
                            encontrada["descripcion"] = v["descripcion"]
                        if v.get("pregunta") and not encontrada["pregunta"]:
                            encontrada["pregunta"] = v["pregunta"]
                        for nc, datos in v.get("campos", {}).items():
                            encontrada["campos"].setdefault(nc, datos)
        if encontrada is not None:
            tablas_finales[nombre_canonico] = encontrada
        else:
            print(f"[WARN] Tabla no encontrada en los TXT: {clave_parquet}")

    catalogo = {
        "2023": {
            "campos_generales": campos_generales,
            "tablas": tablas_finales,
        }
    }
    return catalogo


def main():
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    catalogo = construir_catalogo()

    with SALIDA.open("w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)

    # Resumen en consola
    info = catalogo["2023"]
    print(f"Catálogo guardado en: {SALIDA}")
    print(f"  Campos generales:  {len(info['campos_generales'])} variables")
    print(f"  Tablas procesadas: {len(info['tablas'])}")
    for nombre, datos in info["tablas"].items():
        print(f"    - {nombre}: {len(datos['campos'])} campos")


if __name__ == "__main__":
    main()
