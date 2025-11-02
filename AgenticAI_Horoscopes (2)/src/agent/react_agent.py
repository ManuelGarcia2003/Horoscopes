import os
import json
from datetime import datetime
from pathlib import Path
from src.agent.summarizer import Summarizer
from  src.agent.scraper.splitter import split_by_sign, split_with_llm

class ReActAgent:
    """
    Agente ReAct mínimo: ejecuta scrape() + summarize()
    para cada intérprete, fecha y signo detectado.
    """

    def __init__(self, raw_dir="data/raw", summaries_dir="data/summaries", model="gpt-4o-mini"):
        self.raw_dir = Path(raw_dir)
        self.summaries_dir = Path(summaries_dir)
        self.summaries_dir.mkdir(parents=True, exist_ok=True)

        self.summarizer = Summarizer(model_name=model, provider="openai")

    # ==========================================================
    # Función interna para leer el texto base (scrapeado)
    # ==========================================================
    def _get_raw_text(self, interpreter: str, date: str) -> str:
        """Busca el archivo all_signs.txt para el intérprete y fecha."""
        path = self.raw_dir / interpreter / date / "all_signs.txt"
        if not path.exists():
            raise FileNotFoundError(f"⚠️ No se encontró el archivo: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # ==========================================================
    # Pipeline principal ReAct
    # ==========================================================
    def run(self, interpreter: str, date: str):
        """
        Ejecuta el pipeline completo para un intérprete y fecha:
        1. Lee el texto raw.
        2. Divide por signo (regex → fallback LLM).
        3. Genera y guarda resúmenes JSON por signo.
        4. Guarda log de pensamiento y acciones.
        """
        log = {
            "interpreter": interpreter,
            "date": date,
            "timestamp": datetime.now().isoformat(),
            "thoughts": [],
            "actions": [],
            "observations": [],
        }

        try:
            # === Acción 1: Obtener texto ===
            log["thoughts"].append(f"Necesito el texto del horóscopo de {interpreter} ({date}).")
            raw_text = self._get_raw_text(interpreter, date)
            log["actions"].append(f"Lectura del archivo raw.")
            log["observations"].append(f"Texto obtenido ({len(raw_text)} caracteres).")

            # === Acción 2: Dividir por signo ===
            log["thoughts"].append("Dividir el texto en secciones por signo zodiacal.")
            sign_texts = split_by_sign(raw_text)

            if len(sign_texts) < 6:
                log["observations"].append(
                    f"Solo se detectaron {len(sign_texts)} signos, usando LLM como fallback."
                )
                sign_texts = split_with_llm(raw_text)
            else:
                log["observations"].append(f"Se detectaron {len(sign_texts)} signos por regex.")

            # === Acción 3: Generar resúmenes por signo ===
            for sign, txt in sign_texts.items():
                log["thoughts"].append(f"Resumir el signo {sign}.")
                summary = self.summarizer.summarize(txt, sign, date, interpreter)
                self.summarizer.save_summary(summary)
                log["observations"].append(f"✅ Resumen generado para {sign} ({len(txt)} chars).")

            log["final_answer"] = f"Resúmenes generados correctamente para {interpreter} ({len(sign_texts)} signos)."

        except Exception as e:
            log["final_answer"] = f"❌ Error: {str(e)}"

        # === Guardar log del agente ===
        log_path = Path("data/logs") / f"react_log_{interpreter}_{date}.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)

        print(f"🧠 Log guardado en {log_path}")
        return log
