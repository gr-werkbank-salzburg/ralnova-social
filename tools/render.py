"""Render Ralnova Connect post images (1080x1350 PNG) from a week plan.

Usage: python3 tools/render.py posts/plan/<week>.json
Each post in the plan: {"date","time","audience":"betriebe"|"handwerker","file",
  "headline","body","footer","cta","caption"}  (optional "kicker")
Only posts whose PNG does not exist yet are rendered.
Needs: pip install playwright && python3 -m playwright install chromium
"""
import html, json, os, sys
from string import Template
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
THEMES = {
    "betriebe": dict(bg="#1B1A18", fg="#F4EFE6", accent="#E8833A", muted="#B8B0A3",
                     body="#D9D2C6", rule="#3A3833", ctabg="#E8833A", ctafg="#1B1A18",
                     kicker="FÜR HANDWERKSBETRIEBE"),
    "handwerker": dict(bg="#F4EFE6", fg="#1B1A18", accent="#B85A16", muted="#5E584F",
                       body="#3D3933", rule="#D6CEC1", ctabg="#1B1A18", ctafg="#F4EFE6",
                       kicker="JOBS IM HANDWERK · SALZBURG"),
}

def hsize(text):
    n = len(text)
    return "104px" if n <= 55 else "92px" if n <= 70 else "80px" if n <= 90 else "70px"

def main(plan_path):
    plan = json.load(open(plan_path, encoding="utf-8"))
    tpl = Template(open(os.path.join(HERE, "template.html"), encoding="utf-8").read())
    todo = [p for p in plan["posts"] if not os.path.exists(os.path.join(ROOT, p["file"]))]
    if not todo:
        print("nothing to render"); return
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for p in todo:
            t = dict(THEMES[p["audience"]])
            t["kicker"] = p.get("kicker", t["kicker"])
            page = tpl.substitute(**{k: html.escape(v) if k == "kicker" else v for k, v in t.items()},
                                  hsize=hsize(p["headline"]),
                                  headline=html.escape(p["headline"]),
                                  body_text=html.escape(p["body"]),
                                  footer=html.escape(p["footer"]),
                                  cta=html.escape(p["cta"]))
            out = os.path.join(ROOT, p["file"])
            os.makedirs(os.path.dirname(out), exist_ok=True)
            pg.set_content(page, wait_until="load")
            pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            print("rendered", p["file"])
        b.close()

if __name__ == "__main__":
    main(sys.argv[1])
