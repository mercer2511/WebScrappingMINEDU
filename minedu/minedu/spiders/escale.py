import html
import os
import re
from urllib.parse import unquote, urlparse

import scrapy


class EscaleSpider(scrapy.Spider):
    name = "escale"
    allowed_domains = ["escale.minedu.gob.pe"]

    folder_ids = {
        "2023": "8520583",
        "2024": "9538443",
        "2025": "10632985",
    }

    start_urls = [
        f"https://escale.minedu.gob.pe/uee/-/document_library_display/GMv7/view/{folder_id}"
        for folder_id in folder_ids.values()
    ]

    def parse(self, response):
        folder_id = self.get_folder_id(response.url)
        year = self.get_year_from_folder_id(folder_id)

        rows = response.css("tr.portlet-section-body, tr.portlet-section-alternate")

        for row in rows:
            filename = row.css("span.taglib-text::text").get()
            detail_url = row.css("a::attr(href)").get()

            if not filename or not detail_url:
                continue

            filename = self.clean_filename(filename.strip())
            detail_url = html.unescape(detail_url)
            detail_url = response.urljoin(detail_url)

            yield scrapy.Request(
                detail_url,
                callback=self.parse_detail,
                meta={
                    "year": year,
                    "filename": filename,
                    "detail_url": detail_url,
                },
            )

        next_page = response.css("div.page-links a.next::attr(href)").get()

        if next_page:
            next_page = html.unescape(next_page)
            next_page = response.urljoin(next_page)

            yield scrapy.Request(
                next_page,
                callback=self.parse,
            )

    def parse_detail(self, response):
        year = response.meta["year"]
        filename = response.meta["filename"]
        detail_url = response.meta["detail_url"]

        download_url = response.css(
            "div.lfr-asset-summary a[href*='/documents/']::attr(href)"
        ).get()

        if not download_url:
            download_url = response.css(
                "div.lfr-asset-name a[href*='/documents/']::attr(href)"
            ).get()

        if not download_url:
            download_url = response.css(
                "a[href$='.zip']::attr(href), a[href$='.pdf']::attr(href)"
            ).get()

        if download_url:
            download_url = response.css(
                "a[href$='.zip']::attr(href), a[href$='.pdf']::attr(href)"
            ).get()

        if not download_url:
            yield {
                "año": year,
                "nombre_archivo": filename,
                "url_detalle": detail_url,
                "url_descarga": None,
                "descargado": False,
                "error": "No se encontró URL de descarga",
            }
            return

        download_url = html.unescape(download_url)
        download_url = response.urljoin(download_url)

        folder = os.path.join("descargas", year)
        os.makedirs(folder, exist_ok=True)

        yield scrapy.Request(
            download_url,
            callback=self.save_file,
            meta={
                "year": year,
                "filename": filename,
                "folder": folder,
                "detail_url": detail_url,
                "download_url": download_url,
            },
        )

    def save_file(self, response):
        year = response.meta["year"]
        filename = response.meta["filename"]
        folder = response.meta["folder"]
        detail_url = response.meta["detail_url"]
        download_url = response.meta["download_url"]

        content_type = response.headers.get("Content-Type", b"").decode().lower()

        if "text/html" in content_type:
            yield {
                "año": year,
                "nombre_archivo": filename,
                "url_detalle": detail_url,
                "url_descarga": download_url,
                "descargado": False,
                "error": "La respuesta fue HTML, no un archivo",
            }
            return

        filename = self.ensure_extension(filename, response.url)

        filepath = os.path.join(folder, filename)
        filepath = self.get_unique_filepath(filepath)

        with open(filepath, "wb") as file:
            file.write(response.body)

        yield {
            "año": year,
            "nombre_archivo": filename,
            "url_detalle": detail_url,
            "url_descarga": download_url,
            "ruta": filepath,
            "tamaño_bytes": len(response.body),
            "descargado": True,
        }

    def clean_filename(self, filename):
        filename = filename.strip()
        filename = re.sub(r'[\\/:*?"<>|]', "_", filename)
        filename = re.sub(r"\s+", " ", filename)
        return filename

    def ensure_extension(self, filename, url):
        lower_filename = filename.lower()

        if lower_filename.endswith((".zip", ".pdf")):
            return filename

        path = unquote(urlparse(url).path).lower()

        if path.endswith(".zip"):
            return f"{filename}.zip"

        if path.endswith(".pdf"):
            return f"{filename}.pdf"

        return filename

    def get_unique_filepath(self, filepath):
        if not os.path.exists(filepath):
            return filepath

        folder = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        name, extension = os.path.splitext(filename)

        counter = 1

        while True:
            new_filepath = os.path.join(folder, f"{name}_{counter}{extension}")

            if not os.path.exists(new_filepath):
                return new_filepath

            counter += 1

    def get_folder_id(self, url):
        parts = url.split("/view/")

        if len(parts) < 2:
            return None

        return parts[1].split("/")[0].split("?")[0]

    def get_year_from_folder_id(self, folder_id):
        for year, current_folder_id in self.folder_ids.items():
            if current_folder_id == folder_id:
                return year

        return None