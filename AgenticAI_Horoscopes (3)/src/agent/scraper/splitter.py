import re
from unidecode import unidecode
import json
import os

# ----------------------------------------------------------
# Lista de signos zodiacales
# ----------------------------------------------------------
ZODIAC_SIGNS = [
    "aries", "tauro", "geminis", "cancer", "leo", "virgo",
    "libra", "escorpio", "sagitario", "capricornio", "acuario", "piscis"
]

# ----------------------------------------------------------
# Funciones auxiliares
# ----------------------------------------------------------
def normalize(text: str) -> str:
    """Convierte texto a minúsculas y sin acentos para facilitar coincidencias."""
    return unidecode(text.lower())

# ----------------------------------------------------------
# Splitter basado en regex (sin API)
# ----------------------------------------------------------
def split_by_sign(raw_text: str) -> dict:
    """
    Divide el texto completo en secciones por signo zodiacal.
    Usa coincidencias insensibles a mayúsculas, acentos y símbolos.
    """
    text_norm = normalize(raw_text)

    # patrón flexible: busca el nombre del signo seguido de :, -, o salto
    pattern = r"\b(" + "|".join(ZODIAC_SIGNS) + r")[\s:–-]"
    matches = list(re.finditer(pattern, text_norm, re.IGNORECASE))

    if not matches:
        print("⚠️ No se detectaron signos, devolviendo texto general.")
        return {"general": raw_text.strip()}

    sign_sections = {}
    for i, match in enumerate(matches):
        sign = match.group(1).capitalize()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text_norm)
        segment = raw_text[start:end].strip()
        sign_sections[sign] = segment

    return sign_sections


# ----------------------------------------------------------
# Splitter asistido por modelo (usando OpenAI)
# ----------------------------------------------------------
def split_with_llm(raw_text: str, model="gpt-4o-mini") -> dict:
    """
    Usa un modelo LLM (GPT o Gemini) para dividir el texto en 12 secciones por signo.
    Solo usar si el texto no tiene separadores claros.
    """
    try:
        from openai import OpenAI
    except ImportError:
        print("❌ openai no está instalado. Ejecuta: pip install openai")
        return {"general": raw_text.strip()}

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ No se encontró la variable OPENAI_API_KEY en el entorno.")
        return {"general": raw_text.strip()}

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Divide el siguiente texto de horóscopos en 12 secciones (una por cada signo zodiacal):
    Aries, Tauro, Géminis, Cáncer, Leo, Virgo, Libra, Escorpio, Sagitario, Capricornio, Acuario y Piscis.

    Devuelve un JSON con formato:
    {{
      "Aries": "...",
      "Tauro": "...",
      ...
      "Piscis": "..."
    }}

    Texto:
    {raw_text[:12000]}
    """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content.strip()

        # Limpieza de bordes tipo ```json ... ```
        content = content.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(content)
        print("✅ División asistida por modelo completada.")
        return parsed

    except Exception as e:
        print(f"⚠️ Error al usar el modelo para dividir texto: {e}")
        return {"general": raw_text.strip()}
