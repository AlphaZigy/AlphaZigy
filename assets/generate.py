"""Generate the SVG cards and banners used by the profile README.

    python assets/generate.py

Edit the data below and re-run; every SVG in assets/ is rebuilt.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"

ACCENTS = {
    "ai":      ("#00D9FF", "#A78BFA"),
    "agri":    ("#34D399", "#00D9FF"),
    "fintech": ("#FBBF24", "#F472B6"),
    "culture": ("#A78BFA", "#F472B6"),
}

# (slug, emoji, title, category, accent, status, description, tech)
PROJECTS = [
    ("ubuntuintelligence", "🗣️", "UbuntuIntelligence", "AI · Research", "ai", "Open source",
     "Indigenous LLM ecosystem for Shona language learning and cultural heritage preservation, grounded by vector retrieval.",
     ["Django", "PostgreSQL", "pgvector", "Redis", "React"]),
    ("srlms", "🎓", "SRLMS", "AI · EdTech", "ai", "Open source",
     "AI-powered self-regulated learning for programming education: plan, act, monitor, reflect, with AI-assisted grading.",
     ["Django", "DRF", "JWT", "React"]),
    ("eduscheduler", "📅", "EduScheduler", "SaaS · EdTech", "ai", "Private",
     "Multi-tenant timetabling SaaS. A constraint solver builds clash-free weekly and exam timetables with PDF/Excel exports.",
     ["React", "TypeScript", "Django", "PostgreSQL"]),
    ("zou-assistant", "🤖", "ZOU Student Assistant", "AI · Support", "ai", "Private",
     "Support assistant for Zimbabwe Open University that cannot hallucinate: it only serves staff-approved answers.",
     ["Django", "NLP", "Knowledge base"]),
    ("paburiro", "📚", "Paburiro AI Tutor", "AI · EdTech", "ai", "Team project",
     "Web frontend for a national AI tutoring platform covering the curriculum, exams and ECD content.",
     ["React", "TypeScript", "shadcn/ui", "TanStack"]),
    ("procv-africa", "📄", "ProCV Africa", "SaaS · Careers", "ai", "Private",
     "ATS-friendly CV builder for African job seekers, with AI grammar fixes, content suggestions and premium templates.",
     ["React", "Django", "PWA", "AI"]),

    ("agridoctor", "🌿", "AgriDoctor 2.0", "AI · AgriTech", "agri", "Open source",
     "Snap a leaf, get a diagnosis. On-device plant disease detection with treatment plans, in several languages.",
     ["React Native", "Expo", "TensorFlow.js"]),
    ("solcure", "☀️", "SolCure", "IoT · AgriTech", "agri", "Open source",
     "Smart solar-powered tobacco curing. Real-time monitoring and control of barn temperature, humidity and airflow.",
     ["React Native", "Expo", "IoT"]),
    ("ecocampus", "♻️", "EcoCampus AI", "IoT · Sustainability", "agri", "Private",
     "Sustainability OS for universities: ESP32 telemetry, ML forecasts, anomaly detection and carbon accounting.",
     ["React 19", "Django", "scikit-learn", "ESP32"]),
    ("mymushroom", "🍄", "MyMushroom", "IoT · AgriTech", "agri", "Private",
     "IoT mushroom-farm controller with live temperature, humidity and CO2 gauges, remote actuators and alerts.",
     ["Expo", "Django", "Arduino"]),
    ("agie", "🚜", "Agie", "Mobile · AgriTech", "agri", "Private",
     "Agribusiness super-app: weather, ecological regions, agronomists, contract farming, marketplace and forum.",
     ["React Native", "Expo", "Django"]),

    ("tengesa", "🧾", "Tengesa POS", "FinTech · Retail", "fintech", "Private",
     "Offline-first point of sale for Zimbabwean retail, with signed offline licences and EcoCash / OneMoney billing.",
     ["Expo", "SQLite", "Django", "Paynow"]),
    ("logigo", "🚚", "LogiGo", "Logistics · Marketplace", "fintech", "Private",
     "Smart courier marketplace connecting buyers, sellers and drivers, with live WebSocket tracking.",
     ["Expo", "Channels", "PostGIS", "Celery"]),
    ("mvurawaterhub", "💧", "MvuraWaterHub", "Marketplace · Services", "fintech", "Private",
     "Water-services marketplace: requests, contractor quotes, bookings, payments and reviews across app, admin and web.",
     ["Expo", "React", "Django"]),

    ("aogzim", "⛪", "Mashava Ultra-REG", "Platform · Events", "culture", "Open source",
     "Church-wide event registration and logistics platform: registrations, payments, messaging and audit trail.",
     ["Django", "DRF", "React", "MySQL"]),
    ("aog-hymns", "🎵", "AOG Hymnal", "Mobile · Culture", "culture", "Open source",
     "Offline hymnal with 168 hymns in isiZulu, chiShona and English, full-text search, readable in low light.",
     ["React Native", "Expo", "SQLite FTS5"]),
    ("zimheritagexr", "🏺", "ZimHeritageXR", "XR · Tourism", "culture", "Private",
     "WebXR heritage explorer with guided tours of Great Zimbabwe, Victoria Falls, Matobo Hills and Chinhoyi Caves.",
     ["React", "Three.js", "WebXR"]),
    ("eventive", "🎟️", "Eventive", "SaaS · Events", "culture", "Live",
     "Event planning platform with pitch decks, sponsorship proposals, in-browser PDF/DOCX/PPTX export and OTP 2FA.",
     ["TanStack Start", "Django"]),
]

SECTIONS = [
    ("about", "About Me", "who I am and what drives me", "ai"),
    ("stack", "Tech Stack", "the tools I ship production systems with", "ai"),
    ("work", "Featured Work", "selected products, platforms and research", "ai"),
    ("principles", "How I Build", "the engineering principles behind my work", "culture"),
    ("analytics", "GitHub Analytics", "live numbers, updated automatically", "ai"),
    ("connect", "Let's Connect", "open to roles, contracts and collaborations", "culture"),
    ("cat-ai", "AI & Education", "", "ai"),
    ("cat-agri", "AgriTech, IoT & Sustainability", "", "agri"),
    ("cat-fintech", "FinTech, Commerce & Logistics", "", "fintech"),
    ("cat-culture", "Community, Culture & Events", "", "culture"),
]

HIGHLIGHTS = [
    ("30+", "Projects built", "ai"),
    ("6", "Industries served", "agri"),
    ("4", "Web · Mobile · IoT · AI", "fintech"),
    ("1", "Company founded", "culture"),
]


def text_width(s, size):
    # Rough average glyph width for Segoe UI; good enough for layout.
    return sum(size * (0.33 if c in "il.,:;|!'" else 0.62 if c.isupper() else 0.49) for c in s)


def wrap(s, size, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if text_width(trial, size) > max_w and cur:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    return lines + [cur] if cur else lines


def gradient(id_, a, b, animated=False):
    anim = ""
    if animated:
        anim = ('<animateTransform attributeName="gradientTransform" type="rotate" '
                'from="0 .5 .5" to="360 .5 .5" dur="8s" repeatCount="indefinite"/>')
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/>{anim}'
            f'</linearGradient>')


def project_card(slug, emoji, title, category, accent, status, desc, tech):
    a, b = ACCENTS[accent]
    W, H, P = 440, 236, 24
    desc_lines = wrap(desc, 13.5, W - 2 * P)[:3]

    chips, x, y = [], P, H - P - 24
    for t in tech:
        w = text_width(t, 11.5) + 22
        if x + w > W - P:
            break
        chips.append(
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="24" rx="12" fill="#161B22" stroke="#30363D"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 16}" text-anchor="middle" class="chip">{escape(t)}</text>')
        x += w + 8

    sw = text_width(status, 10.5) * 1.25 + 22
    desc_svg = "".join(
        f'<text x="{P}" y="{118 + i * 21}" class="desc">{escape(l)}</text>' for i, l in enumerate(desc_lines))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">
<title>{escape(title)} — {escape(desc)}</title>
<defs>
{gradient("bg", "#0D1117", "#141B26")}
{gradient("acc", a, b, animated=True)}
{gradient("acc2", a, b)}
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{a}" stop-opacity=".35"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
<clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>
<style>
.title{{font:700 21px {FONT};fill:#F0F6FC}}
.cat{{font:600 10.5px {FONT};fill:{a};letter-spacing:1.6px}}
.desc{{font:400 13.5px {FONT};fill:#9DA7B3}}
.chip{{font:600 11.5px {FONT};fill:#C9D1D9}}
.status{{font:700 10.5px {FONT};fill:{a};letter-spacing:.6px}}
.glow{{animation:pulse 4s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
.shine{{animation:sweep 6s ease-in-out infinite}}
@keyframes sweep{{0%{{transform:translateX(-160px)}}60%,100%{{transform:translateX({W + 160}px)}}}}
</style>
</defs>
<g clip-path="url(#clip)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle class="glow" cx="{W - 40}" cy="30" r="130" fill="url(#glow)"/>
<rect class="shine" x="0" y="0" width="90" height="{H}" fill="#FFFFFF" opacity=".035" transform="skewX(-20)"/>
<rect width="{W}" height="3" fill="url(#acc2)"/>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="17.5" fill="none" stroke="url(#acc)" stroke-opacity=".55" stroke-width="1.5"/>
<rect x="{P}" y="{P}" width="52" height="52" rx="14" fill="{a}" fill-opacity=".12" stroke="{a}" stroke-opacity=".35"/>
<text x="{P + 26}" y="{P + 35}" text-anchor="middle" font-size="26">{emoji}</text>
<text x="{P + 68}" y="{P + 20}" class="cat">{escape(category.upper())}</text>
<text x="{P + 68}" y="{P + 45}" class="title">{escape(title)}</text>
<rect x="{W - P - sw:.1f}" y="{P}" width="{sw:.1f}" height="22" rx="11" fill="{a}" fill-opacity=".1" stroke="{a}" stroke-opacity=".4"/>
<text x="{W - P - sw / 2:.1f}" y="{P + 15}" text-anchor="middle" class="status">{escape(status.upper())}</text>
{desc_svg}
{"".join(chips)}
</svg>
'''
    (OUT / "projects" / f"{slug}.svg").write_text(svg, encoding="utf-8")


def section_banner(slug, title, subtitle, accent):
    a, b = ACCENTS[accent]
    small = slug.startswith("cat-")
    W, H = 880, (44 if small else 78)
    size = 20 if small else 30
    tw = text_width(title, size) * 1.08
    y_title = 29 if small else 38
    sub = "" if small else f'<text x="22" y="64" class="sub">{escape(subtitle)}</text>'
    line_x = 22 + tw + 18
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<defs>
{gradient("t", a, b)}
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{b}" stop-opacity=".7"/><stop offset="1" stop-color="{b}" stop-opacity="0"/></linearGradient>
<style>
.h{{font:800 {size}px {FONT};fill:url(#t)}}
.sub{{font:500 13.5px {FONT};fill:#8B949E;letter-spacing:.4px}}
.bar{{animation:grow 2.4s ease-in-out infinite alternate;transform-origin:0 50%}}
@keyframes grow{{from{{transform:scaleY(.55)}}to{{transform:scaleY(1)}}}}
</style>
</defs>
<rect class="bar" x="4" y="{8 if small else 10}" width="5" height="{H - (16 if small else 20)}" rx="2.5" fill="url(#t)"/>
<text x="22" y="{y_title}" class="h">{escape(title)}</text>
<rect x="{line_x:.1f}" y="{y_title - size * 0.33:.1f}" width="{W - line_x - 4:.1f}" height="1.5" fill="url(#fade)"/>
{sub}
</svg>
'''
    (OUT / "sections" / f"{slug}.svg").write_text(svg, encoding="utf-8")


def highlights():
    W, H, gap = 880, 112, 16
    tile = (W - gap * 3) / 4
    tiles = []
    for i, (num, label, accent) in enumerate(HIGHLIGHTS):
        a, b = ACCENTS[accent]
        x = i * (tile + gap)
        lines = wrap(label, 12.5, tile - 28)[:2]
        label_svg = "".join(
            f'<text x="{x + tile / 2:.1f}" y="{80 + j * 16}" text-anchor="middle" class="lbl">{escape(l)}</text>'
            for j, l in enumerate(lines))
        tiles.append(f'''<defs>{gradient(f"g{i}", a, b)}</defs>
<g class="tile" style="animation-delay:{i * .25}s">
<rect x="{x + .75:.1f}" y=".75" width="{tile - 1.5:.1f}" height="{H - 1.5}" rx="16" fill="#0D1117" stroke="url(#g{i})" stroke-opacity=".6" stroke-width="1.5"/>
<text x="{x + tile / 2:.1f}" y="{55 if len(lines) > 1 else 60}" text-anchor="middle" class="num" fill="url(#g{i})">{escape(num)}</text>
{label_svg}
</g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Highlights">
<title>30+ projects · 6 industries · 4 platforms · founder of Dubzig</title>
<style>
.num{{font:800 36px {FONT}}}
.lbl{{font:600 12.5px {FONT};fill:#9DA7B3}}
.tile{{animation:rise 3s ease-in-out infinite alternate}}
@keyframes rise{{from{{transform:translateY(2px)}}to{{transform:translateY(-2px)}}}}
</style>
{"".join(tiles)}
</svg>
'''
    (OUT / "highlights.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    (OUT / "projects").mkdir(exist_ok=True)
    (OUT / "sections").mkdir(exist_ok=True)
    for p in PROJECTS:
        project_card(*p)
    for s in SECTIONS:
        section_banner(*s)
    highlights()
    print(f"Wrote {len(PROJECTS)} cards, {len(SECTIONS)} banners and highlights.svg to {OUT}")
