import json, os, sys
BASE = "https://extezzu.github.io/webtools/"
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
NAV = [("security-headers-generator/", "Security headers"), ("sitemap-validator/", "Sitemap validator"),
       ("robots-txt-tester/", "robots.txt tester"), ("guides/export-app-store-reviews/", "App Store reviews")]

def page(path, title, desc, body, schema=None, lang="en", brand="SiteCheck Tools", nav_items=None, footer=None):
    depth = path.count("/")
    rel = "../" * depth
    home = "vypyska/" if lang == "uk" else ""
    nav = "".join(f'<a href="{rel}{h}">{t}</a>' for h, t in (nav_items or NAV))
    foot = footer or 'Free, private tools: everything runs in your browser, nothing is uploaded. Need it for thousands of sites or on a schedule? See our cloud versions on <a href="https://apify.com/extezzu">Apify</a>. Source: <a href="https://github.com/extezzu/webtools">GitHub</a>.'
    sd = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    html = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<link rel="stylesheet" href="{rel}style.css">{sd}</head><body>
<header><a href="{rel}{home}">{brand}</a><nav>{nav}</nav></header><main>{body}</main>
<footer>{foot}</footer>
</body></html>"""
    p = os.path.join(OUT, path, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(html)
    return path

def tool_schema(name, desc, path):
    return {"@context": "https://schema.org", "@type": "WebApplication", "name": name, "description": desc,
            "url": BASE + path, "applicationCategory": "DeveloperApplication", "operatingSystem": "Any",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}

pages = []
for mod in sorted(os.listdir(os.path.join(os.path.dirname(__file__), "pages"))):
    ns = {}
    exec(open(os.path.join(os.path.dirname(__file__), "pages", mod)).read(), ns)
    for d in ns["PAGES"]:
        schema = d.get("schema") or (tool_schema(d["name"], d["desc"], d["path"]) if d.get("tool") else None)
        pages.append(page(d["path"], d["title"], d["desc"], d["body"], schema, **d.get("layout", {})))
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for p in pages: f.write(f"  <url><loc>{BASE}{p}</loc><lastmod>2026-11-22</lastmod></url>\n")
    f.write("</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
print(len(pages), "pages")
