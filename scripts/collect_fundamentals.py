"""
collect_fundamentals.py
Extrae fundamentales financieros de SEC EDGAR (API gratuita) y Yahoo Finance.

Datos obtenidos:
  - Ingresos, Utilidad Neta, Margen Bruto, Margen Operativo (SEC EDGAR XBRL)
  - Gasto en I+D (proxy de innovacion)
  - Gastos en costo de ventas / soporte (proxy de deuda tecnica)
  - Numero de empleados
  - P/E, Market Cap, Beta (Yahoo Finance)

Uso:
    pip install yfinance pandas requests
    python scripts/collect_fundamentals.py

Salida:
    data/raw/fundamentals_annual.csv  -- datos anuales por empresa
    data/raw/yahoo_current.csv        -- datos actuales de Yahoo Finance
"""

import requests
import yfinance as yf
import pandas as pd
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

EDGAR_BASE = "https://data.sec.gov/api/xbrl/companyfacts"
EDGAR_HEADERS = {
    "User-Agent": "Research Project alejandro.jimenez@evolveam.com.mx",
    "Accept-Encoding": "gzip, deflate",
}

# CIK numbers de SEC para las empresas del universo
# Fuente: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company=&CIK=
TICKER_TO_CIK = {
    # Platform incumbents
    "MSFT":  "0000789019",
    "GOOGL": "0001652044",
    "ORCL":  "0001341439",
    "SAP":   "0001000184",
    "IBM":   "0000051143",
    "ADBE":  "0000796343",
    "CRM":   "0001108524",
    "INTU":  "0000896878",
    "NOW":   "0001373715",
    "WDAY":  "0001327811",
    # Pure-play SaaS
    "TEAM":  "0001650372",
    "ZM":    "0001585521",
    "OKTA":  "0001660134",
    "DDOG":  "0001677250",
    "SNOW":  "0001640147",
    "MDB":   "0001441816",
    "ESTC":  "0001707753",
    "HUBS":  "0001404655",
    "PCTY":  "0001591698",
    "PAYC":  "0001590955",
    "VEEV":  "0001393052",
    "TYL":   "0000860731",
    "BOX":   "0001372612",
    "DOCN":  "0001800227",
    "FIVN":  "0001288847",
    "MELI":  "0001099590",
    "SHOP":  "0001594805",
    "TWLO":  "0001447362",
    "BRZE":  "0001676238",
    "BILL":  "0001425287",
    "PRGS":  "0000876343",
    # AI-native
    "PLTR":  "0001321655",
    "AI":    "0001577526",
    "PATH":  "0001739942",
    "BBAI":  "0001836935",
    "SOUN":  "0001840292",
    # Semiconductores / infra
    "NVDA":  "0001045810",
    "AMD":   "0000002488",
    "INTC":  "0000050863",
    "AVGO":  "0001730168",
    "MRVL":  "0001058057",
    "ANET":  "0001596532",
    "SMCI":  "0001375365",
    # Seguridad
    "CRWD":  "0001535527",
    "PANW":  "0001327567",
    "FTNT":  "0001262039",
    "ZS":    "0001713683",
    "S":     "0001816017",
    "VRNS":  "0001614806",
    # Legacy / IT services
    "CTSH":  "0001058290",
    "ACN":   "0001467373",
    "INFY":  "0001067491",
    "EPAM":  "0001352010",
    "GLOB":  "0001557860",
    "PEGA":  "0001018979",
    "VRNT":  "0001166388",
    "MANH":  "0001056696",
    "BSY":   "0001517228",
    "PTC":   "0000857005",
    "CDNS":  "0000813672",
    "SNPS":  "0000883241",
}

# Conceptos XBRL con alternativas por orden de preferencia.
# Se usara el primero que tenga datos anuales disponibles.
XBRL_CONCEPTS: dict[str, list[tuple[str, str]]] = {
    "revenues": [
        ("us-gaap", "Revenues"),
        ("us-gaap", "RevenueFromContractWithCustomerExcludingAssessedTax"),
        ("us-gaap", "RevenueFromContractWithCustomerIncludingAssessedTax"),
        ("us-gaap", "SalesRevenueNet"),
        ("us-gaap", "RevenuesNetOfInterestExpense"),
        ("us-gaap", "ContractsRevenue"),
        ("ifrs-full", "Revenue"),
        ("ifrs-full", "RevenueFromContractsWithCustomers"),
    ],
    "net_income": [
        ("us-gaap", "NetIncomeLoss"),
        ("us-gaap", "ProfitLoss"),
        ("us-gaap", "NetIncomeLossAvailableToCommonStockholdersBasic"),
        ("ifrs-full", "ProfitLoss"),
    ],
    "gross_profit": [
        ("us-gaap", "GrossProfit"),
        ("ifrs-full", "GrossProfit"),
    ],
    "operating_income": [
        ("us-gaap", "OperatingIncomeLoss"),
        ("us-gaap", "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"),
        ("ifrs-full", "ProfitLossFromOperatingActivities"),
        ("ifrs-full", "OperatingProfit"),
    ],
    "rd_expense": [
        ("us-gaap", "ResearchAndDevelopmentExpense"),
        ("us-gaap", "ResearchAndDevelopmentExpenseExcludingAcquiredInProcessCost"),
        ("ifrs-full", "ResearchAndDevelopmentExpense"),
    ],
    "cogs": [
        ("us-gaap", "CostOfRevenue"),
        ("us-gaap", "CostOfGoodsAndServicesSold"),
        ("us-gaap", "CostOfGoodsSold"),
        ("us-gaap", "CostOfServices"),
        ("us-gaap", "CostOfRevenueAmortization"),
        ("ifrs-full", "CostOfSales"),
    ],
    "employees": [
        ("dei", "EntityNumberOfEmployees"),
    ],
}


def fetch_company_facts(cik: str) -> dict:
    """Descarga el JSON completo de hechos XBRL de una empresa (una sola peticion HTTP)."""
    url = f"{EDGAR_BASE}/CIK{cik}.json"
    try:
        r = requests.get(url, headers=EDGAR_HEADERS, timeout=45)
        if r.status_code != 200:
            log.warning(f"EDGAR HTTP {r.status_code} para CIK={cik}")
            return {}
        return r.json()
    except Exception as e:
        log.warning(f"EDGAR fetch error CIK={cik}: {e}")
        return {}


def extract_annual_series(facts_json: dict, taxonomy: str, concept: str) -> list[dict]:
    """Extrae serie anual (10-K o 20-F, FY) de un concepto XBRL del JSON ya descargado.
    Elige la unidad monetaria con más registros anuales FY (maneja IFRS/EUR para SAP etc.)."""
    facts = facts_json.get("facts", {}).get(taxonomy, {}).get(concept, {})
    units = facts.get("units", {})
    best: list[dict] = []
    for unit_vals in units.values():
        annual = [v for v in unit_vals if v.get("form") in ("10-K", "20-F") and v.get("fp") == "FY"]
        if len(annual) > len(best):
            best = annual
    return best


def edgar_to_dataframe(ticker: str, cik: str) -> pd.DataFrame:
    """Extrae todos los conceptos XBRL para una empresa usando el JSON cacheado."""
    facts_json = fetch_company_facts(cik)
    if not facts_json:
        return pd.DataFrame()

    time.sleep(0.12)  # respeta rate limit SEC (max ~10 req/s)

    records: dict[int, dict] = {}

    for col_name, alternatives in XBRL_CONCEPTS.items():
        items = []
        for taxonomy, concept in alternatives:
            items = extract_annual_series(facts_json, taxonomy, concept)
            if items:
                log.debug(f"  {ticker} {col_name}: usando {taxonomy}/{concept} ({len(items)} pts)")
                break  # primer alternativo con datos

        for item in items:
            year = int(item.get("end", "0000")[:4])
            if year < 2018:
                continue
            val = item.get("val")
            if val is None:
                continue
            if year not in records:
                records[year] = {"ticker": ticker, "year": year}
            # Solo sobreescribir si no habia valor (evita duplicados de restatements)
            if col_name not in records[year]:
                records[year][col_name] = val

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(list(records.values())).sort_values("year").reset_index(drop=True)

    # Calcular margenes (requieren revenues)
    if "revenues" in df.columns:
        for margin_col, num_col in [
            ("gross_margin", "gross_profit"),
            ("op_margin", "operating_income"),
            ("net_margin", "net_income"),
        ]:
            if num_col in df.columns:
                df[margin_col] = df[num_col] / df["revenues"] * 100

        if "cogs" in df.columns:
            df["tech_debt_proxy"] = df["cogs"] / df["revenues"] * 100

        if "rd_expense" in df.columns:
            df["rd_intensity"] = df["rd_expense"] / df["revenues"] * 100

    return df


def fetch_yahoo_fundamentals(tickers: list[str]) -> pd.DataFrame:
    """Obtiene P/E, market cap, beta, margenes actuales de Yahoo Finance."""
    records = []
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            records.append({
                "ticker": ticker,
                "market_cap": info.get("marketCap"),
                "pe_trailing": info.get("trailingPE"),
                "pe_forward": info.get("forwardPE"),
                "beta": info.get("beta"),
                "div_yield": info.get("dividendYield"),
                "profit_margin_ttm": info.get("profitMargins"),
                "gross_margin_ttm": info.get("grossMargins"),
                "op_margin_ttm": info.get("operatingMargins"),
                "revenue_ttm": info.get("totalRevenue"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "employees_current": info.get("fullTimeEmployees"),
                "country": info.get("country"),
            })
            time.sleep(0.4)
        except Exception as e:
            log.warning(f"Yahoo error {ticker}: {e}")
    return pd.DataFrame(records)


def main():
    # -- 1. Datos anuales de SEC EDGAR --
    log.info(f"Descargando fundamentales de SEC EDGAR para {len(TICKER_TO_CIK)} empresas...")
    dfs = []
    for ticker, cik in TICKER_TO_CIK.items():
        log.info(f"  {ticker} (CIK {cik})")
        df = edgar_to_dataframe(ticker, cik)
        if not df.empty:
            dfs.append(df)
            log.info(f"    -> {len(df)} filas, cols: {[c for c in df.columns if c not in ('ticker','year')]}")
        else:
            log.warning(f"    -> sin datos")

    if dfs:
        fundamentals = pd.concat(dfs, ignore_index=True)
        path = RAW_DIR / "fundamentals_annual.csv"
        fundamentals.to_csv(path, index=False)
        log.info(f"Fundamentales guardados: {path} ({len(fundamentals):,} filas)")

        # Cobertura por columna
        print("\n-- Cobertura por variable --")
        for col in ["revenues", "cogs", "rd_expense", "operating_income", "net_income",
                    "tech_debt_proxy", "rd_intensity", "op_margin"]:
            if col in fundamentals.columns:
                n = fundamentals.dropna(subset=[col])["ticker"].nunique()
                print(f"  {col}: {n} empresas")
    else:
        log.warning("No se obtuvieron datos de EDGAR")
        return

    # -- 2. Datos actuales de Yahoo Finance --
    log.info("Descargando datos actuales de Yahoo Finance...")
    yahoo_df = fetch_yahoo_fundamentals(list(TICKER_TO_CIK.keys()))
    yahoo_path = RAW_DIR / "yahoo_current.csv"
    yahoo_df.to_csv(yahoo_path, index=False)
    log.info(f"Yahoo actuales guardados: {yahoo_path} ({len(yahoo_df)} empresas)")

    # -- Resumen --
    print("\n-- Margenes operativos medios 2023-2024 --")
    recent = fundamentals[fundamentals["year"] >= 2023]
    if "op_margin" in recent.columns:
        summary = recent.groupby("ticker")["op_margin"].mean().dropna().sort_values(ascending=False).round(1)
        print(summary.to_string())


if __name__ == "__main__":
    main()
