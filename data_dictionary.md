# Diccionario de Datos
**Proyecto:** Futuro de las Empresas de Software ante la IA Generativa  
**Última actualización:** 2026-05-17

---

## Identificadores del Panel

| Variable | Tipo | Descripción | Fuente |
|----------|------|-------------|--------|
| `ticker` | string | Símbolo bursátil de la empresa (e.g., MSFT, ORCL) | Yahoo Finance |
| `company_name` | string | Nombre completo de la empresa | Yahoo Finance / SEC |
| `year` | int | Año fiscal (2019–2025) | — |
| `quarter` | int | Trimestre (1–4); NULL si dato anual | — |
| `gics_sector` | string | Sector GICS de nivel 1 (e.g., "Information Technology") | Yahoo Finance |
| `gics_subsector` | string | Subsector GICS (e.g., "Software", "IT Services") | Yahoo Finance |
| `region` | string | "North America", "Europe", "Asia Pacific", "Other" | Yahoo Finance |
| `country` | string | País de cotización primaria | Yahoo Finance |

---

## Variables Dependientes

| Variable | Tipo | Descripción | Fuente | Notas |
|----------|------|-------------|--------|-------|
| `return_1y` | float | Retorno total ajustado a 1 año (%) | Yahoo Finance history API | Adjusted close, incluye dividendos |
| `return_3y_ann` | float | Retorno anualizado a 3 años (%) | Yahoo Finance history API | CAGR = (endPrice/startPrice)^(1/3) - 1 |
| `return_ytd` | float | Retorno año a la fecha (%) | Yahoo Finance | Al cierre del año fiscal |
| `profit_margin` | float | Margen de utilidad neta (%) | SEC EDGAR 10-K / yahoo-finance2 | Net income / Revenue |
| `gross_margin` | float | Margen bruto (%) | SEC EDGAR 10-K | Gross profit / Revenue |
| `op_margin` | float | Margen operativo (%) | SEC EDGAR 10-K | Operating income / Revenue |
| `market_cap_growth` | float | Crecimiento de market cap YoY (%) | Yahoo Finance | (MC_t - MC_{t-1}) / MC_{t-1} |
| `revenue_growth` | float | Crecimiento de ingresos YoY (%) | SEC EDGAR | (Rev_t - Rev_{t-1}) / Rev_{t-1} |

---

## Variable Independiente Clave: AI_intensity

Índice compuesto (0–100) que mide el grado de involucramiento de la empresa con IA generativa.

**Construcción del índice:**

| Componente | Peso | Descripción | Fuente |
|------------|------|-------------|--------|
| `ai_revenue_pct` | 40% | % de ingresos atribuibles a productos/servicios AI | SEC 10-K (segment data) |
| `ai_mentions_10k` | 20% | # de veces que "artificial intelligence" o "generative AI" aparece en 10-K anual | SEC EDGAR text search |
| `ai_product_binary` | 20% | 1 si la empresa tiene producto AI generativa lanzado, 0 si no | Clasificación manual + press releases |
| `rd_intensity` | 20% | Gasto I+D / Ingresos (proxy de innovación) | SEC 10-K |

**Fórmula:**
```
AI_intensity = 0.40 × norm(ai_revenue_pct) + 0.20 × norm(ai_mentions_10k) + 0.20 × ai_product_binary + 0.20 × norm(rd_intensity)
```
Donde `norm()` normaliza cada componente al rango [0,1] usando min-max scaling.

**Clasificación por quintil:**
- Q5 (80–100): AI-nativas o líderes de adopción (MSFT, NVDA, GOOGL)
- Q4 (60–79): Adoptadores tempranos con productos AI establecidos
- Q3 (40–59): Adoptadores en progreso
- Q2 (20–39): Adoptadores tardíos
- Q1 (0–19): Sin adopción significativa

---

## Variables Independientes de Control

| Variable | Tipo | Descripción | Fuente | Por qué se incluye |
|----------|------|-------------|--------|-------------------|
| `log_market_cap` | float | ln(market cap en USD) | Yahoo Finance | Controla por tamaño de empresa |
| `beta` | float | Beta de mercado (3 años) | Yahoo Finance | Controla por riesgo sistemático |
| `pe_ratio` | float | Price-to-Earnings trailing | Yahoo Finance | Controla por valuación |
| `div_yield` | float | Dividend yield (%) | Yahoo Finance | Controla por madurez/estilo de empresa |
| `leverage` | float | Deuda total / Equity total | SEC 10-K | Controla por estructura de capital |
| `age_years` | int | Años desde fundación | Wikipedia / Crunchbase | Controla por madurez de empresa |
| `employees` | int | Número de empleados | SEC 10-K | Control adicional de tamaño |

---

## Variable de Deuda Técnica (Proxy)

| Variable | Tipo | Descripción | Fuente | Limitación |
|----------|------|-------------|--------|-----------|
| `tech_debt_proxy` | float | Gastos en mantenimiento y soporte / Ingresos totales (%) | SEC 10-K (Cost of Revenue breakdown) | No todas las empresas reportan este desglose |
| `support_cost_ratio` | float | Costo de soporte al cliente / Ingresos (%) | SEC 10-K | Proxy alternativo si tech_debt_proxy no disponible |
| `bug_rate_index` | float | Índice de bugs reportados públicamente (NVD CVEs / 1000 LOC equiv.) | NIST NVD API | Solo para empresas con suficientes CVEs registrados |

**Nota:** La deuda técnica no es directamente observable en datos públicos. Los proxies son aproximaciones imperfectas. Se documenta esta limitación explícitamente en la tesis.

---

## Variables de Adopción Sectorial (Nivel Macro)

| Variable | Tipo | Descripción | Fuente | Frecuencia |
|----------|------|-------------|--------|-----------|
| `so_ai_usage_pct` | float | % de developers que usan AI tools "regularmente" por año | Stack Overflow Developer Survey | Anual (2020–2024) |
| `so_ai_trust_pct` | float | % de developers que "confían en las respuestas de AI" | Stack Overflow Developer Survey | Anual (2022–2024) |
| `gh_ai_code_pct` | float | % de código en repos públicos generado con asistencia AI | GitHub Innovation Graph (estimado) | Semestral |
| `llm_price_per_1M_tokens` | float | Precio promedio por 1M tokens de input (USD), promedio de OpenAI + Anthropic | OpenAI/Anthropic pricing history pública | Mensual |
| `llm_context_window_k` | int | Ventana de contexto en miles de tokens del modelo top de mercado | Documentación pública de providers | Trimestral |

---

## Variables de Eventos (para DiD)

| Variable | Tipo | Descripción | Valor |
|----------|------|-------------|-------|
| `post_copilot` | binary | 1 si fecha > octubre 2021 (GA de GitHub Copilot) | 0 o 1 |
| `post_chatgpt` | binary | 1 si fecha > noviembre 2022 (lanzamiento ChatGPT) | 0 o 1 |
| `post_deepseek` | binary | 1 si fecha > enero 2025 (DeepSeek-R1 open source) | 0 o 1 |
| `treated` | binary | 1 si empresa adoptó AI tools en <6 meses de cada evento | 0 o 1 |

---

## Fuentes de Datos y Acceso

| Fuente | URL | Formato | Costo | Script de extracción |
|--------|-----|---------|-------|---------------------|
| Yahoo Finance v8 | Vía Dashboard API (localhost) | JSON → CSV | Gratis | `collect_prices.py` |
| SEC EDGAR | https://data.sec.gov/api/xbrl/ | JSON | Gratis | `collect_fundamentals.py` |
| Stack Overflow Survey | https://survey.stackoverflow.co/ | CSV público | Gratis | `collect_survey_data.py` |
| OECD STAN | https://stats.oecd.org/ | CSV | Gratis | Descarga manual |
| BLS MFP | https://www.bls.gov/mfp/ | CSV | Gratis | Descarga manual |
| NIST NVD | https://services.nvd.nist.gov/rest/json/ | JSON | Gratis | `collect_nvd_cves.py` (futura) |

---

## Universo de Empresas

**Criterios de inclusión:**
1. Listada en NYSE o NASDAQ
2. GICS sector "Information Technology", subsector "Software" o "IT Services"
3. Market cap > $500M USD (evita micro-caps con poca liquidez y datos incompletos)
4. Al menos 3 años de datos disponibles en Yahoo Finance

**Tamaño esperado:** ~130–160 empresas

**Clasificación por tipo:**
- `Pure-play software`: empresa cuyo negocio principal es venta de software (Salesforce, Workday)
- `AI-native`: fundada después de 2018 con AI como core del producto (Palantir AI, C3.ai)
- `Platform incumbent`: empresa grande que integró AI a su plataforma existente (MSFT, GOOGL, Oracle)
- `Infrastructure`: cloud y cómputo que habilita AI (AWS/AMZN, Azure/MSFT — tratar con cuidado, son conglomerados)
- `Vertical SaaS`: software especializado por industria (Veeva, Tyler Technologies)

**Nota:** NVDA se incluye como control/comparación pero no es "software" — es hardware/semiconductors. Se usa para el análisis de la cadena de valor de AI.

---

## Convenciones

- Todos los valores monetarios en USD corrientes (no ajustados por inflación en análisis de retornos; ajustados por CPI en análisis de TFP)
- Retornos calculados sobre adjusted close price (ajustado por splits y dividendos)
- Año fiscal varía por empresa; se normaliza al año calendario cuando es posible
- Variables con sufijo `_log` son transformaciones logarítmicas naturales
- Variables con sufijo `_norm` están normalizadas a [0,1]
- `NA` indica dato no disponible; no se imputa sin documentarlo
