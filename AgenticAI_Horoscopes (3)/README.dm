Para ejecutar todo el proyecto hay que descargar la carpeta AgenticAI_Horoscopes.
1. Debemos de ir a la carpeta llamada 'notebooks'
2. Hay cuatro notebooks, se deben ejecutar en el siguiente orden:
  2.1 Part0
  2.2 PartA
  2.3 PartB
  2.4 PartC

El notebook Part0 y PartA, usan archivos .py que contienen funciones de scrapping y summarize, estos archivos .py estan en la carpeta src/agent y src/agent/scraper, el funcionamient 
de cada uno de estos .py es el siguiente: 

  ## Archivos `.py` y para qué sirven

### 1. `src/agent/scraper/hola_scraper.py`
- **Función:** descarga y limpia el horóscopo de **hola.com** para una fecha dada; extrae los tags más comunes (`h1..h6`, `p`, `li`, `span`, `a`) y devuelve el texto largo.
- **Lo usa:** (Parte 0) para guardar `data/raw/hola/<fecha>/all_signs.txt`.

### 2. `src/agent/scraper/veinte_scraper.py`
- **Función:** hace scraping de **20minutos.es** usando las URLs fijas que ya pusiste (porque la página cambia el patrón); también devuelve el texto completo del día.
- **Lo usa:**  (Parte 0) para guardar `data/raw/20minutos/<fecha>/all_signs.txt`.

### 3. `src/agent/scraper/lecturas_scraper.py`
- **Función:** obtiene el horóscopo de **lecturas.com** para el día indicado; limpia encabezados y párrafos.
- **Lo usa:**  (Parte 0) para guardar `data/raw/lecturas/<fecha>/all_signs.txt`.

### 4. `src/agent/scraper/splitter.py`
- **Función:** recibe el **texto largo** de un sitio/día (el `all_signs.txt`) y lo intenta **dividir en los 12 signos**.  
  - Primero intenta con regex sobre el texto normalizado (para agarrar “aries”, “Aries”, “ARIES:”, etc.).
  - Si no encuentra todos, puede usar la versión con LLM para que el modelo regrese un JSON `{signo: texto}`.
- **Lo usa:**  (Parte A) y también tu `react_agent.py`.

### 5. `src/agent/summarizer.py`
- **Función:** encapsula la llamada al modelo (OpenAI / Gemini / lo que configures) para convertir el texto de **un solo signo** en un **resumen estructurado** con:
  - `tone`
  - `facets` → `love`, `career`, `health`
  - `key_points`
  - `final_summary`
  y le agrega metadatos (`sign`, `date`, `interpreter`, `model`).
- **Lo usa:**  (Parte A) para generar los JSON en `data/summaries/`.

### 6. `src/agent/react_agent.py`
- **Función:** es el **orquestador ReAct**. Hace:
  1. “pienso qué necesito” (`thought`)
  2. “ejecuto scrape” (leer de `data/raw/...`)
  3. “observo el texto” (`observation`)
  4. “divido por signo” (usa `splitter.py`)
  5. “resumo cada signo” (usa `summarizer.py`)
  6. “guardo los JSON” (`data/summaries/...`)
  7. “escribo el log” (`data/logs/...`)
- **Lo usa:**  (Parte A) para mostrar que sí hay agente con `thought → action → observation → final_answer`.

### 7. `src/agent/scraper/scraper_manager.py` *(si lo dejaste)*
- **Función:** centraliza las URLs fijas y las rutas de guardado para no repetir lógica en cada scraper.
- **Lo usa:** principalmente `00_scrape_data.ipynb` cuando quieres bajar los 3 sitios y los 3 días en un solo ciclo.
