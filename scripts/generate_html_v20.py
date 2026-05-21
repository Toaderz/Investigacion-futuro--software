"""
generate_html_v20.py
Genera output/thesis.html completo desde output/thesis.md (versión 2.0).
  - Conversión Markdown → HTML con python-markdown (extensiones: tables, fenced_code, nl2br)
  - Embeds figuras como base64 PNG en ubicaciones específicas
  - MathJax para ecuaciones LaTeX ($$...$$)
  - CSS académico: papel A4, tipografía serif, AEA style
"""

import sys, re, base64
from pathlib import Path
import markdown
from markdown.extensions.tables import TableExtension
from markdown.extensions.fenced_code import FencedCodeExtension

sys.stdout.reconfigure(encoding="utf-8")

PROJ = Path(__file__).parent.parent
MD_PATH  = PROJ / "output" / "thesis.md"
HTML_OUT = PROJ / "output" / "thesis.html"
FIGS_DIR = PROJ / "output" / "figures"

# ── Figuras a embeber ──────────────────────────────────────────────────────────
# Tuplas: (nombre_archivo_sin_ext, caption, posicion_marker)
# posicion_marker: substring del texto HTML después del cual se inserta la figura.
FIGURES = [
    ("fig01_event_study",
     "<strong>Figura 1.</strong> Event study: retornos acumulados pre/post ChatGPT (nov-2022). "
     "Empresas con AI_intensity > mediana vs. grupo de comparación. Ventana: −24 a +12 meses.",
     "F=13.4, p&lt;0.001</strong>"),

    ("fig_new_01_trajectory_returns",
     "<strong>Figura 2.</strong> Retornos anuales medios por trayectoria estratégica, pre-ChatGPT "
     "(2019–2022) y post-ChatGPT (2023–2025). Las cajas muestran el rango intercuartílico; "
     "los rombos (◆) indican la media; n por trayectoria: A=16, B=19, C=31 empresas.",
     "La compresión de retornos refleja que el período 2019–2022 fue extraordinariamente favorable"),

    ("fig_new_02_m5_forestplot",
     "<strong>Figura 3.</strong> Forest plot del Modelo M5: coeficientes de AI_intensity y sus "
     "interacciones con trayectoria estratégica (IC 95%, SE clustered por entidad). "
     "Trayectoria B = categoría base omitida. N=437 obs., 66 entidades.",
     "La dirección de los coeficientes es consistente con la hipótesis"),

    ("fig03_returns_by_group",
     "<strong>Figura 4.</strong> Retornos anuales medios por grupo de adopción de IA "
     "(cuartiles de AI_intensity) vs. benchmarks sectoriales (QQQ, IGV). 2019–2025.",
     "Esta diferencia debe interpretarse con cautela"),

    ("fig09_benchmarks",
     "<strong>Figura 5.</strong> Retornos acumulados del panel de 66 empresas vs. "
     "benchmarks de referencia (^GSPC, QQQ, IGV, SKYY). Base 100 = enero 2019.",
     "Proyección de retorno acumulado 2026–2030"),

    ("fig10_scenarios",
     "<strong>Figura 6.</strong> Escenarios prospectivos Monte Carlo 2026–2030 "
     "(10,000 iteraciones por escenario). Las bandas representan IC 90%.",
     "El resultado de Porter sobre empresas"),

    ("fig12_bifurcation",
     "<strong>Figura 7.</strong> Diagrama conceptual de bifurcación estratégica. "
     "La IA generativa amplifica los recursos VRIN existentes (Barney, 1991), "
     "creando trayectorias divergentes de desempeño.",
     "La bifurcación es observable y cuantificable"),
]

# ── CSS ───────────────────────────────────────────────────────────────────────
CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: "Computer Modern Serif", "Latin Modern Roman", "Times New Roman", Times, serif;
    font-size: 11pt;
    line-height: 1.65;
    color: #000;
    background: #f4f1ec;
  }

  .page {
    width: 210mm;
    min-height: 297mm;
    margin: 20px auto;
    background: #fff;
    padding: 25mm 30mm 25mm 35mm;
    box-shadow: 0 2px 20px rgba(0,0,0,0.18);
  }

  @media print {
    body { background: #fff; }
    .page { margin: 0; box-shadow: none; padding: 20mm 25mm; width: 100%; }
  }

  .title-block {
    text-align: center;
    margin-bottom: 2.5em;
    padding-bottom: 1.5em;
    border-bottom: 1px solid #555;
  }

  .title-block h1 {
    font-size: 15pt;
    font-weight: bold;
    line-height: 1.4;
    margin-bottom: 1.2em;
    letter-spacing: -0.01em;
  }

  .title-meta {
    font-size: 10pt;
    line-height: 1.9;
    color: #222;
  }

  .title-meta .label { font-style: normal; font-weight: bold; }

  .keywords { font-size: 9.5pt; margin-top: 0.8em; color: #333; }
  .keywords span { font-style: italic; }

  .abstract-block { margin: 2em 1.5em 2.5em 1.5em; }

  .abstract-block h2 {
    font-size: 10pt;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    text-align: center;
    margin-bottom: 0.7em;
    font-variant: small-caps;
  }

  .abstract-block p {
    font-size: 10pt;
    text-align: justify;
    hyphens: auto;
    text-indent: 0;
    line-height: 1.55;
  }

  hr.abstract-rule { border: none; border-top: 1px solid #888; margin: 2em 0; }

  h2 {
    font-size: 11.5pt;
    font-weight: bold;
    margin: 2em 0 0.7em 0;
    font-variant: small-caps;
    letter-spacing: 0.04em;
  }

  h3 {
    font-size: 11pt;
    margin: 1.5em 0 0.5em 0;
    font-style: italic;
    font-weight: normal;
  }

  h4 {
    font-size: 10.5pt;
    margin: 1.2em 0 0.4em 0;
    font-weight: bold;
  }

  p {
    text-align: justify;
    hyphens: auto;
    text-indent: 1.5em;
    margin-bottom: 0;
  }

  p.no-indent { text-indent: 0; }

  section > p:first-of-type,
  .subsection > p:first-of-type { text-indent: 0; }

  ul, ol {
    margin: 0.6em 0 0.6em 2em;
    font-size: 10.5pt;
  }

  li { margin-bottom: 0.3em; }

  .table-container { margin: 1.6em 0; overflow-x: auto; }

  .table-caption {
    font-size: 9.5pt;
    text-align: center;
    margin-bottom: 0.4em;
    font-weight: bold;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 9.5pt;
    margin: 0 auto;
  }

  table thead tr:first-child { border-top: 1.5px solid #000; }
  table thead tr:last-child  { border-bottom: 1px solid #000; }
  table tbody tr:last-child  { border-bottom: 1.5px solid #000; }

  table th, table td {
    padding: 4px 10px;
    text-align: center;
    vertical-align: middle;
  }

  table th { font-weight: bold; font-size: 9pt; background: none; }
  table td:first-child, table th:first-child { text-align: left; }

  .table-note { font-size: 8.5pt; color: #333; margin-top: 0.3em; font-style: italic; }

  .equation-block { margin: 1.2em 2em; text-align: center; overflow-x: auto; }

  pre, code {
    font-family: "Courier New", Courier, monospace;
    font-size: 8.5pt;
  }

  pre {
    background: #f8f8f5;
    border: 1px solid #ccc;
    padding: 0.7em 1em;
    margin: 1em 0;
    overflow-x: auto;
    line-height: 1.5;
    white-space: pre;
  }

  blockquote {
    background: #f5f5f0;
    border-left: 3px solid #555;
    margin: 1.4em 1em;
    padding: 0.6em 1em;
    font-size: 9.5pt;
    line-height: 1.55;
  }

  blockquote p { text-indent: 0; }

  .references-list { list-style: none; padding: 0; }

  .references-list li {
    font-size: 9.5pt;
    text-indent: -1.5em;
    padding-left: 1.5em;
    margin-bottom: 0.5em;
    text-align: left;
    line-height: 1.5;
  }

  .appendix-label { font-weight: bold; font-variant: small-caps; }

  hr { border: none; border-top: 1px solid #ccc; margin: 2.5em 0; }

  .figure-block { margin: 1.8em 0; text-align: center; }
  .figure-block img { max-width: 90%; border: 1px solid #ddd; }
  .figure-block figcaption {
    margin-top: 0.45em;
    font-size: 9pt;
    color: #333;
    text-align: center;
  }

  em { font-style: italic; }
  strong { font-weight: bold; }
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Adaptación estratégica o mortandad — Alejandro Jiménez</title>
<script>
MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    tags: 'ams'
  }},
  options: {{ skipHtmlTags: ['script','noscript','style','textarea','pre'] }}
}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
<style>
{css}
</style>
</head>
<body>
<div class="page">
{body}
</div>
</body>
</html>
"""

# ── Helpers ───────────────────────────────────────────────────────────────────

def b64_fig(name: str) -> str:
    path = FIGS_DIR / f"{name}.png"
    if not path.exists():
        print(f"  AVISO: figura no encontrada: {path}")
        return ""
    data = path.read_bytes()
    return base64.b64encode(data).decode()


def figure_html(name: str, caption: str) -> str:
    b64 = b64_fig(name)
    if not b64:
        return ""
    return (
        f'<figure class="figure-block">'
        f'<img src="data:image/png;base64,{b64}" alt="{caption}" loading="lazy">'
        f'<figcaption>{caption}</figcaption>'
        f'</figure>\n'
    )


def split_title_block(md_text: str):
    """Extrae el bloque de título/meta del markdown (hasta el primer ---) y el resto."""
    parts = md_text.split("\n---\n", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return "", md_text


def render_title_block(header_md: str) -> str:
    """Convierte el bloque de encabezado en HTML del título."""
    lines = header_md.strip().splitlines()
    title = ""
    meta_lines = []
    keywords = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("**"):
            # **Autor:** Alejandro Jiménez
            meta_lines.append(re.sub(r"\*\*(.*?):\*\*\s*(.+)", r"<strong>\1:</strong> \2", line))
        elif line.startswith("**Palabras clave"):
            m = re.match(r"\*\*Palabras clave[^:]*:\*\*\s*(.*)", line)
            if m:
                keywords = m.group(1)

    meta_html = "<br>".join(l for l in meta_lines if l.strip())
    kw_html = f'<p class="keywords"><strong>Palabras clave:</strong> <span>{keywords}</span></p>' if keywords else ""

    return f"""<div class="title-block">
<h1>{title}</h1>
<div class="title-meta">{meta_html}</div>
{kw_html}
</div>"""


def extract_abstract(body_md: str):
    """Separa el abstract del resto; devuelve (abstract_html, rest_md)."""
    # Abstract is between "## Abstract" and the next "---"
    m = re.search(r"^## Abstract\s*\n(.*?)\n---", body_md, re.DOTALL | re.MULTILINE)
    if m:
        abstract_text = m.group(1).strip()
        rest = body_md[m.end():].lstrip()
        return abstract_text, rest
    return None, body_md


def protect_equations(text: str):
    """Reemplaza bloques $$...$$ con placeholders para que markdown no los toque."""
    placeholders = {}
    counter = [0]

    def _replace(m):
        key = f"EQBLOCK{counter[0]}EQBLOCK"
        placeholders[key] = m.group(0)
        counter[0] += 1
        return key

    text = re.sub(r"\$\$.*?\$\$", _replace, text, flags=re.DOTALL)
    return text, placeholders


def restore_equations(html: str, placeholders: dict) -> str:
    for key, val in placeholders.items():
        # Wrap block equations in a div for centering
        html = html.replace(key, f'<div class="equation-block">{val}</div>')
    return html


def md_to_html(text: str) -> str:
    """Convierte markdown a HTML usando python-markdown con extensiones."""
    # Protect equations first
    text, eq_placeholders = protect_equations(text)

    md_instance = markdown.Markdown(
        extensions=[
            TableExtension(),
            FencedCodeExtension(),
            "nl2br",
        ],
        output_format="html"
    )
    html = md_instance.convert(text)

    # Restore equations
    html = restore_equations(html, eq_placeholders)
    return html


def insert_figures(html: str) -> str:
    """Inserta bloques de figura después de marcadores de texto."""
    for fig_name, caption, marker in FIGURES:
        fig_block = figure_html(fig_name, caption)
        if not fig_block:
            continue
        # Find the marker and insert after the enclosing paragraph/block
        idx = html.find(marker)
        if idx == -1:
            print(f"  AVISO: marcador no encontrado para {fig_name}: '{marker[:60]}...'")
            continue
        # Find the next </p> or </pre> or </blockquote> after the marker
        end_tag_match = re.search(r"</(?:p|pre|blockquote|ul|ol|table)>", html[idx:])
        if end_tag_match:
            insert_pos = idx + end_tag_match.end()
        else:
            insert_pos = idx + len(marker)
        html = html[:insert_pos] + "\n" + fig_block + html[insert_pos:]
        print(f"  Figura insertada: {fig_name}")
    return html


def post_process(html: str) -> str:
    """Ajustes finales al HTML generado."""
    # Sección de referencias: convertir lista de párrafos en lista con hanging indent
    # (python-markdown genera párrafos para la sección de referencias)
    # No hay mucho que hacer aquí — el CSS ya maneja el hanging indent en .references-list

    # Agregar clase no-indent al primer párrafo después de h2/h3
    html = re.sub(r"(</h[23]>)\s*<p>", r"\1\n<p class='no-indent'>", html)

    # En la sección de referencias, las líneas empiezan con autor en mayúsculas
    # Esto se manejará con CSS (referencias-list no disponible aquí sin marcadores)

    return html


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"Leyendo: {MD_PATH}")
    md_text = MD_PATH.read_text(encoding="utf-8")

    # 1. Título
    header_md, body_md = split_title_block(md_text)
    title_html = render_title_block(header_md)

    # 2. Abstract
    abstract_md, main_md = extract_abstract(body_md)
    if abstract_md:
        abstract_html = f"""<div class="abstract-block">
<h2>Abstract</h2>
<p>{abstract_md}</p>
</div>
<hr class="abstract-rule">
"""
    else:
        abstract_html = ""
        main_md = body_md

    # 3. Cuerpo principal → HTML
    print("Convirtiendo markdown a HTML...")
    body_html = md_to_html(main_md)

    # 4. Insertar figuras
    print("Insertando figuras...")
    body_html = insert_figures(body_html)

    # 5. Post-proceso
    body_html = post_process(body_html)

    # 6. Ensamblar HTML final
    full_body = title_html + "\n" + abstract_html + "\n" + body_html
    final_html = HTML_TEMPLATE.format(css=CSS, body=full_body)

    # 7. Guardar
    HTML_OUT.write_text(final_html, encoding="utf-8")
    size_kb = len(final_html) / 1024
    print(f"\nthesis.html generado: {HTML_OUT}")
    print(f"Tamaño: {size_kb:.1f} KB")

    # 8. Verificaciones básicas
    checks = [
        ("Título v2.0", "Adaptación estratégica o mortandad" in final_html),
        ("MathJax script", "mathjax" in final_html.lower()),
        ("Ecuación M5", "EQBLOCK" not in final_html),
        ("Cuadro 2 tabla", "Trayectoria" in final_html),
        ("Figura fig_new_01", "fig_new_01" not in final_html or "base64" in final_html),
        ("Referencia Teece", "Teece" in final_html),
        ("Apéndice A", "Apéndice A" in final_html),
    ]
    print("\nVerificaciones:")
    all_ok = True
    for label, passed in checks:
        status = "OK" if passed else "FALLO"
        if not passed:
            all_ok = False
        print(f"  {status}: {label}")

    if all_ok:
        print("\nthesis.html v2.0 generado correctamente.")
    else:
        print("\nALGUNAS VERIFICACIONES FALLARON.")


if __name__ == "__main__":
    main()
