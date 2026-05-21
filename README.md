# Adaptación estratégica o mortandad: Trayectorias de las empresas de software ante la democratización de la IA generativa (2019–2025)

Tesis universitaria formal — Universidad Panamericana  
**Autor:** Alejandro Jiménez (alejandro.jimenez@evolveam.com.mx)  
**Versión:** 2.0 (Mayo 2026)  
**Estado:** Completa — datos, análisis y redacción finalizados

---

## Pregunta central

¿Hacia dónde van las empresas de software dado el avance acelerado y democratización de la IA generativa?

*Analogía conductora DC→AC:* Así como la transición de corriente continua a corriente alterna democratizó la energía y reestructuró la industria eléctrica, la IA generativa democratiza la producción de software — creando ganadores, perdedores, y una nueva infraestructura sobre la que todos operan.

---

## Hallazgo principal

Las 66 empresas del panel no responden de manera uniforme al shock de la IA generativa. Se identifican **tres trayectorias estratégicas**, clasificadas ex-ante con datos de 10-K FY2021 (antes de ChatGPT, nov-2022):

| Trayectoria | Descripción | Retorno medio post-2022 |
|-------------|-------------|------------------------|
| **A — Diferenciación** | Software de dominio técnico o regulatorio inimitable (ciberseguridad, compliance, EDA, biofarma) | 24.3% |
| **B — "Atrapados en el medio"** | SaaS horizontal sin moat claro; categoría base en regresiones | 25.2% |
| **C — Plataforma/Infraestructura** | Cloud, APIs, ecosistemas y efectos de red | **45.9%** |

El Test de Chow confirma inestabilidad estructural pre/post ChatGPT (F=13.4, p<0.001).

---

## Marco teórico

- **Schumpeter (1942):** destrucción creativa y transiciones de industria
- **Barney (1991):** Visión Basada en Recursos — la IA como herramienta no es VRIN; la reconfiguración organizacional sí
- **Teece, Pisano & Shuen (1997):** Capacidades Dinámicas — triada *sensing / seizing / transforming* aplicada al shock LLM
- **Williamson (1975):** Economía de Costos de Transacción — si codificar es casi gratuito, ¿por qué existen grandes empresas de software?
- **Porter (1980):** Estrategias genéricas como ancla de las tres trayectorias

---

## Metodología

- **Universo:** 66 empresas de software cotizadas (NYSE/NASDAQ) + 7 benchmarks de referencia
- **Periodo:** 2019–2025 (7 años, datos anuales; 437 observaciones empresa-año)
- **Modelo principal (M5):** Panel con efectos fijos + interacciones de trayectoria

$$R_{it} = \alpha_i + \gamma_t + \beta_1 AI_{it} + \beta_2 (AI_{it} \times Traj_A{}_i) + \beta_3 (AI_{it} \times Traj_C{}_i) + \beta_4 TD_{it} + \beta_5 \ln(Rev_{it}) + \varepsilon_{it}$$

- **Identificación causal:** Difference-in-Differences usando ChatGPT (nov-2022) como evento exógeno
- **Robustez:** SE clustered por firma, Wild Cluster Bootstrap (1,000 iter., Rademacher)
- **Clasificación ex-ante:** `trajectory_type` asignado con 10-K FY2021 para evitar sesgo retrospectivo

---

## Fuentes de datos

| Fuente | Datos | Acceso |
|--------|-------|--------|
| Yahoo Finance v8 | Precios históricos, market cap, fundamentales | Gratuito (sin API key) |
| SEC EDGAR (data.sec.gov) | Ingresos, I+D, márgenes operativos, empleados | Gratuito |
| Stack Overflow Developer Survey 2023–2025 | Adopción AI (44%→68%), confianza (45%→29%) | Gratuito (survey.stackoverflow.co) |

---

## Estructura del repositorio

```
├── data/
│   ├── raw/                        # Datos sin procesar (precios, fundamentales, SO survey)
│   └── processed/
│       ├── panel_final.csv         # 66 empresas × 2019-2025, incluye trajectory_type
│       ├── benchmarks.csv          # Índices de referencia
│       ├── bootstrap_ai_intensity.csv
│       ├── event_study_chatgpt.csv
│       └── m5_summary.txt          # Resultados del Modelo M5
├── scripts/
│   ├── collect_prices.py           # Extrae precios Yahoo Finance
│   ├── collect_fundamentals.py     # Extrae datos SEC EDGAR
│   ├── collect_survey_data.py      # Procesa Stack Overflow Survey
│   ├── build_panel.py              # Ensambla panel_final.csv (incluye trajectory_type)
│   ├── analysis_v20.py             # Modelo M5 + figuras nuevas (v2.0)
│   ├── generate_html_v20.py        # Genera thesis.html desde thesis.md
│   └── add_toc.py                  # Añade índice navegable a thesis.html
├── notebooks/
│   ├── 01_panel_regression.ipynb   # Regresiones OLS + DiD + bootstrap
│   ├── 02_figures.ipynb            # Figuras de resultados
│   └── 03_scenarios.ipynb          # Escenarios Monte Carlo
├── output/
│   ├── figures/                    # fig01–fig12 + fig_new_01, fig_new_02 (PNG)
│   ├── tables/                     # Tablas formato AEA (CSV)
│   ├── thesis.md                   # Tesis completa v2.0 (fuente Markdown)
│   └── thesis.html                 # Tesis completa v2.0 (HTML standalone, figuras embebidas)
├── hypotheses.md                   # Hipótesis pre-registradas (NO modificar post-datos)
├── data_dictionary.md              # Descripción de todas las variables
├── CLAUDE.md                       # Instrucciones para el asistente IA
└── README.md                       # Este archivo
```

---

## Cómo reproducir el análisis

### 1. Instalar dependencias

```bash
pip install pandas numpy matplotlib seaborn statsmodels scipy yfinance linearmodels markdown
```

### 2. Recolectar datos

```bash
python scripts/collect_prices.py
python scripts/collect_fundamentals.py
python scripts/collect_survey_data.py --use-published
```

### 3. Construir el panel (incluye clasificación de trayectorias)

```bash
python scripts/build_panel.py
```

### 4. Análisis v2.0 (Modelo M5 + figuras nuevas)

```bash
python scripts/analysis_v20.py
```

### 5. Generar el documento HTML

```bash
python scripts/generate_html_v20.py
python scripts/add_toc.py
```

### 6. Notebooks (análisis exploratorio adicional)

```
notebooks/01_panel_regression.ipynb
notebooks/02_figures.ipynb
notebooks/03_scenarios.ipynb
```

---

## Datos de adopción IA (Stack Overflow Developer Survey)

| Año | Usan actualmente | Planean usar | No planean | Confían en AI | n muestra |
|-----|-----------------|--------------|------------|---------------|-----------|
| 2023 | 44% | 26% | 30% | 45% | 90,000 |
| 2024 | 62% | 14% | 24% | 40% | 65,437 |
| 2025 | 68% | 16% | 16% | 29% | n/d |

*Fuente: Stack Overflow Developer Survey 2023–2025. survey.stackoverflow.co*

---

## Figuras generadas

| Figura | Descripción |
|--------|-------------|
| fig01_event_study | Event study: retornos acumulados pre/post ChatGPT |
| fig02_quintiles | Retornos medios por quintil de AI_intensity |
| fig03_returns_by_group | Retornos High AI vs. Low AI vs. benchmarks |
| fig04_opmargin_time | Margen operativo en el tiempo por grupo |
| fig05_so_vs_returns | Adopción SO vs. retorno del sector (scatter) |
| fig06_bootstrap_ai | Bootstrap: distribución del coeficiente AI_intensity |
| fig07_scatter_ai_return | Scatter: AI_intensity vs. retorno por empresa |
| fig08_so_spectrum | Espectro de adopción SO (stacked bar 2023–2025) |
| fig09_benchmarks | Retornos benchmarks vs. empresas del panel |
| fig10_scenarios | 3 escenarios de retorno (conservador/base/acelerado) |
| fig11_sensitivity | Análisis de sensibilidad de supuestos clave |
| fig12_bifurcation | Diagrama conceptual de bifurcación del mercado |
| **fig_new_01** | **Retornos por trayectoria estratégica pre/post 2022 (v2.0)** |
| **fig_new_02** | **Forest plot Modelo M5: coeficientes de interacción (v2.0)** |

---

## Limitaciones

1. **N=66** — potencia estadística limitada; IC del Wild Bootstrap son amplios (cost of FE + clustering con muestra pequeña)
2. **trajectory_type** es variable observada, no randomizada — clasificación ex-ante documentada y replicable
3. **AI_intensity** es un índice construido (no observable directamente en datos públicos)
4. **Sesgo mega-cap en Trayectoria C** — `log_revenues` controla parcialmente pero no elimina el "mega-cap premium" de 2023–2024
5. **Sesgo de supervivencia** — el universo excluye empresas que quebraron o fueron adquiridas

---

## Citación

```
Jiménez, A. (2026). Adaptación estratégica o mortandad: Trayectorias de las empresas
  de software ante la democratización de la IA generativa (2019–2025).
  Tesis, Universidad Panamericana.
```
