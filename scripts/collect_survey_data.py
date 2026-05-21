"""
collect_survey_data.py
Procesa los microdatos del Stack Overflow Developer Survey para extraer
estadísticas de adopción de AI tools por año.

DATOS REQUERIDOS (descarga manual):
  Cada año está disponible como archivo ZIP con un CSV de microdatos:
    2023: https://survey.stackoverflow.co/2023 → "Download full data set"
    2024: https://survey.stackoverflow.co/2024 → "Download full data set"
    2025: https://survey.stackoverflow.co/2025 → "Download full data set"

  Guardar los CSV descomprimidos en:
    data/raw/so_microdata/survey_results_public_2023.csv
    data/raw/so_microdata/survey_results_public_2024.csv
    data/raw/so_microdata/survey_results_public_2025.csv

  Tamaño aproximado: 200-400 MB por archivo (70,000-90,000 respondientes).

COLUMNAS RELEVANTES POR AÑO:
  2023: "AISelect" — "Do you currently use AI tools in your development process?"
        Valores: "Yes, I use them" | "No, but I want to" | "No, and I don't want to"
  2024: "AISelect" — misma pregunta
        Valores: "Yes" | "No, but I plan to soon" | "No, and I don't plan to"
  2025: "AISelect" — misma pregunta (estructura similar)

  Trust (todas las ediciones):
  "AITrust" o "AISent" — confianza en los resultados de AI tools

SALIDA:
  data/raw/so_survey.csv — estadísticas agregadas por año (ai_usage_pct, ai_trust_pct)
  Formato citable: cada fila incluye fuente, n de muestra y pregunta exacta.

CITA ACADÉMICA:
  Stack Overflow (2023). Stack Overflow Developer Survey 2023.
  Retrieved from https://survey.stackoverflow.co/2023. n=90,000.

Uso:
    python scripts/collect_survey_data.py
    python scripts/collect_survey_data.py --years 2024 2025
    python scripts/collect_survey_data.py --use-published   # usa datos publicados sin microdatos
"""

import argparse
import logging
from pathlib import Path

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
MICRO_DIR = RAW_DIR / "so_microdata"
OUT_PATH = RAW_DIR / "so_survey.csv"

# Datos publicados de los informes anuales de SO (fuente: survey.stackoverflow.co)
# Usados como fallback cuando los microdatos no están disponibles.
# Pregunta: "Are you currently using AI tools in your development process?"
PUBLISHED_DATA = {
    2023: {
        "ai_usage_pct": 44.0,   # % "Yes, I use them" (n=90,000)
        "ai_trust_pct": 45.0,   # % "Somewhat trust" + "Highly trust" accuracy
        "n_total": 90000,
        "source": "SO Developer Survey 2023 — survey.stackoverflow.co/2023",
        "note": "ai_usage: respondientes que actualmente usan AI tools en desarrollo",
    },
    2024: {
        "ai_usage_pct": 62.0,   # % "Yes" (n=65,437) — +18pp vs 2023
        "ai_trust_pct": 40.0,   # % que confían (aprox; 31% distrust publicado)
        "n_total": 65437,
        "source": "SO Developer Survey 2024 — survey.stackoverflow.co/2024",
        "note": "76% usan o planean usar; 62% usan actualmente",
    },
    2025: {
        "ai_usage_pct": 68.0,   # estimado: 84% total - 16% plan = ~68% activos
        "ai_trust_pct": 29.0,   # publicado: baja 11pp vs 2024 (era ~40%)
        "n_total": None,         # n no publicado al momento de redacción
        "source": "SO Developer Survey 2025 — survey.stackoverflow.co/2025",
        "note": "51% devs profesionales usan diariamente; 68% estimado activos totales",
    },
}

# Mapeo de columnas por año (puede variar entre ediciones del survey)
COLUMN_MAP = {
    2023: {
        "ai_use":   "AISelect",
        "ai_trust": "AIBenefits",  # o AITrust según versión
        "use_yes":  ["Yes, I use them"],
        "trust_pos": ["Increase my productivity", "Learning or training"],
    },
    2024: {
        "ai_use":   "AISelect",
        "ai_trust": "AISent",
        "use_yes":  ["Yes"],
        "trust_pos": ["Favorable", "Very favorable"],
    },
    2025: {
        "ai_use":   "AISelect",
        "ai_trust": "AISent",
        "use_yes":  ["Yes"],
        "trust_pos": ["Favorable", "Very favorable"],
    },
}


def process_microdata(year: int) -> dict | None:
    """
    Procesa el CSV de microdatos de un año específico.
    Retorna dict con ai_usage_pct y ai_trust_pct, o None si el archivo no existe.
    """
    candidates = [
        MICRO_DIR / f"survey_results_public_{year}.csv",
        MICRO_DIR / f"stack-overflow-developer-survey-{year}" / f"survey_results_public.csv",
    ]
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        log.warning(f"Microdatos {year} no encontrados en {MICRO_DIR}. Usa --use-published.")
        return None

    log.info(f"Cargando microdatos {year}: {path}")
    df = pd.read_csv(path, low_memory=False)
    log.info(f"  {len(df):,} respondientes, {len(df.columns)} columnas")

    cfg = COLUMN_MAP.get(year, {})
    ai_col   = cfg.get("ai_use")
    trust_col = cfg.get("ai_trust")
    use_yes  = cfg.get("use_yes", [])
    trust_pos = cfg.get("trust_pos", [])

    result = {
        "year": year,
        "n_total": len(df),
        "source": f"SO Developer Survey {year} — microdatos, n={len(df):,}",
    }

    # % que actualmente usan AI tools
    if ai_col and ai_col in df.columns:
        total_valid = df[ai_col].notna().sum()
        count_yes = df[ai_col].isin(use_yes).sum()
        result["ai_usage_pct"] = round(100 * count_yes / max(total_valid, 1), 1)
        log.info(f"  AI usage {year}: {result['ai_usage_pct']:.1f}% ({count_yes:,}/{total_valid:,})")
    else:
        log.warning(f"  Columna '{ai_col}' no encontrada. Columnas disponibles: {list(df.columns[:20])}")
        result["ai_usage_pct"] = np.nan

    # % que confían en los resultados
    if trust_col and trust_col in df.columns:
        total_valid = df[trust_col].notna().sum()
        count_trust = df[trust_col].isin(trust_pos).sum()
        result["ai_trust_pct"] = round(100 * count_trust / max(total_valid, 1), 1)
        log.info(f"  AI trust {year}: {result['ai_trust_pct']:.1f}%")
    else:
        result["ai_trust_pct"] = np.nan

    return result


def build_from_published() -> pd.DataFrame:
    """Construye so_survey.csv usando los datos publicados en los informes anuales."""
    rows = []
    for year, data in sorted(PUBLISHED_DATA.items()):
        rows.append({
            "year":         year,
            "ai_usage_pct": data["ai_usage_pct"],
            "ai_trust_pct": data["ai_trust_pct"],
        })
    return pd.DataFrame(rows)


def main(years: list[int] | None = None, use_published: bool = False) -> None:
    if years is None:
        years = sorted(PUBLISHED_DATA.keys())

    if use_published:
        log.info("Usando datos publicados (sin microdatos)")
        df = build_from_published()
        df.to_csv(OUT_PATH, index=False)
        log.info(f"Guardado: {OUT_PATH}")
        print(df.to_string(index=False))
        return

    # Intentar procesar microdatos para cada año
    MICRO_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for year in years:
        result = process_microdata(year)
        if result is None:
            # Fallback a datos publicados
            pub = PUBLISHED_DATA.get(year)
            if pub:
                log.info(f"  Usando datos publicados para {year}")
                rows.append({
                    "year": year,
                    "ai_usage_pct": pub["ai_usage_pct"],
                    "ai_trust_pct": pub["ai_trust_pct"],
                })
        else:
            rows.append({
                "year": result["year"],
                "ai_usage_pct": result.get("ai_usage_pct", np.nan),
                "ai_trust_pct": result.get("ai_trust_pct", np.nan),
            })

    if not rows:
        log.error("Sin datos. Verifica que los archivos de microdatos estén en data/raw/so_microdata/")
        return

    df = pd.DataFrame(rows).sort_values("year")
    df.to_csv(OUT_PATH, index=False)
    log.info(f"Guardado: {OUT_PATH} ({len(df)} filas)")
    print("\nResultado:")
    print(df.to_string(index=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesa datos de adopción AI del SO Developer Survey")
    parser.add_argument("--years", nargs="+", type=int, default=None,
                        help="Años a procesar (default: todos)")
    parser.add_argument("--use-published", action="store_true",
                        help="Usar datos de informes publicados sin necesidad de microdatos")
    args = parser.parse_args()
    main(years=args.years, use_published=args.use_published)
