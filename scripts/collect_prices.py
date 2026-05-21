"""
collect_prices.py
Extrae precios históricos OHLCV y retornos para el universo de empresas de software.
Fuente: Yahoo Finance v8 (gratis, sin API key) via yfinance.

Uso:
    pip install yfinance pandas
    python scripts/collect_prices.py

Salida:
    data/raw/prices_daily.csv   — OHLCV diario por ticker
    data/raw/returns_annual.csv — Retornos anuales por ticker y año
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, date
from pathlib import Path
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

# ── Universo de empresas ──────────────────────────────────────────────────────
# ~150 empresas software + comparadores. Clasificadas por tipo.
# Fuente de la lista: GICS 4510/4520/4530 + S&P 500 + Russell 1000

UNIVERSE = {
    # --- Platform incumbents (adoptaron AI en producto existente) ---
    "platform": [
        "MSFT",   # Microsoft (Copilot, Azure AI)
        "GOOGL",  # Alphabet (Gemini, Cloud AI)
        "ORCL",   # Oracle (AI Data Platform)
        "SAP",    # SAP SE (Joule AI)
        "IBM",    # IBM (watsonx)
        "ADBE",   # Adobe (Firefly)
        "CRM",    # Salesforce (Einstein AI)
        "INTU",   # Intuit (AI-powered finance)
        "NOW",    # ServiceNow (AI workflows)
        "WDAY",   # Workday (AI in HCM)
    ],
    # --- Pure-play SaaS (software como servicio, adoptadores AI) ---
    "saas": [
        "TEAM",   # Atlassian
        "ZM",     # Zoom (AI companion)
        "OKTA",   # Okta
        "DDOG",   # Datadog
        "SNOW",   # Snowflake (Cortex AI)
        "MDB",    # MongoDB
        "ESTC",   # Elastic
        "HUBS",   # HubSpot (AI features)
        "PCTY",   # Paylocity
        "PAYC",   # Paycom
        "VEEV",   # Veeva (vertical SaaS, pharma)
        "TYL",    # Tyler Technologies (vertical SaaS, gov)
        "BOX",    # Box (AI document intelligence)
        "DOCN",   # DigitalOcean
        "FIVN",   # Five9 (contact center AI)
        "NICE",   # NICE (CX AI)
        "MELI",   # MercadoLibre (tech latam)
        "SHOP",   # Shopify (AI commerce)
        "TWLO",   # Twilio
        "SEND",   # Klaviyo
        "BRZE",   # Braze
        "BILL",   # Bill.com
        "PRGS",   # Progress Software
    ],
    # --- AI-native (core de negocio es AI) ---
    "ai_native": [
        "PLTR",   # Palantir (AIP)
        "AI",     # C3.ai
        "PATH",   # UiPath (RPA + AI)
        "BBAI",   # BigBear.ai
        "SOUN",   # SoundHound AI (voice AI)
        "GFAI",   # Guardforce AI
        "AIOT",   # Alphaiot (industrial AI)
    ],
    # --- Semiconductores/infra (cadena de valor AI, comparadores) ---
    "infra": [
        "NVDA",   # NVIDIA (GPU AI)
        "AMD",    # AMD
        "INTC",   # Intel
        "AVGO",   # Broadcom (AI networking)
        "MRVL",   # Marvell (AI silicon)
        "ANET",   # Arista Networks
        "SMCI",   # Super Micro Computer
    ],
    # --- Software de seguridad (mercado de remediación AI) ---
    "security": [
        "CRWD",   # CrowdStrike (AI security)
        "PANW",   # Palo Alto Networks
        "FTNT",   # Fortinet
        "ZS",     # Zscaler
        "S",      # SentinelOne
        "VRNS",   # Varonis
        "RPM",    # Rapid7
    ],
    # --- Software empresarial legacy (control, baja adopción AI) ---
    "legacy": [
        "CTSH",   # Cognizant
        "ACN",    # Accenture
        "WIT",    # Wipro
        "INFY",   # Infosys
        "EPAM",   # EPAM Systems
        "GLOB",   # Globant
        "PEGA",   # Pegasystems
        "VRNT",   # Verint Systems
        "MANH",   # Manhattan Associates
        "BSY",    # Bentley Systems
        "PTC",    # PTC Inc
        "CDNS",   # Cadence Design Systems
        "SNPS",   # Synopsys
    ],
    # --- Índices de referencia ---
    "benchmarks": [
        "^GSPC",  # S&P 500
        "^IXIC",  # NASDAQ Composite
        "QQQ",    # NASDAQ 100 ETF
        "IGV",    # iShares Expanded Tech-Software ETF
        "SKYY",   # First Trust Cloud Computing ETF
        "ROBT",   # First Trust Nasdaq Artificial Intelligence ETF
        "CIBR",   # First Trust NASDAQ Cybersecurity ETF
    ],
}

START_DATE = "2019-01-01"
END_DATE = date.today().isoformat()
RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def all_tickers() -> list[str]:
    tickers = []
    for group in UNIVERSE.values():
        tickers.extend(group)
    return list(dict.fromkeys(tickers))  # dedup, preserve order


def fetch_prices(tickers: list[str]) -> pd.DataFrame:
    """Descarga precios diarios OHLCV ajustados para todos los tickers."""
    log.info(f"Descargando precios para {len(tickers)} tickers ({START_DATE} → {END_DATE})")
    raw = yf.download(
        tickers,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True,  # adjusted close, splits y dividendos incluidos
        progress=True,
        threads=True,
    )
    # yf 1.x returns MultiIndex columns with names ('Price', 'Ticker')
    if isinstance(raw.columns, pd.MultiIndex):
        raw = raw.stack(level=1).reset_index()
        raw.columns.name = None
        # yfinance 1.x uses 'Ticker' as the stacked level name
        ticker_col = next((c for c in raw.columns if c.lower() in ("ticker", "level_1", "symbol")), None)
        date_col = next((c for c in raw.columns if c.lower() in ("date", "datetime")), None)
        rename_map = {}
        if ticker_col and ticker_col != "ticker":
            rename_map[ticker_col] = "ticker"
        if date_col and date_col != "date":
            rename_map[date_col] = "date"
        if rename_map:
            raw = raw.rename(columns=rename_map)
    else:
        raw = raw.reset_index()
        date_col = next((c for c in raw.columns if c.lower() in ("date", "datetime")), "Date")
        raw = raw.rename(columns={date_col: "date"})
        raw["ticker"] = tickers[0]

    raw["date"] = pd.to_datetime(raw["date"]).dt.date.astype(str)
    cols = ["ticker", "date", "Open", "High", "Low", "Close", "Volume"]
    available = [c for c in cols if c in raw.columns]
    raw = raw[available].rename(columns=str.lower)
    raw = raw.dropna(subset=["close"])
    return raw.sort_values(["ticker", "date"]).reset_index(drop=True)


def compute_annual_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calcula retorno anual para cada ticker y año."""
    prices["date"] = pd.to_datetime(prices["date"])
    prices["year"] = prices["date"].dt.year

    records = []
    for ticker, grp in prices.groupby("ticker"):
        grp = grp.sort_values("date")
        for year in grp["year"].unique():
            yr = grp[grp["year"] == year]
            if len(yr) < 5:
                continue
            start_price = yr.iloc[0]["close"]
            end_price = yr.iloc[-1]["close"]
            if start_price and start_price > 0:
                ret = (end_price - start_price) / start_price * 100
                records.append({"ticker": ticker, "year": int(year), "return_annual_pct": round(ret, 4)})

    return pd.DataFrame(records)


def add_ticker_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Añade columna 'group' según el universo definido."""
    ticker_to_group = {}
    for group, tickers in UNIVERSE.items():
        for t in tickers:
            ticker_to_group[t] = group
    df["group"] = df["ticker"].map(ticker_to_group).fillna("other")
    return df


def main():
    tickers = all_tickers()
    log.info(f"Universo total: {len(tickers)} tickers")

    prices = fetch_prices(tickers)
    prices = add_ticker_metadata(prices)

    prices_path = RAW_DIR / "prices_daily.csv"
    prices.to_csv(prices_path, index=False)
    log.info(f"Precios guardados: {prices_path} ({len(prices):,} filas)")

    returns = compute_annual_returns(prices)
    returns = add_ticker_metadata(returns)
    returns_path = RAW_DIR / "returns_annual.csv"
    returns.to_csv(returns_path, index=False)
    log.info(f"Retornos anuales guardados: {returns_path} ({len(returns):,} filas)")

    # Resumen rápido
    print("\n-- Retornos medios por grupo (2019-2025) --")
    summary = returns.groupby("group")["return_annual_pct"].agg(["mean", "std", "count"])
    print(summary.round(2).to_string())


if __name__ == "__main__":
    main()
