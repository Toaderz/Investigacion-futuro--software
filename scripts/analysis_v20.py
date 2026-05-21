"""
analysis_v20.py
Análisis empírico adicional para tesis v2.0:
  - Modelo M5: efectos fijos con interacciones trajectory_type × ai_intensity
  - Fig_new_01: retornos por trayectoria pre/post 2022
  - Fig_new_02: forest plot de coeficientes de interacción

Nota metodológica sobre M5:
  Los efectos principales traj_A y traj_C NO se incluyen como términos aislados porque
  trajectory_type es invariante en el tiempo (clasificado con 10-K FY2021). Al ser
  constante por firma, son perfectamente colineales con EntityEffects y se absorben en la
  transformación within. Solo la interacción con ai_intensity (variante en el tiempo)
  sobrevive. Esta omisión es intencionada y metodológicamente correcta.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

BASE = Path(__file__).parent.parent
DATA = BASE / "data" / "processed"
FIGS = BASE / "output" / "figures"
FIGS.mkdir(parents=True, exist_ok=True)

# ── Cargar panel ──────────────────────────────────────────────────────────────
df = pd.read_csv(DATA / "panel_final.csv")
df = df[df["trajectory_type"].notna()].copy()
df["periodo"] = df["year"].apply(lambda y: "pre_2022" if y <= 2022 else "post_2022")

print(f"Panel cargado: {len(df)} filas, {df['ticker'].nunique()} empresas")
print(f"Distribución trajectory_type: {df.groupby('trajectory_type')['ticker'].nunique().to_dict()}")

# ── Modelo M5: efectos fijos con interacciones ─────────────────────────────────
m5_results = None
m5_note = ""

try:
    from linearmodels.panel import PanelOLS

    df_m5 = df[df["return_annual_pct"].notna() &
               df["ai_intensity"].notna() &
               df["trajectory_type"].notna()].copy()

    # Dummies de trayectoria (B = omitida como categoría base)
    df_m5["traj_A"] = (df_m5["trajectory_type"] == "A").astype(float)
    df_m5["traj_C"] = (df_m5["trajectory_type"] == "C").astype(float)
    df_m5["ai_x_A"] = df_m5["ai_intensity"] * df_m5["traj_A"]
    df_m5["ai_x_C"] = df_m5["ai_intensity"] * df_m5["traj_C"]

    # Controles adicionales si disponibles
    controls = []
    if "tech_debt_proxy" in df_m5.columns:
        df_m5["tech_debt_proxy"] = df_m5["tech_debt_proxy"].fillna(df_m5["tech_debt_proxy"].median())
        controls.append("tech_debt_proxy")
    if "log_revenues" in df_m5.columns:
        df_m5["log_revenues"] = df_m5["log_revenues"].fillna(df_m5["log_revenues"].median())
        controls.append("log_revenues")

    df_idx = df_m5.set_index(["ticker", "year"])

    ctrl_str = " + ".join(controls) if controls else "1"
    formula = f"return_annual_pct ~ ai_intensity + ai_x_A + ai_x_C + {ctrl_str} + EntityEffects + TimeEffects"

    mod5 = PanelOLS.from_formula(formula, data=df_idx)
    res5 = mod5.fit(cov_type='clustered', cluster_entity=True)

    m5_results = res5
    print("\n=== MODELO M5: Efectos Fijos con Interacciones Trayectoria ===")
    print(f"N = {res5.nobs}, Entidades = {df_m5['ticker'].nunique()}")
    print(f"R² within = {res5.rsquared:.4f}")
    print("\nCoeficientes principales:")
    for param, coef, se, pval in zip(
        res5.params.index,
        res5.params.values,
        res5.std_errors.values,
        res5.pvalues.values
    ):
        stars = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.10 else ""
        print(f"  {param:30s} {coef:8.3f}  ({se:.3f})  p={pval:.3f} {stars}")

    m5_note = (
        f"N={res5.nobs}, Tickers={df_m5['ticker'].nunique()}, R²={res5.rsquared:.3f}. "
        f"Traj_B=categoría base. Efectos principales traj_A/traj_C absorbidos por EntityEffects "
        f"(trajectory_type es invariante en el tiempo). SE robustos clustered por entidad."
    )

    # Wild Bootstrap para ai_intensity en M5
    print("\n--- Wild Cluster Bootstrap M5 (ai_intensity, 1000 iter.) ---")
    np.random.seed(42)
    beta_hat = float(res5.params["ai_intensity"])
    se_hat = float(res5.std_errors["ai_intensity"])
    firms_m5 = df_m5["ticker"].unique()
    # Alinear residuos con el panel indexado
    resids_vals = np.asarray(res5.resids).flatten()
    fitted_vals = np.asarray(res5.fitted_values).flatten()
    idx_vals = df_idx.index[:len(resids_vals)]
    resids_series = pd.Series(resids_vals, index=idx_vals)
    fitted_series = pd.Series(fitted_vals, index=idx_vals)
    t_stars = []
    for _ in range(1000):
        v = dict(zip(firms_m5, np.random.choice([-1, 1], size=len(firms_m5))))
        df_b = df_idx.copy()
        weights = df_b.index.get_level_values(0).map(v).values
        y_star_vals = fitted_series.values + weights * resids_series.values
        df_b["y_star"] = y_star_vals
        formula_b = formula.replace("return_annual_pct", "y_star")
        try:
            res_b = PanelOLS.from_formula(formula_b, data=df_b).fit(
                cov_type='clustered', cluster_entity=True)
            beta_b = float(res_b.params.get("ai_intensity", np.nan))
            se_b = float(res_b.std_errors.get("ai_intensity", np.nan))
            if not np.isnan(beta_b) and not np.isnan(se_b) and se_b > 0:
                t_stars.append((beta_b - beta_hat) / se_b)
        except Exception:
            pass

    t_arr = np.array([t for t in t_stars if not np.isnan(t)])
    if len(t_arr) > 100:
        ci_lo = beta_hat - np.percentile(t_arr, 97.5) * se_hat
        ci_hi = beta_hat - np.percentile(t_arr, 2.5) * se_hat
        p_wild = np.mean(np.abs(t_arr) > np.abs(beta_hat / se_hat))
        print(f"  beta_ai = {beta_hat:.3f}, SE = {se_hat:.3f}")
        print(f"  Wild Bootstrap 95% CI: [{ci_lo:.3f}, {ci_hi:.3f}]")
        print(f"  p_wild = {p_wild:.3f}, n_valid = {len(t_arr)}")
        m5_note += f" Wild Bootstrap 95% CI (ai_intensity): [{ci_lo:.3f}, {ci_hi:.3f}], p_wild={p_wild:.3f}."
    else:
        print(f"  Iteraciones válidas insuficientes: {len(t_arr)}")

except ImportError:
    print("linearmodels no disponible; M5 no calculado")
    m5_results = None

# ── Fig_new_01: Retornos por trayectoria pre/post 2022 ──────────────────────────
print("\n--- Generando fig_new_01: Retornos por trayectoria ---")

traj_colors = {"A": "#E63946", "B": "#6C757D", "C": "#2196F3"}
traj_labels = {
    "A": "Tray. A\nDiferenciación",
    "B": "Tray. B\n\"Atrapados\"\n(Base)",
    "C": "Tray. C\nPlataforma/Infra"
}

fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
fig.suptitle("Retornos anuales por trayectoria estratégica\npre y post ChatGPT (nov-2022)",
             fontsize=13, fontweight='bold', y=1.02)

for ax_idx, (periodo, ax, title) in enumerate([
    ("pre_2022", axes[0], "Período pre-ChatGPT\n(2019–2022)"),
    ("post_2022", axes[1], "Período post-ChatGPT\n(2023–2025)")
]):
    sub = df[df["periodo"] == periodo]
    data_traj = [sub[sub["trajectory_type"] == t]["return_annual_pct"].dropna() for t in ["A", "B", "C"]]

    bp = ax.boxplot(data_traj, patch_artist=True, notch=False,
                    medianprops=dict(color='black', linewidth=2),
                    whiskerprops=dict(linewidth=1.5),
                    capprops=dict(linewidth=1.5),
                    flierprops=dict(marker='o', markersize=3, alpha=0.5))

    for patch, traj in zip(bp['boxes'], ["A", "B", "C"]):
        patch.set_facecolor(traj_colors[traj])
        patch.set_alpha(0.75)

    # Añadir medias como puntos
    for i, (traj, d) in enumerate(zip(["A", "B", "C"], data_traj)):
        mean_val = d.mean()
        ax.scatter(i + 1, mean_val, color='black', zorder=5, s=50, marker='D')
        ax.annotate(f'μ={mean_val:.1f}%', xy=(i + 1, mean_val),
                    xytext=(10, 5), textcoords='offset points',
                    fontsize=8, ha='left')

    ax.set_title(title, fontsize=11)
    ax.set_xticklabels([traj_labels[t] for t in ["A", "B", "C"]], fontsize=9)
    ax.set_ylabel("Retorno anual (%)" if ax_idx == 0 else "", fontsize=10)
    ax.axhline(0, color='gray', linestyle='--', alpha=0.5, linewidth=0.8)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(-150, 300)

# Leyenda
legend_patches = [mpatches.Patch(color=traj_colors[t], alpha=0.75,
                                  label=f"Tray. {t}: {lbl.split(chr(10))[1]}")
                  for t, lbl in traj_labels.items()]
fig.legend(handles=legend_patches, loc='lower center', ncol=3,
           bbox_to_anchor=(0.5, -0.05), fontsize=9)

plt.tight_layout()
fig_path1 = FIGS / "fig_new_01_trajectory_returns.png"
plt.savefig(fig_path1, dpi=150, bbox_inches='tight')
plt.close()
print(f"  Guardado: {fig_path1}")

# ── Fig_new_02: Forest plot de coeficientes M5 ──────────────────────────────────
if m5_results is not None:
    print("\n--- Generando fig_new_02: Forest plot M5 ---")

    params_of_interest = ["ai_intensity", "ai_x_A", "ai_x_C"]
    labels_map = {
        "ai_intensity": "AI_intensity\n(Tray. B base)",
        "ai_x_A": "AI_intensity × Tray. A\n(Diferenciación vs. Base)",
        "ai_x_C": "AI_intensity × Tray. C\n(Plataforma vs. Base)"
    }

    coefs = []
    for p in params_of_interest:
        if p in m5_results.params.index:
            coefs.append({
                "param": p,
                "label": labels_map[p],
                "coef": m5_results.params[p],
                "se": m5_results.std_errors[p],
                "pval": m5_results.pvalues[p]
            })

    if coefs:
        fig, ax = plt.subplots(figsize=(9, 4))
        fig.suptitle("Modelo M5: Coeficientes de efectos fijos con interacciones de trayectoria\n"
                     "(Variable dependiente: retorno anual %; Trayectoria B = categoría base)",
                     fontsize=11, fontweight='bold')

        y_pos = range(len(coefs))
        colors_fp = [traj_colors.get(
            "A" if "x_A" in c["param"] else "C" if "x_C" in c["param"] else "B", "#555")
                     for c in coefs]

        for i, (c, col) in enumerate(zip(coefs, colors_fp)):
            ci_lo = c["coef"] - 1.96 * c["se"]
            ci_hi = c["coef"] + 1.96 * c["se"]
            ax.plot([ci_lo, ci_hi], [i, i], color=col, linewidth=3, alpha=0.7)
            ax.scatter(c["coef"], i, color=col, zorder=5, s=80)
            stars = "***" if c["pval"] < 0.01 else "**" if c["pval"] < 0.05 else "*" if c["pval"] < 0.10 else "n.s."
            ax.annotate(f"{c['coef']:.3f} ({stars})",
                        xy=(c["coef"], i),
                        xytext=(8, 0), textcoords='offset points',
                        fontsize=9, va='center')

        ax.axvline(0, color='black', linestyle='--', linewidth=1, alpha=0.6)
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels([c["label"] for c in coefs], fontsize=9)
        ax.set_xlabel("Coeficiente (pp de retorno anual por unidad de AI_intensity)", fontsize=9)
        ax.set_xlim(min(c["coef"] - 2.5 * c["se"] for c in coefs) - 0.5,
                    max(c["coef"] + 2.5 * c["se"] for c in coefs) + 0.5)
        ax.grid(axis='x', alpha=0.3)
        ax.text(0.98, 0.02, f"N={m5_results.nobs}  |  SE clustered por firma\n"
                             f"Tray. A: Diferenciación  |  Tray. C: Plataforma/Infra  |  Tray. B: base omitida",
                transform=ax.transAxes, fontsize=7.5, ha='right', va='bottom',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.4))

        plt.tight_layout()
        fig_path2 = FIGS / "fig_new_02_m5_forestplot.png"
        plt.savefig(fig_path2, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Guardado: {fig_path2}")

# ── Resumen de estadística descriptiva por trayectoria ────────────────────────
print("\n=== ESTADÍSTICAS DESCRIPTIVAS POR TRAYECTORIA (para Cuadro Sección 5.3) ===")
traj_table = df.groupby(["trajectory_type", "periodo"])[
    ["return_annual_pct", "ai_intensity", "op_margin"]
].agg(["mean", "median", "std", "count"]).round(2)
print(traj_table.to_string())

# Guardar resumen M5
summary_path = DATA / "m5_summary.txt"
with open(summary_path, "w", encoding="utf-8") as f:
    f.write("=== MODELO M5 SUMMARY ===\n")
    if m5_results is not None:
        f.write(str(m5_results.summary) + "\n\n")
        f.write(f"NOTA: {m5_note}\n")
    else:
        f.write("linearmodels no disponible\n")
print(f"\nResumen M5 guardado: {summary_path}")
print("\nAnálisis v2.0 completado.")
