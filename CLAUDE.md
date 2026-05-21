# CLAUDE.md — Investigación: Futuro del Software ante la IA Generativa

## Contexto del proyecto

Tesis universitaria formal — Universidad Panamericana  
**Investigador:** Alejandro Jiménez (alejandro.jimenez@evolveam.com.mx)  
**Fecha de inicio:** 2026-05-17  
**Versión actual:** v2.0 (pivote estratégico completo — Mayo 2026)

**Pregunta central:** ¿Hacia dónde van las empresas de software dado el avance acelerado y democratización de la IA generativa? (Analogía DC→AC: más accesible y potente, pero requiere reestructuración completa de la industria.)

---

## Estado actual (2026-05-20) — PROYECTO COMPLETO

### Todo completado ✅

- [x] Panel de datos: 66 empresas × 2019-2025, fusionado y limpio
- [x] Columna `trajectory_type` (A/B/C) clasificada ex-ante con 10-K FY2021 — en `panel_final.csv`
- [x] 4 scripts de recolección funcionando
- [x] `analysis_v20.py`: Modelo M5 (FE + interacciones trayectoria), Wild Cluster Bootstrap, fig_new_01 y fig_new_02
- [x] 14 figuras en `output/figures/` (12 originales + 2 nuevas v2.0)
- [x] `output/thesis.md` — tesis v2.0 completa (marco teórico Teece/Barney/Williamson/Porter, taxonomía, evidencia empírica, prospectiva)
- [x] `output/thesis.html` — standalone HTML con figuras base64 embebidas, MathJax, índice navegable

### Nada pendiente

---

## Estructura del proyecto

```
Investigacion futuro software/
├── data/
│   ├── raw/
│   │   ├── prices_daily.csv           # OHLCV diario, 66 tickers, 2019-2025
│   │   ├── returns_annual.csv         # Retornos anuales ajustados
│   │   ├── fundamentals_annual.csv    # Márgenes, I+D, empleados (SEC EDGAR)
│   │   ├── yahoo_current.csv          # Snapshot Yahoo Finance
│   │   └── so_survey.csv              # Stack Overflow Survey 2023-2025
│   └── processed/
│       ├── panel_final.csv            # 66 empresas × 7 años, con trajectory_type
│       ├── benchmarks.csv             # Índices de referencia
│       ├── panel_summary.csv          # Estadísticas descriptivas
│       ├── bootstrap_ai_intensity.csv # 1000 iteraciones bootstrap
│       ├── event_study_chatgpt.csv    # Datos event study DiD
│       └── m5_summary.txt             # Resultados Modelo M5
├── scripts/
│   ├── collect_prices.py              # Extrae precios Yahoo Finance
│   ├── collect_fundamentals.py        # Extrae fundamentales SEC EDGAR
│   ├── collect_survey_data.py         # Procesa SO Survey
│   ├── build_panel.py                 # Ensambla panel + trajectory_type
│   ├── analysis_v20.py                # M5 + fig_new_01 + fig_new_02
│   ├── generate_html_v20.py           # Genera thesis.html desde thesis.md
│   └── add_toc.py                     # Añade índice navegable a thesis.html
├── notebooks/
│   ├── 01_panel_regression.ipynb      # Regresiones OLS + DiD + bootstrap
│   ├── 02_figures.ipynb               # 12 figuras originales
│   └── 03_scenarios.ipynb             # 3 escenarios Monte Carlo
├── output/
│   ├── figures/                       # fig01–fig12 + fig_new_01, fig_new_02
│   ├── tables/                        # Tablas AEA (CSV)
│   ├── thesis.md                      # Tesis v2.0 (fuente)
│   └── thesis.html                    # Tesis v2.0 (HTML standalone, ~1.7 MB)
├── hypotheses.md                      # Hipótesis pre-registradas — NO modificar
├── data_dictionary.md                 # Descripción de todas las variables
├── CLAUDE.md                          # Este archivo
└── README.md                          # Documentación del proyecto
```

---

## Taxonomía central del trabajo (v2.0)

La clasificación `trajectory_type` es **invariante en el tiempo** (ex-ante, 10-K FY2021):

| Trayectoria | Definición | Porter | n firmas | Ejemplo |
|-------------|-----------|--------|----------|---------|
| **A** | Software dominio técnico/regulatorio inimitable | Diferenciación | 16 | CRWD, VEEV, CDNS |
| **B** | SaaS horizontal sin moat claro — **CATEGORÍA BASE** | Stuck in the middle | 19 | ZM, TWLO, CTSH |
| **C** | Cloud/plataforma/efectos de red | Platform/Scale | 31 | MSFT, NVDA, SNOW |

**Nota metodológica crítica:** `traj_A` y `traj_C` como efectos principales NO se incluyen en el Modelo M5 porque son perfectamente colineales con `EntityEffects` (variable invariante en el tiempo). Solo las interacciones `ai_intensity × traj_A/C` sobreviven la transformación within. Esta omisión es intencionada y mecánicamente necesaria.

---

## Datos clave del panel

- **Universo:** 66 empresas de software + 7 benchmarks (^GSPC, QQQ, IGV, SKYY, ROBT, CIBR)
- **Periodo:** 2019–2025 (7 años; 437 observaciones empresa-año)
- **Variable dependiente:** `return_annual_pct` (retorno ajustado anual %)
- **Variable independiente clave:** `ai_intensity` (índice 0–100, compuesto)

### Componentes de AI_intensity
- `ai_product_binary` (40%): 1 si empresa tiene producto AI generativa lanzado ese año
- `rd_intensity_norm` (30%): I+D / Ingresos, normalizado min-max por año
- `ai_mentions_proxy` (30%): años desde lanzamiento (0→1 en 3 años)

### Eventos exógenos para DiD
- `post_copilot`: 2021 (GitHub Copilot GA)
- `post_chatgpt`: 2022 (ChatGPT nov-2022) — **evento principal**
- `post_deepseek`: 2025 (DeepSeek-R1 ene-2025)

---

## Resultados principales (v2.0)

| Métrica | Valor |
|---------|-------|
| Chow test ChatGPT | F=13.4, p<0.001 |
| Retorno Tray. C post-2022 | 45.9% (+17.1 pp vs. pre) |
| Retorno Tray. A post-2022 | 24.3% (−9.6 pp vs. pre) |
| Retorno Tray. B post-2022 | 25.2% (+7.9 pp vs. pre) |
| M5 ai_intensity | −14.006 (n.s.; N=66 limitado) |
| M5 ai_x_A (prima A sobre B) | +13.929 (n.s.) |
| M5 ai_x_C (prima C sobre B) | +14.399 (n.s.) |
| tech_debt_proxy | −0.243 (p<0.001) |
| SO Survey adopción 2025 | 68% (vs. 44% en 2023) |
| SO Survey confianza 2025 | 29% (vs. 45% en 2023) |

---

## Reglas para esta investigación

- **NUNCA** modificar `hypotheses.md` después de ver resultados
- Reportar todos los tests, no solo los significativos
- Outliers (NVDA, MSFT) documentados; incluidos con `log_revenues` como control
- Todo análisis usa `np.random.seed(42)` para reproducibilidad
- Datos de Gartner/IDC evitar — no replicables; preferir Yahoo Finance + SEC EDGAR
- Lenguaje causal ("impacto de la IA") solo donde hay cita; usar "asociación" en el resto

---

## Si se necesita regenerar el HTML

```bash
# Desde el directorio raíz del proyecto:
python scripts/generate_html_v20.py   # genera thesis.html desde thesis.md
python scripts/add_toc.py              # añade índice navegable
```

Requiere: `pip install markdown`
