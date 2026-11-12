#!/usr/bin/env python3
"""Build the bilingual home page (EN at /, PT at /pt/) from the YAML files in data/.

Usage:  python build.py            -> writes the site to _site/
Needs:  pip install pyyaml jinja2
"""
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, pass_context

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "_site"
DATA = ROOT / "data"
LANGS = ("en", "pt")


def load(name):
    with open(DATA / f"{name}.yml", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def check_bilingual(items, fields, where, errors):
    for i, item in enumerate(items, 1):
        for field in fields:
            value = item.get(field)
            if not isinstance(value, dict) or not all(str(value.get(l, "")).strip() for l in LANGS):
                errors.append(f"{where} #{i}: '{field}' needs both 'en' and 'pt' text")


def validate(d):
    errors = []
    course_ids = {c["id"] for c in d["courses"]}
    line_ids = {l["id"] for l in d["lines"]}
    types = set(d["site"]["t"]["type"])
    areas = set(d["site"]["t"]["area"])
    maturities = set(d["site"]["t"]["maturity"])

    check_bilingual(d["resources"], ("title", "description"), "resources.yml", errors)
    for i, r in enumerate(d["resources"], 1):
        if r.get("type") not in types:
            errors.append(f"resources.yml #{i}: type must be one of {sorted(types)}")
        if r.get("area") not in areas:
            errors.append(f"resources.yml #{i}: area must be one of {sorted(areas)}")
        if not r.get("url"):
            errors.append(f"resources.yml #{i}: url is required")
        for c in r.get("courses", []) or []:
            if c not in course_ids:
                errors.append(f"resources.yml #{i}: unknown course id '{c}' (see courses.yml)")

    check_bilingual(d["artifacts"], ("title", "description"), "artifacts.yml", errors)
    for i, a in enumerate(d["artifacts"], 1):
        if a.get("type") not in types:
            errors.append(f"artifacts.yml #{i}: type must be one of {sorted(types)}")
        if str(a.get("line")) not in line_ids:
            errors.append(f"artifacts.yml #{i}: line must be one of {sorted(line_ids)}")
        if a.get("maturity") not in maturities:
            errors.append(f"artifacts.yml #{i}: maturity must be one of {sorted(maturities)}")
        if not a.get("url"):
            errors.append(f"artifacts.yml #{i}: url is required")

    check_bilingual(d["lines"], ("title", "text"), "lines.yml", errors)
    check_bilingual(d["news"], ("title",), "news.yml", errors)
    check_bilingual(d["team"], ("role",), "team.yml", errors)
    check_bilingual(d["partners"], ("text",), "partners.yml", errors)
    check_bilingual(d["courses"], ("title",), "courses.yml", errors)
    return errors


def initials(name):
    parts = [p for p in name.split() if p[0].isupper()]
    return (parts[0][0] + parts[-1][0]) if len(parts) > 1 else name[:2].upper()


def main():
    d = {n: load(n) for n in ("site", "lines", "resources", "artifacts", "courses",
                               "publications", "news", "team", "partners")}
    errors = validate(d)
    if errors:
        print("Data errors:\n  - " + "\n  - ".join(errors), file=sys.stderr)
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True,
                      trim_blocks=True, lstrip_blocks=True)

    @pass_context
    def L(ctx, value):
        """Pick the current language from an {en, pt} mapping; pass plain values through."""
        if isinstance(value, dict):
            return value.get(ctx["lang"], "")
        return value

    env.filters["L"] = L
    env.filters["initials"] = initials
    env.filters["fmtdate"] = lambda v: v.strftime("%d.%m.%Y") if hasattr(v, "strftime") else str(v)

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "static", OUT / "static")
    (OUT / ".nojekyll").write_text("")

    courses = {c["id"]: c for c in d["courses"]}
    lines = {l["id"]: l for l in d["lines"]}
    tpl = env.get_template("index.html.j2")
    for lang in LANGS:
        path = next(l["path"] for l in d["site"]["languages"] if l["code"] == lang)
        html = tpl.render(lang=lang, path=path, courses_by_id=courses, lines_by_id=lines,
                          build_date=date.today(), **d)
        target = OUT / path.strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    base = d["site"]["base_url"].rstrip("/")
    urls = "".join(
        f"  <url><loc>{base}{l['path']}</loc><lastmod>{date.today()}</lastmod></url>\n"
        for l in d["site"]["languages"])
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n",
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
    print(f"Built {OUT} ({len(d['resources'])} resources, {len(d['artifacts'])} artefacts)")


if __name__ == "__main__":
    main()
