#!/usr/bin/env python3
"""Generates banner.svg: night-alarm-clock style banner (Dhaka time + weather)."""
import json, urllib.request
from datetime import datetime, timedelta, timezone

DHAKA = timezone(timedelta(hours=6))
now = datetime.now(DHAKA)

# ---- weather (Open-Meteo, no API key). Falls back to placeholders ----
temp, hi, lo, rain = "--", "--", "--", "--"
try:
    url = ("https://api.open-meteo.com/v1/forecast?latitude=23.81&longitude=90.41"
           "&current=temperature_2m&daily=temperature_2m_max,temperature_2m_min,"
           "precipitation_probability_max&timezone=Asia%2FDhaka&forecast_days=1")
    d = json.load(urllib.request.urlopen(url, timeout=10))
    temp = round(d["current"]["temperature_2m"])
    hi = round(d["daily"]["temperature_2m_max"][0])
    lo = round(d["daily"]["temperature_2m_min"][0])
    rain = d["daily"]["precipitation_probability_max"][0]
except Exception:
    pass

# ---- 7-segment digits ----
SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc",
       "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg"}
W, H, T = 62, 112, 11

def digit(x, y, ch):
    hv = (H - 3 * T) / 2 - 4
    y_up, y_lo = y + T + 2, y + H / 2 + T / 2 + 2
    rects = {
        "a": (x + T + 2, y, W - 2 * T - 4, T),
        "g": (x + T + 2, y + H / 2 - T / 2, W - 2 * T - 4, T),
        "d": (x + T + 2, y + H - T, W - 2 * T - 4, T),
        "f": (x, y_up, T, hv), "b": (x + W - T, y_up, T, hv),
        "e": (x, y_lo, T, hv), "c": (x + W - T, y_lo, T, hv),
    }
    out = []
    for s, (rx, ry, rw, rh) in rects.items():
        on = s in SEG[ch]
        out.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" '
                   f'rx="4" class="{"on" if on else "off"}"/>')
    return "".join(out)

hh = now.strftime("%I").lstrip("0").rjust(2, "0")  # 12-hour
mm = now.strftime("%M")
ampm = now.strftime("%p")
digits = ""
xs = [330, 405, 520, 595]
for x, ch in zip(xs, hh + mm):
    digits += digit(x, 125, ch)

date_str = now.strftime("%A, %b %d, %Y")
upd = now.strftime("%H:%M")

cards = [
    ("🏥", "Digital Health", "OpenMRS+ &amp; health IT"),
    ("🌐", "Network &amp; Servers", "MikroTik · Cisco · Linux"),
    ("🛠️", "Automation", "Python · Flutter · PHP"),
    ("💡", "Always Learning", "Building &amp; improving"),
]
card_svg = ""
for i, (ic, t, s) in enumerate(cards):
    cx = 30 + i * 238
    card_svg += (f'<g transform="translate({cx},330)"><rect width="222" height="66" rx="12" class="card"/>'
                 f'<text x="16" y="28" font-size="18">{ic}</text>'
                 f'<text x="46" y="28" class="ct">{t}</text>'
                 f'<text x="46" y="50" class="cs">{s}</text></g>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 420" width="980" height="420">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#0b2147"/><stop offset="1" stop-color="#040a16"/></linearGradient>
<filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/>
<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
text{{font-family:'Segoe UI',Arial,sans-serif;fill:#fff}}
.on{{fill:#0aa5ff;filter:url(#glow)}} .off{{fill:#0aa5ff;opacity:.07}}
.title{{font-size:34px;font-weight:800}} .sub{{font-size:15px;fill:#9db4d6}}
.date{{font-size:24px;font-weight:700}} .big{{font-size:44px;font-weight:700}}
.mid{{font-size:26px;font-weight:700}} .small{{font-size:15px;fill:#9db4d6}}
.card{{fill:#0e1f3d;stroke:#1d3a6b}} .ct{{font-size:15px;font-weight:700}} .cs{{font-size:12.5px;fill:#9db4d6}}
.blink{{animation:b 2s steps(1) infinite}} @keyframes b{{50%{{opacity:.1}}}}
</style>
<rect width="980" height="420" rx="18" fill="url(#bg)"/>
<text x="490" y="46" text-anchor="middle" class="title">RATUL'S <tspan style="fill:#0aa5ff">DIGITAL</tspan> HUB</text>
<text x="490" y="70" text-anchor="middle" class="sub">ICT &amp; Digital Health · Network Engineer · Tech Enthusiast</text>
<text x="490" y="108" text-anchor="middle" class="date">{date_str}</text>

<text x="60" y="170" class="mid">Dhaka</text>
<text x="60" y="222" class="big">☁ {temp}°</text>
<text x="60" y="250" class="small">⟳ updated {upd}</text>

{digits}
<g class="blink"><rect x="492" y="160" width="12" height="12" rx="3" class="on"/>
<rect x="492" y="205" width="12" height="12" rx="3" class="on"/></g>
<text x="672" y="232" font-size="22" font-weight="700" style="fill:#0aa5ff">{ampm}</text>

<text x="790" y="165" class="mid">↑ {hi}°</text>
<text x="790" y="208" class="mid">↓ {lo}°</text>
<text x="790" y="251" class="mid">💧 {rain}%</text>

<text x="490" y="300" text-anchor="middle" class="sub">📍 Bangladesh 🇧🇩 · "Passionate about technology. Driven by innovation. Always learning."</text>
{card_svg}
</svg>'''

open("banner.svg", "w", encoding="utf-8").write(svg)
print("banner.svg written", hh, mm, ampm)
