# src/agent/scraper/scraper_manager.py
import time
from datetime import datetime
from pathlib import Path
from .hola_scraper import scrape_hola
from .veinte_scraper import scrape_veinte
from .lecturas_scraper import scrape_lecturas


class ScraperManager:
    def __init__(self, save_dir="data/raw"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

        # ✅ URLs fijas
        self.urls = {
            "hola": {
                "2025-10-31": "https://www.hola.com/horoscopo/20251031862743/horoscopo-de-hoy-viernes-31-de-octubre/",
                "2025-10-30": "https://www.hola.com/horoscopo/20251030862741/horoscopo-de-hoy-jueves-30-de-octubre/",
                "2025-10-29": "https://www.hola.com/horoscopo/20251029862740/horoscopo-de-hoy-miercoles-29-de-octubre/"
            },
            "20minutos": {
                "2025-10-31": "https://www.20minutos.es/gente/horoscopo-viernes-31-octubre-2025_6663148_0.html",
                "2025-10-30": "https://www.20minutos.es/gente/horoscopo-jueves-30-octubre-2025_6662667_0.html",
                "2025-10-29": "https://www.20minutos.es/gente/horoscopo-miercoles-29-octubre-2025_6662203_0.html"
            },
            "lecturas": {
                "2025-10-31": "https://www.lecturas.com/horoscopo/horoscopo-fin-semana-31-octubre-2-noviembre-2025-asi-les-ira-a-signos-zodiaco-amor-dinero-y-salud_183477",
                "2025-10-30": "https://www.lecturas.com/horoscopo/horoscopo-hoy-jueves-30-octubre-prediccion-gratis-horoscopo-diario_183560",
                "2025-10-29": "https://www.lecturas.com/horoscopo/miercoles-29-octubre-horoscopo-hoy-sobre-salud-amor-y-trabajo-tu-prediccion-diaria-gratis_183496"
            }
        }

    def scrape_day(self, site: str, date_str: str):
        """Descarga y guarda el horóscopo completo de un sitio y fecha específica."""
        save_path = self.save_dir / site / date_str
        save_path.mkdir(parents=True, exist_ok=True)

        try:
            url = self.urls[site][date_str]
            print(f"\n🔗 Scrapeando {site} ({date_str}) → {url}")

            # Seleccionar scraper adecuado
            if site == "hola":
                text = scrape_hola(url)
            elif site == "20minutos":
                text = scrape_veinte(url)
            elif site == "lecturas":
                text = scrape_lecturas(url)
            else:
                raise ValueError(f"Sitio no reconocido: {site}")

            file_path = save_path / "all_signs.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"✅ Guardado: {file_path} ({len(text)} chars)")
            time.sleep(1.5)

        except Exception as e:
            print(f"❌ Error en {site} ({date_str}): {e}")
