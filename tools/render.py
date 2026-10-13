"""Render Ralnova Connect post images (1080x1350 PNG) from a week plan.

Usage: python3 tools/render.py posts/plan/<week>.json
Each post: {"date","time","audience":"betriebe"|"handwerker","layout","palette","file",
            "headline","body","footer","cta","caption"}  (optional "kicker")
Layouts: klassik, block, zitat, liste, frage, rahmen  (tools/layouts/<name>.html)
  liste: "body" = one point per line (3-5 lines, no numbers - they are added).
Palettes: see PALETTES below; betriebe use b-*, handwerker use h-*.
Only posts whose PNG does not exist yet are rendered.
Needs: pip install playwright && python3 -m playwright install chromium
"""
import html, json, os, sys
from string import Template
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PALETTES = {
    # Betriebe (Inhaber) - dunkle, ruhige Grundtöne
    "b-kohle": dict(bg="#1B1A18", fg="#F4EFE6", accent="#E8833A", onaccent="#1B1A18", muted="#B8B0A3",
                    body="#D9D2C6", rule="#3A3833", ctabg="#E8833A", ctafg="#1B1A18"),
    "b-nacht": dict(bg="#14213D", fg="#F5F3EE", accent="#F2B33D", onaccent="#14213D", muted="#A9B3C7",
                    body="#D6DBE5", rule="#2C3A5A", ctabg="#F2B33D", ctafg="#14213D"),
    "b-wald":  dict(bg="#23302A", fg="#F1EEE4", accent="#D9C27E", onaccent="#23302A", muted="#A8B3A9",
                    body="#D4D8CF", rule="#3A4A42", ctabg="#D9C27E", ctafg="#23302A"),
    # Handwerker (Bewerber) - helle Grundtöne
    "h-creme":  dict(bg="#F4EFE6", fg="#1B1A18", accent="#B85A16", onaccent="#FFFFFF", muted="#5E584F",
                     body="#3D3933", rule="#D6CEC1", ctabg="#1B1A18", ctafg="#F4EFE6"),
    "h-signal": dict(bg="#F5F5F2", fg="#111111", accent="#1F5FA8", onaccent="#FFFFFF", muted="#555555",
                     body="#333333", rule="#DDDDDD", ctabg="#1F5FA8", ctafg="#FFFFFF"),
    "h-sand":   dict(bg="#EDE3D1", fg="#2A2118", accent="#7A4E2D", onaccent="#F7F0E3", muted="#6B5A48",
                     body="#3E3226", rule="#D3C4A8", ctabg="#2A2118", ctafg="#EDE3D1"),
}
DEFAULT_PALETTE = {"betriebe": "b-kohle", "handwerker": "h-creme"}
KICKER = {"betriebe": "FÜR HANDWERKSBETRIEBE", "handwerker": "JOBS IM HANDWERK · SALZBURG"}

def hsize(text, layout):
    n = len(text)
    big = layout in ("frage", "block")
    if n <= 40: return "112px" if big else "104px"
    if n <= 55: return "100px" if big else "96px"
    if n <= 70: return "88px"
    if n <= 90: return "76px"
    return "66px"

def hsize_small(text):
    return "76px" if len(text) <= 45 else "64px"

def items_html(body):
    lines = [l.strip(" –-•\t") for l in body.split("\n") if l.strip()]
    return "".join(f'<div class="item"><div class="num">{i}</div><div class="txt">{html.escape(l)}</div></div>'
                   for i, l in enumerate(lines, 1))

def page_for(p):
    layout = p.get("layout", "klassik")
    pal = dict(PALETTES[p.get("palette") or DEFAULT_PALETTE[p["audience"]]])
    tpl = Template(open(os.path.join(HERE, "layouts", layout + ".html"), encoding="utf-8").read())
    return tpl.substitute(**pal,
                          kicker=html.escape(p.get("kicker", KICKER[p["audience"]])),
                          hsize=hsize(p["headline"], layout),
                          hsize_small=hsize_small(p["headline"]),
                          headline=html.escape(p["headline"]),
                          body_text=html.escape(p["body"]),
                          items=items_html(p["body"]),
                          footer=html.escape(p["footer"]),
                          cta=html.escape(p["cta"]))

def main(plan_path):
    plan = json.load(open(plan_path, encoding="utf-8"))
    todo = [p for p in plan["posts"] if not os.path.exists(os.path.join(ROOT, p["file"]))]
    if not todo:
        print("nothing to render"); return
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for p in todo:
            out = os.path.join(ROOT, p["file"])
            os.makedirs(os.path.dirname(out), exist_ok=True)
            pg.set_content(page_for(p), wait_until="load")
            overflow = pg.evaluate("document.documentElement.scrollHeight > 1350 || document.documentElement.scrollWidth > 1080")
            pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            print("rendered", p["file"], "OVERFLOW - Text kürzen!" if overflow else "")
        b.close()

if __name__ == "__main__":
    main(sys.argv[1])
