"""
add_toc.py
Añade un índice navegable (TOC) a output/thesis.html.
- Asigna id a cada <h2>/<h3> (excepto Abstract)
- Genera bloque <nav id="toc"> con links anclados
- Inserta CSS del TOC en el <style> existente
- Inserta el TOC justo después de <hr class="abstract-rule">
"""

import re
from pathlib import Path

HTML_PATH = Path(__file__).parent.parent / "output" / "thesis.html"

# ── Leer ──────────────────────────────────────────────────────────────────────
html = HTML_PATH.read_text(encoding="utf-8")

# ── 1. Generar ids para cada h2/h3 (excepto Abstract) ─────────────────────────
def make_id(text):
    """Convierte texto de heading a slug simple."""
    text = re.sub(r"<[^>]+>", "", text)          # quitar tags HTML internos
    text = text.strip()
    # Tomar los primeros caracteres útiles
    slug = re.sub(r"[^a-zA-Z0-9À-ÿ\s\-]", "", text)
    slug = slug.strip().lower()
    slug = re.sub(r"\s+", "-", slug)
    slug = slug[:60]
    return slug

heading_pattern = re.compile(r"(<h([23]))(>)(.*?)(</h\2>)", re.DOTALL)

id_map = []   # [(level, id, display_text)]

def assign_id(m):
    tag_open, level, gt, inner, tag_close = m.groups()
    display = re.sub(r"<[^>]+>", "", inner).strip()
    if display.lower() == "abstract":
        return m.group(0)
    slug = make_id(inner)
    id_map.append((int(level), slug, display))
    return f'{tag_open} id="{slug}"{gt}{inner}{tag_close}'

html = heading_pattern.sub(assign_id, html)

# ── 2. Construir HTML del TOC ──────────────────────────────────────────────────
def build_toc(entries):
    lines = ['<nav id="toc">', '<h2 class="toc-title">Índice</h2>', '<ol class="toc-list">']
    open_sub = False
    for level, slug, text in entries:
        # Eliminar el número de sección del texto para el índice (lo dejamos para claridad)
        if level == 2:
            if open_sub:
                lines.append("</ol></li>")
                open_sub = False
            lines.append(f'<li class="toc-h2"><a href="#{slug}">{text}</a>')
            lines.append('<ol class="toc-sub">')
            open_sub = True
        else:  # h3
            lines.append(f'<li class="toc-h3"><a href="#{slug}">{text}</a></li>')
    if open_sub:
        lines.append("</ol></li>")
    lines.append("</ol>")
    lines.append("</nav>")
    return "\n".join(lines)

toc_html = build_toc(id_map)

# ── 3. CSS del TOC ─────────────────────────────────────────────────────────────
toc_css = """
  /* ── Índice / Table of Contents ── */
  #toc {
    border: 1px solid #bbb;
    background: #fafaf7;
    padding: 1.2em 1.8em 1.4em 1.8em;
    margin: 2em 0 2.5em 0;
    font-size: 9.5pt;
    break-inside: avoid;
  }

  .toc-title {
    font-size: 10pt !important;
    font-weight: bold !important;
    font-variant: small-caps !important;
    letter-spacing: 0.12em !important;
    text-align: center !important;
    margin: 0 0 0.8em 0 !important;
    border-bottom: 1px solid #aaa;
    padding-bottom: 0.4em;
  }

  ol.toc-list {
    margin: 0;
    padding: 0;
    list-style: none;
    counter-reset: none;
  }

  .toc-list > li.toc-h2 {
    margin-top: 0.45em;
    font-weight: bold;
  }

  .toc-list > li.toc-h2 > a {
    font-weight: bold;
    color: #111;
    text-decoration: none;
  }

  .toc-list > li.toc-h2 > a:hover { text-decoration: underline; color: #333; }

  ol.toc-sub {
    list-style: none;
    margin: 0.1em 0 0 1.5em;
    padding: 0;
  }

  li.toc-h3 {
    margin: 0.15em 0;
    font-weight: normal;
  }

  li.toc-h3 a {
    color: #333;
    text-decoration: none;
  }

  li.toc-h3 a:hover { text-decoration: underline; color: #000; }

  @media print {
    #toc { border: 1px solid #999; background: none; }
    #toc a { color: #000; text-decoration: none; }
    #toc a::after { content: none; }
  }
"""

# ── 4. Insertar CSS antes de </style> ─────────────────────────────────────────
html = html.replace("</style>", toc_css + "\n</style>", 1)

# ── 5. Insertar TOC después de <hr class="abstract-rule"> ────────────────────
marker = '<hr class="abstract-rule">'
insert_after = marker + "\n"
html = html.replace(insert_after, insert_after + toc_html + "\n", 1)

# ── 6. Guardar ────────────────────────────────────────────────────────────────
HTML_PATH.write_text(html, encoding="utf-8")
size_kb = HTML_PATH.stat().st_size / 1024
print(f"Guardado: {HTML_PATH}  ({size_kb:.1f} KB)")
print(f"Entradas en el índice: {len(id_map)} ({sum(1 for l,_,_ in id_map if l==2)} secciones, {sum(1 for l,_,_ in id_map if l==3)} subsecciones)")
