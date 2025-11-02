# src/agent/scraper/lecturas_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_lecturas(url: str) -> str:
    """
    Extrae el texto completo de horóscopos desde lecturas.com,
    filtrando menús, enlaces y publicidad.
    Devuelve un texto limpio con todos los signos.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    container = soup.select_one("div.column-left") or soup

    for ad in container.select(
        ".ad, .related, .article-tags, .author, .video, script, style, .promo, .link, .recommended"
    ):
        ad.decompose()

    TAGS_TEXT = [
        "p", "h1", "h2", "h3", "h4", "h5", "h6",
        "strong", "b", "em", "i", "u",
        "span", "a", "blockquote", "li", "div"
    ]

    elements = container.find_all(TAGS_TEXT)
    texts = [el.get_text(" ", strip=True) for el in elements if el.get_text(strip=True)]

    cleaned = [
        t for t in texts
        if len(t.split()) > 5
        and not any(x in t.lower() for x in [
            "leer también", "puedes seguir", "síguenos", "haz clic", "suscríbete"
        ])
    ]

    return "\n".join(cleaned).strip()
