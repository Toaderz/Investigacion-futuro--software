# Hipótesis Pre-registradas
**Fecha de registro:** 2026-05-17  
**Investigador:** Alejandro Jiménez  
**Proyecto:** Futuro de las Empresas de Software ante la IA Generativa

> Pre-registration: estas hipótesis se registran ANTES de correr cualquier regresión para evitar p-hacking y HARKing (Hypothesizing After Results are Known).

---

## Pregunta Central de Investigación

¿Hacia dónde van las empresas de software dado el avance acelerado y democratización de la IA generativa? ¿Este cambio tecnológico crea ganadores y perdedores definidos, o transforma al sector de manera uniforme?

**Analogía conceptual:** El cambio de corriente continua (DC) a corriente alterna (AC) — una tecnología más accesible, más potente y con mayor alcance, pero que requirió reestructuración de toda la industria eléctrica y creó nuevos modelos de negocio mientras volvía obsoletos a otros.

---

## H1 — Hipótesis de Bifurcación del Mercado

**Enunciado:** La adopción de IA generativa en empresas de software no produce resultados uniformes, sino una polarización donde las empresas de alta adopción divergen significativamente de las de baja adopción en retornos, valuación y márgenes.

| | Formulación |
|--|--|
| **H₀** | No existe diferencia estadísticamente significativa en retornos ajustados al riesgo entre empresas de software con alta vs. baja intensidad de AI (top vs. bottom quintil de AI_intensity) |
| **H₁** | Las empresas en el quintil superior de AI_intensity tienen mayor retorno medio Y mayor varianza, evidenciando bifurcación (ganadores grandes, perdedores grandes) |

**Tests estadísticos:**
- Welch two-sample t-test (medias de retorno por grupo)
- Levene / F-test (igualdad de varianzas)
- Regresión con interacción: `Return_it = β₀ + β₁·AI_intensity_it + β₂·Year_t + β₃·(AI_intensity × Year) + Controls + ε`
- Umbral de significancia: α = 0.05 (bilateral)

**Variables:**
- Variable dependiente: retorno ajustado anual (1Y adjusted return)
- Variable independiente clave: AI_intensity (índice compuesto, ver data_dictionary.md)
- Controles: tamaño (log market cap), sector subsector, región, beta

**Predicción direccional:** Se espera H₁ verdadera. El efecto debería amplificarse post-ChatGPT (nov 2022).

---

## H2 — Hipótesis de Paradoja de Productividad

**Enunciado:** Las ganancias brutas de productividad atribuidas a la IA generativa en desarrollo de software se ven parcialmente o totalmente anuladas por el aumento en deuda técnica, bugs, y costos de mantenimiento ("vibe coding problem").

| | Formulación |
|--|--|
| **H₀** | El coeficiente de AI_adoption en una regresión sobre profit margin es no significativamente diferente de cero cuando se incluye un proxy de deuda técnica |
| **H₁** | El coeficiente de AI_adoption es positivo y significativo en ausencia del control de deuda técnica, pero se reduce (o invierte) cuando se incluye el proxy de tech_debt |

**Tests estadísticos:**
- OLS sin control de tech_debt: `ProfitMargin_it = β₀ + β₁·AI_adoption_it + Controls + ε`
- OLS con control de tech_debt: `ProfitMargin_it = β₀ + β₁·AI_adoption_it + β₂·TechDebt_it + Controls + ε`
- Comparar β₁ entre ambas especificaciones (Frisch-Waugh-Lovell)
- Umbral de significancia: α = 0.05

**Proxy de deuda técnica:** ratio de gastos en mantenimiento/soporte sobre ingresos totales (extraído de SEC 10-K filings)

**Predicción direccional:** Se espera que β₁ se reduzca al incluir tech_debt. Si se invierte completamente, el efecto neto de la IA sería negativo en margen.

---

## H3 — Hipótesis de Reto a Acemoglu (TFP)

**Enunciado:** El crecimiento de la Productividad Total de los Factores (TFP) en el sector software excede la proyección de Acemoglu (2024) de 0.53–0.66% acumulado en 10 años, especialmente en subsectores con alta adopción de IA.

| | Formulación |
|--|--|
| **H₀** | El TFP observado en empresas de software con AI_adoption > 70% es ≤ 0.66% acumulado en el periodo analizado (alineado con proyección Acemoglu) |
| **H₁** | El TFP excede 0.66% acumulado, rechazando la proyección conservadora de Acemoglu |

**Tests estadísticos:**
- One-sample t-test vs. valor teórico μ₀ = 0.66%
- Datos fuente: BLS Multifactor Productivity Tables (sector Information Technology) + OECD STAN
- Periodo: 2021-2025 (4 años post-inicio del ciclo AI generativa)

**Nota metodológica:** La medición de TFP sectorial requiere datos de OECD/BLS, no de Yahoo Finance. Esta hipótesis usa fuentes macroeconómicas, no datos de empresas individuales.

**Predicción direccional:** Se espera rechazo de H₀ — el TFP real supera la proyección Acemoglu en subsectores de alta adopción.

---

## H4 — Hipótesis de Velocidad de Adopción sin Precedente

**Enunciado:** La curva de adopción de la IA generativa en la industria del software tiene una pendiente estadísticamente mayor que la de tecnologías transformadoras previas (internet/web, cloud computing, móvil).

| | Formulación |
|--|--|
| **H₀** | La pendiente de adopción de IA generativa (2022-2025) no difiere significativamente de la de internet (1995-2000) y cloud (2008-2013) en sus primeros 3 años |
| **H₁** | La pendiente de adopción es significativamente mayor, confirmando una aceleración estructural en la velocidad de adopción tecnológica |

**Tests estadísticos:**
- Chow test de cambio estructural entre periodos de tecnologías
- Comparación de coeficientes de crecimiento por periodo (regresión logística de curva S)
- Datos: Stack Overflow Developer Survey 2018-2024 (adopción AI), datos históricos de adopción de tecnologías anteriores

**Predicción direccional:** Se espera rechazo de H₀. La hipótesis del "7.7x más rápido" del intento anterior necesita validación estadística formal.

---

## Variables no-hipoteizadas a explorar (exploratory, no confirmatorio)

Las siguientes preguntas se analizan de forma exploratoria y NO se usarán para confirmar/rechazar hipótesis formales:

1. ¿Las empresas AI-nativas (fundadas post-2020) tienen perfiles de riesgo-retorno diferentes a las incumbentes que adoptaron IA?
2. ¿Qué sectores dentro del software muestran la mayor heterogeneidad en respuesta a la IA? (superespecialización vs. commoditización)
3. ¿El precio decreciente de tokens LLM (exponencial 2023-2025) tiene correlación con el aumento de márgenes en empresas de software que los usan?
4. ¿Las estrategias de las empresas AI (Claude Design, Copilot for X, Gemini Enterprise) muestran especialización por vertical o generalización?

---

## Protocolo anti-sesgo

- No se modificarán las hipótesis después de ver los datos
- Si los resultados son contrarios a las predicciones direccionales, se reportarán tal cual
- Se reportarán todos los tests, no solo los que resulten significativos
- Los outliers identificados se documentarán antes de decidir si incluirlos o excluirlos
- Se aplicará corrección de Bonferroni para comparaciones múltiples donde aplique
