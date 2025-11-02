# src/agent/scraper/veinte_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_veinte(url: str) -> str:
    """
    Extrae el texto real del horóscopo de 20minutos.es,
    ignorando menús, comentarios y bloques externos.
    Usa un rango amplio de etiquetas HTML relevantes.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    container = soup.select_one("div.gente-body") or soup

    for ad in container.select(
        ".article-related, .article-tags, .social, .article-media, script, style, .enlace, .video"
    ):
        ad.decompose()

    TAGS_TEXT = [
        "p", "h1", "h2", "h3", "h4", "h5", "h6",
        "strong", "b", "em", "i", "u",
        "span", "a", "blockquote", "li", "div"
    ]

    elements = container.find_all(TAGS_TEXT)
    texts = [el.get_text(" ", strip=True) for el in elements if el.get_text(strip=True)]

    seen = set()
    cleaned = []
    for t in texts:
        t_lower = t.lower()
        if t_lower not in seen and len(t.split()) > 5:
            seen.add(t_lower)
            cleaned.append(t)

    return "\n".join(cleaned).strip()
