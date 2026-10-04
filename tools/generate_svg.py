"""
Generates dark_mode.svg and light_mode.svg (the neofetch-style profile card).

Run this only when you want to change the card's TEXT or AVATAR:
    pip install pillow
    python tools/generate_svg.py

The stats (repos, stars, commits, followers, lines of code, uptime) are filled in
automatically every day by today.py through the GitHub Action, so you never edit those.
"""
import html
from pathlib import Path
from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- EDIT BELOW
USERNAME_LINE = "nikunj@procoder"
ROW_CHARS = 60  # total characters per row on the right column

TOP = [  # (key, value)
    ("OS", "Linux"),
    ("Uptime", None),  # filled by today.py
    ("Host", "B.Tech CSE, GGSIPU Delhi"),
    ("Kernel", "Solana + AI Agents Developer"),
    ("Location", "New Delhi, India"),
]
MIDDLE_1 = [
    ("Languages.Programming", "TypeScript, JavaScript, Python"),
    ("Languages.Computer", "HTML, CSS, JSON, YAML"),
]
MIDDLE_2 = [
    ("Focus.Chain", "Solana"),
    ("Focus.Agents", "LangGraph, Ollama, Multi-LLM"),
    ("Focus.Backend", "Node.js, Express, MongoDB"),
    ("Building", "ChainPulse, LoanMatters, Cyphud"),
]
CONTACT = [
    ("Email", "p03490978@gmail.com"),
    ("LinkedIn", "nikunjrustagi"),
    ("X", "zynloqdev"),
    ("Media", "FoundrSpeak"),
]
# ---------------------------------------------------------------- EDIT ABOVE

THEMES = {
    "dark": dict(bg="#0d0b1a", key="#14F195", val="#E9E4FF", cc="#4a3b78",
                 add="#3fb950", dele="#f85149", text="#E9E4FF", title="#9945FF"),
    "light": dict(bg="#f6f2ff", key="#7B2FF7", val="#2b2540", cc="#bdaee6",
                  add="#1a7f37", dele="#cf222e", text="#2b2540", title="#7B2FF7"),
}
LINE = "\u2500"  # box-drawing line for the section rules
ASCII_COLS, ASCII_ROWS = 38, 24
CHARS = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"


def esc(s):
    return html.escape(str(s), quote=False)


def row(key, value, tspan_ids=None):
    """'. Key:  .....  value' padded to ROW_CHARS."""
    dots = ROW_CHARS - 2 - len(key) - 1 - len(value) - 2
    dots = max(1, dots)
    ids = tspan_ids or {}
    d_id = f' id="{ids["dots"]}"' if "dots" in ids else ""
    v_id = f' id="{ids["val"]}"' if "val" in ids else ""
    key_html = ".".join(f'<tspan class="key">{esc(k)}</tspan>' for k in key.split("."))
    return (f'<tspan class="cc">. </tspan>{key_html}:'
            f'<tspan class="cc"{d_id}> {"." * dots} </tspan>'
            f'<tspan class="value"{v_id}>{esc(value)}</tspan>')


def rule(title):
    n = max(0, ROW_CHARS - len(title) - 5)
    return f' {LINE}{LINE * n}{LINE}{LINE}'


def build_right(theme):
    t = THEMES[theme]
    lines = []  # each item is (html_for_line, is_gap)

    def add(h):
        lines.append(h)

    def gap_dot():
        lines.append('<tspan class="cc">. </tspan>')

    add(f'<tspan fill="{t["title"]}">{esc(USERNAME_LINE)}</tspan><tspan class="cc">{rule(USERNAME_LINE)}</tspan>')
    for k, v in TOP:
        if k == "Uptime":
            add(row(k, "0 years, 0 months, 0 days", {"dots": "age_data_dots", "val": "age_data"}))
        else:
            add(row(k, v))
    gap_dot()
    for k, v in MIDDLE_1:
        add(row(k, v))
    gap_dot()
    for k, v in MIDDLE_2:
        add(row(k, v))
    lines.append(None)  # visual gap, no dot
    add(f'<tspan fill="{t["title"]}">- Contact</tspan><tspan class="cc">{rule("- Contact")}</tspan>')
    for k, v in CONTACT:
        add(row(k, v))

    # pad so the stats block always sits on the last 4 lines (rows 21..24)
    while len(lines) < 21:
        lines.append(None)
    assert len(lines) == 21, f"Too many rows ({len(lines)}); the card fits 21 before the stats block. Remove some."

    stats_title = "- GitHub Stats"
    lines.append(f'<tspan fill="{t["title"]}">{stats_title}</tspan><tspan class="cc">{rule(stats_title)}</tspan>')
    lines.append(
        '<tspan class="cc">. </tspan><tspan class="key">Repos</tspan>:<tspan class="cc" id="repo_data_dots"> .... </tspan>'
        '<tspan class="value" id="repo_data">0</tspan> {<tspan class="key">Contributed</tspan>: '
        '<tspan class="value" id="contrib_data">0</tspan>} | <tspan class="key">Stars</tspan>:'
        '<tspan class="cc" id="star_data_dots"> ........... </tspan><tspan class="value" id="star_data">0</tspan>')
    lines.append(
        '<tspan class="cc">. </tspan><tspan class="key">Commits</tspan>:<tspan class="cc" id="commit_data_dots"> ................ </tspan>'
        '<tspan class="value" id="commit_data">0</tspan> | <tspan class="key">Followers</tspan>:'
        '<tspan class="cc" id="follower_data_dots"> ....... </tspan><tspan class="value" id="follower_data">0</tspan>')
    lines.append(
        '<tspan class="cc">. </tspan><tspan class="key">Lines of Code on GitHub</tspan>:<tspan class="cc" id="loc_data_dots">. </tspan>'
        '<tspan class="value" id="loc_data">0</tspan> ( <tspan class="addColor" id="loc_add">0</tspan><tspan class="addColor">++</tspan>, '
        '<tspan id="loc_del_dots"> </tspan><tspan class="delColor" id="loc_del">0</tspan><tspan class="delColor">--</tspan> )')

    out = []
    for i, h in enumerate(lines):
        if h is None:
            continue
        y = 30 + 20 * i
        out.append(f'<tspan x="390" y="{y}">{h}</tspan>' if not h.startswith('<tspan x=') else h)
    return "\n".join(out)


def hex_(rgb):
    return "#%02x%02x%02x" % rgb


def build_ascii(theme):
    img = Image.open(ROOT / "assets" / "avatar.png").convert("RGB").crop((95, 40, 305, 300))
    if theme == "dark":
        # lift dark tones so hair and glasses stay visible on the dark card
        px = img.load()
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = px[x, y]
                f = lambda c: int((0.28 + 0.72 * ((c / 255) ** 0.5)) * 255)
                px[x, y] = (f(r), f(g), f(b))
        img = ImageEnhance.Color(img).enhance(1.4)
    else:
        img = ImageEnhance.Color(img).enhance(1.2)
        img = ImageEnhance.Brightness(img).enhance(0.85)
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = img.resize((ASCII_COLS, ASCII_ROWS), Image.LANCZOS)
    px = img.load()
    cx, cy = (ASCII_COLS - 1) / 2, (ASCII_ROWS - 1) / 2
    rows = []
    for gy in range(ASCII_ROWS):
        runs, cur_color, buf = [], None, ""
        for gx in range(ASCII_COLS):
            # elliptical mask: keep the avatar round like the original badge
            if ((gx - cx) / (ASCII_COLS / 2)) ** 2 + ((gy - cy) / (ASCII_ROWS / 2)) ** 2 > 1.0:
                ch, col = " ", None
            else:
                r, g, b = px[gx, gy]
                luma = 0.299 * r + 0.587 * g + 0.114 * b
                d = luma if theme == "dark" else 255 - luma
                ch = CHARS[int(d / 255 * (len(CHARS) - 1))]
                col = hex_((r, g, b))
            if col == cur_color:
                buf += esc(ch)
            else:
                if buf:
                    runs.append((cur_color, buf))
                cur_color, buf = col, esc(ch)
        if buf:
            runs.append((cur_color, buf))
        inner = "".join(f'<tspan fill="{c}">{b}</tspan>' if c else b for c, b in runs)
        rows.append(f'<tspan x="15" y="{30 + 20 * gy + 20}">{inner}</tspan>')
    return "\n".join(rows)


def build(theme):
    t = THEMES[theme]
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {t['key']};}}
.value {{fill: {t['val']};}}
.addColor {{fill: {t['add']};}}
.delColor {{fill: {t['dele']};}}
.cc {{fill: {t['cc']};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="985px" height="530px" fill="{t['bg']}" rx="15"/>
<text x="15" y="30" fill="{t['text']}" class="ascii">
{build_ascii(theme)}
</text>
<text x="390" y="30" fill="{t['text']}">
{build_right(theme)}
</text>
</svg>
"""


if __name__ == "__main__":
    for theme in ("dark", "light"):
        (ROOT / f"{theme}_mode.svg").write_text(build(theme), encoding="utf-8")
        print("wrote", f"{theme}_mode.svg")
