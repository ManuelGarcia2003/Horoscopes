# src/agent/scraper/hola_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_hola(url: str) -> str:
    """
    Extrae el texto real del horóscopo desde hola.com,
    ignorando publicidad o artículos relacionados.
    Devuelve todo el texto concatenado (sin dividir por signo).
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    # ✅ Buscar el contenedor principal de texto
    container = soup.select_one("div.texto-noticia") or soup

    # ❌ Excluir secciones irrelevantes
    for ad in container.select(".bloqueRelacionado, .bloqueRecetas, .bloquePublicidad"):
        ad.decompose()

    # ✅ Extraer solo los párrafos y títulos
    elements = container.find_all(["p", "h1", "h2", "h3", "h4", "h5", "strong", "b", "em", "span"])
    texts = [el.get_text(" ", strip=True) for el in elements if el.get_text(strip=True)]

    # 🔎 Filtrar texto útil (descartar frases genéricas)
    cleaned = [
        t for t in texts
        if not t.lower().startswith("si estás embarazada") and len(t.split()) > 5
    ]

    return "\n".join(cleaned).strip()
