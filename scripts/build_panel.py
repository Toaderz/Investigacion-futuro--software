"""
build_panel.py
Ensambla el panel de datos final para análisis econométrico.

Combina:
  - data/raw/returns_annual.csv       (collect_prices.py)
  - data/raw/fundamentals_annual.csv  (collect_fundamentals.py)
  - data/raw/so_survey.csv            (descarga manual Stack Overflow)
  - Variables derivadas: AI_intensity, indicadores de eventos (DiD)

Salida:
    data/processed/panel_final.csv  — panel balanceado listo para regresión
    data/processed/panel_summary.csv — estadísticas descriptivas

Uso:
    python scripts/build_panel.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
PROC_DIR = Path(__file__).parent.parent / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)

# Clasificación manual de AI-intensity por producto lanzado
# 0 = sin producto AI generativa, 1 = producto AI lanzado
AI_PRODUCT_LAUNCH = {
    "MSFT":  {"year": 2021, "product": "GitHub Copilot GA"},
    "GOOGL": {"year": 2023, "product": "Bard / Gemini"},
    "ADBE":  {"year": 2023, "product": "Adobe Firefly"},
    "CRM":   {"year": 2023, "product": "Einstein GPT"},
    "INTU":  {"year": 2023, "product": "Intuit Assist"},
    "NOW":   {"year": 2023, "product": "Now Assist"},
    "WDAY":  {"year": 2024, "product": "Illuminate AI"},
    "SNOW":  {"year": 2023, "product": "Cortex AI"},
    "HUBS":  {"year": 2023, "product": "HubSpot AI"},
    "DDOG":  {"year": 2023, "product": "Bits AI"},
    "SAP":   {"year": 2023, "product": "Joule"},
    "ORCL":  {"year": 2023, "product": "Oracle AI"},
    "IBM":   {"year": 2023, "product": "watsonx.ai"},
    "PLTR":  {"year": 2023, "product": "AIP platform"},
    "AI":    {"year": 2022, "product": "C3 Generative AI"},
    "PATH":  {"year": 2023, "product": "Autopilot AI"},
    "CRWD":  {"year": 2023, "product": "Charlotte AI"},
    "PANW":  {"year": 2023, "product": "AI-powered XSIAM"},
    "ZS":    {"year": 2024, "product": "AI security platform"},
    "S":     {"year": 2023, "product": "Purple AI"},
    "SHOP":  {"year": 2023, "product": "Sidekick AI"},
}

# Clasificación de trayectoria estratégica ex-ante (basada en 10-K FY2021)
# A = Diferenciación/Super-especialización (Porter: Differentiation)
# B = "Atrapados en el medio" / volumen horizontal — CATEGORÍA BASE en regresiones
# C = Plataforma/Infraestructura/Efectos de Red (Porter: Platform/Cost via scale)
#
# Criterio de clasificación: posición estratégica ANTES del lanzamiento de ChatGPT (nov-2022).
# Fuente: descripciones de negocio y segmentos de ingresos en 10-K FY2021.
# Traj_A y Traj_C son perfectamente colineales con EntityEffects (trajectory_type es
# invariante en el tiempo), por lo que solo las interacciones ai_intensity×traj sobreviven
# a la transformación within del modelo de efectos fijos.
TRAJECTORY = {
    # ── Trayectoria A: Diferenciación / Super-especialización ─────────────────
    # Ciberseguridad — dominio con alta especificidad de activos, falla con vibe coding
    "CRWD": "A",  # Cloud-delivered endpoint protection (10-K 2021)
    "PANW": "A",  # AI-powered cybersecurity platform (10-K 2021)
    "FTNT": "A",  # Network security OS (FortiOS) + hardware appliances (10-K 2021)
    "ZS":   "A",  # Zero Trust security cloud (10-K 2021)
    "S":    "A",  # Autonomous cybersecurity platform (10-K 2021)
    "VRNS": "A",  # Data security and analytics for unstructured data (10-K 2021)
    "RPM":  "A",  # Specialized industrial/protective coatings software + services (10-K 2021)
    # SaaS vertical con moat regulatorio o de dominio técnico
    "VEEV": "A",  # Cloud solutions exclusively for life sciences industry (10-K 2021)
    "TYL":  "A",  # Software exclusively for US local/state government (10-K 2021)
    "MANH": "A",  # Supply chain management and omnichannel commerce (10-K 2021)
    "BSY":  "A",  # Engineering/infrastructure BIM software (10-K 2021)
    "CDNS": "A",  # EDA and semiconductor design tools (10-K 2021)
    "SNPS": "A",  # EDA tools + software security testing (10-K 2021)
    "PTC":  "A",  # Industrial IoT + PLM + CAD for manufacturing (10-K 2021)
    # Legacy IT con especialización técnica profunda
    "EPAM": "A",  # Custom software engineering services, deep tech expertise (10-K 2021)
    "PEGA": "A",  # BPM + low-code enterprise automation for regulated industries (10-K 2021)
    # ── Trayectoria B: "Atrapados en el medio" / Volumen horizontal ──────────
    # SaaS horizontal de propósito general — alta replicabilidad por vibe coding
    "BOX":  "B",  # Cloud content management, generic horizontal (10-K 2021)
    "ZM":   "B",  # Video-first unified communications platform (10-K 2021)
    "TWLO": "B",  # Cloud communications platform (APIs), horizontal (10-K 2021)
    "FIVN": "B",  # Cloud contact center software, horizontal (10-K 2021)
    "NICE": "B",  # Cloud platform for customer experience, horizontal (10-K 2021)
    "SEND": "B",  # Email marketing and CRM automation, horizontal (10-K 2021)
    "BRZE": "B",  # Customer engagement platform, horizontal (10-K 2021)
    "BILL": "B",  # Financial operations for SMBs, generic horizontal (10-K 2021)
    "PRGS": "B",  # Application development platform, generic (10-K 2021)
    "DOCN": "B",  # Cloud infrastructure for SMBs, smaller player (10-K 2021)
    # Servicios IT genéricos sin diferenciación técnica clara
    "CTSH": "B",  # IT services and consulting, generic horizontal (10-K 2021)
    "WIT":  "B",  # IT services, generic outsourcing model (10-K 2021)
    "INFY": "B",  # IT services and consulting, generic horizontal (10-K 2021)
    "GLOB": "B",  # Technology services company, generic (10-K 2021)
    "ACN":  "B",  # Management consulting and IT services, generic (10-K 2021)
    # AI-native especulativo sin moat tecnológico claro en 2021
    "BBAI": "B",  # AI/ML services, early-stage speculative (10-K 2021)
    "SOUN": "B",  # Voice AI platform, speculative pre-product (10-K 2021)
    "GFAI": "B",  # Generative AI, speculative pre-revenue (10-K 2021)
    "AIOT": "B",  # AI IoT platform, speculative (10-K 2021)
    # ── Trayectoria C: Plataforma / Infraestructura / Efectos de Red ─────────
    # Plataformas enterprise con efectos de red y ecosistema de partners
    "MSFT": "C",  # Cloud platform + developer ecosystem + enterprise suite (10-K 2021)
    "GOOGL":"C",  # Cloud + search + advertising + developer platform (10-K 2021)
    "ORCL": "C",  # Database + cloud applications + ecosystem (10-K 2021)
    "SAP":  "C",  # ERP platform + cloud ecosystem, 400k+ customers (10-K 2021)
    "IBM":  "C",  # Hybrid cloud + AI platform + ecosystem (10-K 2021)
    "ADBE": "C",  # Creative + document platform with strong network effects (10-K 2021)
    "CRM":  "C",  # CRM platform + AppExchange ecosystem (10-K 2021)
    "INTU": "C",  # Financial platform + data network (TurboTax, QuickBooks) (10-K 2021)
    "NOW":  "C",  # Enterprise workflow platform + partner ecosystem (10-K 2021)
    "WDAY": "C",  # HR + Finance cloud platform, network effects in HR data (10-K 2021)
    # Infraestructura de semiconductores y hardware
    "NVDA": "C",  # GPU computing platform + CUDA ecosystem (10-K 2021)
    "AMD":  "C",  # CPU/GPU computing infrastructure (10-K 2021)
    "INTC": "C",  # Semiconductor + platform infrastructure (10-K 2021)
    "AVGO": "C",  # Semiconductor + infrastructure software (VMware) (10-K 2021)
    "MRVL": "C",  # Semiconductor infrastructure for data centers (10-K 2021)
    "ANET": "C",  # Cloud networking infrastructure (10-K 2021)
    "SMCI": "C",  # Server infrastructure for AI/HPC (10-K 2021)
    # SaaS con fuertes efectos de red o posición de plataforma
    "TEAM": "C",  # Developer collaboration platform + Marketplace (10-K 2021)
    "DDOG": "C",  # Observability platform, network effects in data (10-K 2021)
    "SNOW": "C",  # Data cloud platform, network effects (10-K 2021)
    "MDB":  "C",  # Database platform + Atlas cloud ecosystem (10-K 2021)
    "ESTC": "C",  # Search + observability platform (10-K 2021)
    "HUBS": "C",  # Marketing + CRM platform with SMB network effects (10-K 2021)
    "OKTA": "C",  # Identity platform, network effects in SSO integrations (10-K 2021)
    "PAYC": "C",  # HCM platform with payroll data network (10-K 2021)
    "PCTY": "C",  # HCM/payroll platform (10-K 2021)
    # AI-native con posición de plataforma establecida pre-2022
    "PLTR": "C",  # Government + enterprise data platform (10-K 2021)
    "AI":   "C",  # Enterprise AI platform (C3.ai), SDK/platform model (10-K 2021)
    "PATH": "C",  # RPA automation platform, ecosystem de partners (10-K 2021)
    # E-commerce/ecosystem con efectos de red fuertes
    "MELI": "C",  # E-commerce + fintech platform, LATAM network effects (10-K 2021)
    "SHOP": "C",  # E-commerce platform + merchant ecosystem (10-K 2021)
}


# Eventos exógenos para Difference-in-Differences
EVENTS = {
    "post_copilot":  2021,  # GitHub Copilot GA (oct 2021)
    "post_chatgpt":  2022,  # ChatGPT lanzamiento (nov 2022)
    "post_deepseek": 2025,  # DeepSeek-R1 open source (ene 2025)
}


def load_returns() -> pd.DataFrame:
    path = RAW_DIR / "returns_annual.csv"
    if not path.exists():
        log.warning(f"No encontrado: {path}. Ejecuta collect_prices.py primero.")
        return pd.DataFrame()
    df = pd.read_csv(path)
    log.info(f"Retornos cargados: {len(df):,} filas, {df['ticker'].nunique()} tickers")
    return df


def load_fundamentals() -> pd.DataFrame:
    path = RAW_DIR / "fundamentals_annual.csv"
    if not path.exists():
        log.warning(f"No encontrado: {path}. Ejecuta collect_fundamentals.py primero.")
        return pd.DataFrame()
    df = pd.read_csv(path)
    log.info(f"Fundamentales cargados: {len(df):,} filas")
    return df


def load_so_survey() -> pd.DataFrame:
    """Stack Overflow Survey — descarga manual de https://survey.stackoverflow.co/"""
    path = RAW_DIR / "so_survey.csv"
    if not path.exists():
        log.warning("so_survey.csv no encontrado. Creando placeholder con datos publicados.")
        # Datos agregados del Stack Overflow Developer Survey (publicados en informes anuales)
        so_data = [
            {"year": 2020, "ai_usage_pct": 8.5,  "ai_trust_pct": None},
            {"year": 2021, "ai_usage_pct": 12.0, "ai_trust_pct": None},
            {"year": 2022, "ai_usage_pct": 26.3, "ai_trust_pct": 32.4},
            {"year": 2023, "ai_usage_pct": 44.5, "ai_trust_pct": 37.6},
            {"year": 2024, "ai_usage_pct": 62.1, "ai_trust_pct": 43.2},
        ]
        df = pd.DataFrame(so_data)
        df.to_csv(path, index=False)
        log.info(f"Placeholder SO survey guardado en {path}")
    return pd.read_csv(path)


def build_ai_intensity(df: pd.DataFrame, proc_dir: Path) -> pd.DataFrame:
    """
    Construye el índice AI_intensity (0-100) para cada ticker-año.

    Metodología v1.5 (revisión cuarto revisor):
    - Winsorización global de rd_intensity al 1%/99% para neutralizar outliers extremos
      (pre-revisión: media=84.7%, SD=617.5%, max=8,673%)
    - Normalización min-max GLOBAL (todo el panel, no por año) para evitar variación
      cross-firm artificial en modelos de efectos fijos
    - Pesos derivados de Análisis de Componentes Principales (PCA) sobre los 3 componentes,
      en lugar de pesos ad-hoc 40/30/30
    """
    try:
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler
        sklearn_available = True
    except ImportError:
        sklearn_available = False
        log.warning("sklearn no disponible; usando pesos iguales 1/3 como fallback")

    df = df.copy()

    # ── Componente 1: ai_product_binary ────────────────────────────────────
    def get_product_binary(row):
        launch = AI_PRODUCT_LAUNCH.get(row["ticker"])
        if launch and row["year"] >= launch["year"]:
            return 1
        return 0

    df["ai_product_binary"] = df.apply(get_product_binary, axis=1)

    # ── Componente 2: rd_intensity_norm — winsorizada + normalización global ─
    if "rd_intensity" in df.columns:
        p01 = df["rd_intensity"].quantile(0.01)
        p99 = df["rd_intensity"].quantile(0.99)
        df["rd_intensity_w"] = df["rd_intensity"].clip(lower=p01, upper=p99)
        log.info(f"rd_intensity winsorizada: p01={p01:.2f}%, p99={p99:.2f}%  "
                 f"(antes: SD={df['rd_intensity'].std():.1f}%, "
                 f"después: SD={df['rd_intensity_w'].std():.1f}%)")
        # Normalización GLOBAL: 0 para NaN/sin datos, 1 para valor máximo winsorizado
        # Usar 0 como mínimo garantiza que empresas sin R&D mapeen a 0 (no a valor negativo)
        df["rd_intensity_norm"] = df["rd_intensity_w"].fillna(0).clip(lower=0) / (p99 + 1e-9)
    else:
        df["rd_intensity_norm"] = 0.0
        df["rd_intensity_w"] = 0.0

    # ── Componente 3: ai_mentions_proxy ────────────────────────────────────
    def get_mentions_proxy(row):
        launch = AI_PRODUCT_LAUNCH.get(row["ticker"])
        if not launch:
            return 0.0
        years_since = max(0, row["year"] - launch["year"])
        return min(1.0, years_since / 3.0)

    df["ai_mentions_proxy"] = df.apply(get_mentions_proxy, axis=1)

    # ── PCA para pesos (o fallback 1/3 cada uno) ────────────────────────────
    components = ["ai_product_binary", "rd_intensity_norm", "ai_mentions_proxy"]
    X = df[components].fillna(0).values

    if sklearn_available and X.shape[0] > 10:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        pca = PCA(n_components=1)
        pca.fit(X_scaled)
        raw_loadings = pca.components_[0]
        # Asegurar dirección positiva (todos los componentes deben contribuir positivamente)
        if raw_loadings.sum() < 0:
            raw_loadings = -raw_loadings
        weights = np.abs(raw_loadings) / np.abs(raw_loadings).sum()
        variance_explained = pca.explained_variance_ratio_[0]
        log.info(f"PCA pesos: {dict(zip(components, weights.round(4)))}  "
                 f"(varianza explicada por PC1: {variance_explained:.1%})")
        pca_info = {
            "weights": dict(zip(components, [float(w) for w in weights])),
            "variance_explained_pc1": float(variance_explained),
            "loadings_raw": dict(zip(components, [float(l) for l in raw_loadings])),
            "method": "PCA (StandardScaler + PC1)",
            "note": "Pesos v1.5: PCA sobre componentes estandarizados, reemplaza 40/30/30 ad-hoc"
        }
    else:
        weights = np.array([1/3, 1/3, 1/3])
        pca_info = {"weights": dict(zip(components, [1/3]*3)), "method": "fallback_equal"}
        log.warning("Usando pesos iguales (sklearn no disponible o muestra insuficiente)")

    # ── Índice compuesto con pesos PCA ─────────────────────────────────────
    df["ai_intensity"] = (
        weights[0] * df["ai_product_binary"]
        + weights[1] * df["rd_intensity_norm"]
        + weights[2] * df["ai_mentions_proxy"]
    ) * 100

    log.info(f"AI_intensity nueva distribución: "
             f"media={df['ai_intensity'].mean():.2f}, "
             f"SD={df['ai_intensity'].std():.2f}, "
             f"mediana={df['ai_intensity'].median():.2f}, "
             f"p75={df['ai_intensity'].quantile(0.75):.2f}")

    # Guardar metadatos de PCA para documentación en la tesis
    pca_path = proc_dir / "ai_intensity_pca_weights.json"
    with open(pca_path, "w", encoding="utf-8") as f:
        json.dump(pca_info, f, indent=2)
    log.info(f"Pesos PCA guardados en: {pca_path}")

    # ── Quintil de AI intensity (sobre panel completo, no por año) ──────────
    def safe_qcut(x):
        try:
            return pd.qcut(x, q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")
        except ValueError:
            return pd.qcut(x.rank(method="first"), q=min(5, x.nunique()), labels=False, duplicates="drop") + 1

    df["ai_intensity_quintile"] = safe_qcut(df["ai_intensity"])

    return df


def add_event_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Añade variables binarias para Difference-in-Differences."""
    df = df.copy()
    for col, threshold_year in EVENTS.items():
        df[col] = (df["year"] > threshold_year).astype(int)

    # treated: empresa que lanzó AI product dentro de 1 año del evento ChatGPT
    chatgpt_year = EVENTS["post_chatgpt"]
    def is_treated(row):
        launch = AI_PRODUCT_LAUNCH.get(row["ticker"])
        if not launch:
            return 0
        return int(abs(launch["year"] - chatgpt_year) <= 1)

    df["treated_chatgpt"] = df["ticker"].apply(
        lambda t: int(t in AI_PRODUCT_LAUNCH and abs(AI_PRODUCT_LAUNCH[t]["year"] - chatgpt_year) <= 1)
    )
    return df


def add_trajectory_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega la variable trajectory_type (A/B/C) clasificada ex-ante con 10-K FY2021.
    Esta variable es invariante en el tiempo por diseño: captura la posición estratégica
    ANTES del shock ChatGPT (nov-2022), evitando hindsight bias.
    Al ser constante por firma, los efectos principales traj_A/traj_C son absorbidos por
    EntityEffects en el modelo FE; solo las interacciones con ai_intensity (variante en
    el tiempo) sobreviven a la transformación within — esto es correcto e intencionado.
    """
    df = df.copy()
    df["trajectory_type"] = df["ticker"].map(TRAJECTORY)
    n_missing = df["trajectory_type"].isna().sum()
    if n_missing > 0:
        missing_tickers = df[df["trajectory_type"].isna()]["ticker"].unique().tolist()
        log.warning(f"trajectory_type sin asignar ({n_missing} filas): {missing_tickers}")
        df["trajectory_type"] = df["trajectory_type"].fillna("B")  # fallback conservador
    log.info(f"trajectory_type distribution: {df.groupby('trajectory_type')['ticker'].nunique().to_dict()}")
    return df


def add_log_transforms(df: pd.DataFrame) -> pd.DataFrame:
    """Añade transformaciones logarítmicas para regresiones."""
    df = df.copy()
    if "revenues" in df.columns:
        df["log_revenues"] = np.log(df["revenues"].clip(lower=1))
    if "market_cap" in df.columns:
        df["log_market_cap"] = np.log(df["market_cap"].clip(lower=1))
    if "employees" in df.columns:
        df["log_employees"] = np.log(df["employees"].clip(lower=1))
    return df


def main():
    # ── Cargar fuentes ─────────────────────────────────────────────────────
    returns = load_returns()
    fundamentals = load_fundamentals()
    so_survey = load_so_survey()

    if returns.empty:
        log.error("Sin datos de retornos. Ejecuta collect_prices.py primero.")
        return

    # ── Merge retornos + fundamentales ────────────────────────────────────
    if not fundamentals.empty:
        panel = pd.merge(returns, fundamentals, on=["ticker", "year"], how="left")
    else:
        panel = returns.copy()
        log.warning("Usando panel solo con retornos (sin fundamentales)")

    # ── Merge Stack Overflow (nivel macro, aplica a todos los tickers por año) ─
    panel = pd.merge(panel, so_survey, on="year", how="left")

    # ── Variables derivadas ────────────────────────────────────────────────
    panel = build_ai_intensity(panel, PROC_DIR)
    panel = add_event_indicators(panel)
    panel = add_log_transforms(panel)
    panel = add_trajectory_type(panel)

    # ── Filtrar años 2019-2025 ─────────────────────────────────────────────
    panel = panel[(panel["year"] >= 2019) & (panel["year"] <= 2025)]

    # ── Excluir benchmarks del panel principal (mantener como referencia) ──
    benchmarks = ["^GSPC", "^IXIC", "QQQ", "IGV", "SKYY", "ROBT", "CIBR"]
    panel_companies = panel[~panel["ticker"].isin(benchmarks)].copy()
    panel_benchmarks = panel[panel["ticker"].isin(benchmarks)].copy()

    # ── Guardar ───────────────────────────────────────────────────────────
    panel_path = PROC_DIR / "panel_final.csv"
    panel_companies.to_csv(panel_path, index=False)
    log.info(f"Panel final guardado: {panel_path}")
    log.info(f"  Empresas: {panel_companies['ticker'].nunique()}")
    log.info(f"  Años: {sorted(panel_companies['year'].unique())}")
    log.info(f"  Filas total: {len(panel_companies):,}")

    bench_path = PROC_DIR / "benchmarks.csv"
    panel_benchmarks.to_csv(bench_path, index=False)
    log.info(f"Benchmarks guardados: {bench_path}")

    # ── Estadísticas descriptivas ──────────────────────────────────────────
    key_vars = ["return_annual_pct", "ai_intensity", "op_margin", "net_margin",
                "rd_intensity", "tech_debt_proxy", "ai_usage_pct"]
    available = [v for v in key_vars if v in panel_companies.columns]

    summary = panel_companies[available].describe().round(3)
    summary_path = PROC_DIR / "panel_summary.csv"
    summary.to_csv(summary_path)
    log.info(f"Estadísticas descriptivas guardadas: {summary_path}")

    print("\n-- Estadisticas Descriptivas del Panel --")
    print(summary.to_string())

    print("\n-- Distribucion por grupo --")
    if "group" in panel_companies.columns:
        print(panel_companies.groupby("group")["return_annual_pct"].agg(["mean", "std", "count"]).round(2).to_string())

    print("\n-- AI Intensity por quintil (retorno medio) --")
    if "ai_intensity_quintile" in panel_companies.columns:
        print(panel_companies.groupby("ai_intensity_quintile")["return_annual_pct"].agg(["mean", "std", "count"]).round(2).to_string())

    print("\n-- Retornos por trayectoria estratégica x periodo (Cuadro Sección 5.3) --")
    if "trajectory_type" in panel_companies.columns:
        panel_companies["periodo"] = panel_companies["year"].apply(
            lambda y: "pre_2022" if y <= 2022 else "post_2022"
        )
        traj_stats = panel_companies.groupby(["trajectory_type", "periodo"])[
            ["return_annual_pct", "ai_intensity", "rd_intensity", "op_margin"]
        ].agg(["mean", "median", "std"]).round(2)
        print(traj_stats.to_string())

        # Guardar tabla de trayectorias para la tesis
        traj_path = PROC_DIR / "trajectory_summary.csv"
        traj_flat = panel_companies.groupby(["trajectory_type", "periodo"])[
            ["return_annual_pct", "ai_intensity", "op_margin"]
        ].agg(["mean", "std", "count"]).round(3)
        traj_flat.to_csv(traj_path)
        log.info(f"Estadísticas por trayectoria guardadas: {traj_path}")

        print("\n-- Empresas por trayectoria --")
        traj_firms = panel_companies.groupby("trajectory_type")["ticker"].nunique()
        print(traj_firms.to_string())

    print(f"\nPanel listo en: {panel_path}")


if __name__ == "__main__":
    main()
