from pathlib import Path
import os, json
from openai import OpenAI
from datetime import datetime

class Summarizer:
    def __init__(self, model_name="gpt-4o-mini", provider="openai"):
        self.model_name = model_name
        self.provider = provider
        self.client = OpenAI(api_key="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")  # tu clave aquí

    def summarize(self, raw_text: str, sign: str, date: str, interpreter: str) -> dict:
        prompt = f"""Summarize this horoscope for {sign} on {date} by {interpreter}.
        Structure: tone, facets (love, career, health), key_points, final_summary.
        Text: {raw_text[:4000]}"""

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are an expert in summarize horoscopes into JSON."},
                {"role": "user", "content": prompt}
            ],
        )

        content = response.choices[0].message.content
        try:
            summary_json = json.loads(content)
        except:
            summary_json = {"raw": content}

        summary_json.update({
            "sign": sign,
            "date": date,
            "interpreter": interpreter,
            "model": self.model_name,
            "timestamp": datetime.now().isoformat()
        })
        return summary_json

    def save_summary(self, summary_json: dict, save_dir="data/summaries"):
        # 🔧 FIX: obtener ruta absoluta de la raíz del proyecto
        project_root = Path(__file__).resolve().parents[2]  # sube desde src/agent/
        save_path = project_root / save_dir
        save_path.mkdir(parents=True, exist_ok=True)

        filename = f"{summary_json['interpreter']}_{summary_json['sign']}_{summary_json['date']}.json"
        file_path = save_path / filename

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(summary_json, f, indent=2, ensure_ascii=False)

        print(f"✅ Guardado en {file_path}")
        return str(file_path)
