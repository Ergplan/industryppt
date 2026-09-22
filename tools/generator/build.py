import math, html
import scenes, hp101
from iso import C

E = html.escape

CSS = r"""

:root{--bg:#090a0b;--panel:#0f1214;--line:#1e2327;--line2:#2c3237;--ink:#eef0f1;--body:#c3c9cd;--mute:#8b949a;--dim:#5d666c;
--green:#3dd68c;--heat:#f2994a;--data:#5b8def;--esg:#c9a43a;--red:#e0604a;--gold:#b8962e;
--sans:"Inter Tight","Helvetica Neue",Helvetica,Arial,sans-serif;--mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);color-scheme:dark}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#090a0b}}
:root[data-theme="dark"]{--bg:#090a0b}
*,*:before,*:after{box-sizing:inherit}
html{scroll-padding-top:calc(env(safe-area-inset-top,0px) + 56px);-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.5;
background-image:linear-gradient(90deg,rgba(255,255,255,.028) 1px,transparent 1px);background-size:136px 100%;background-position:center top}
svg{display:block;width:100%;height:auto;max-width:100%}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:rgba(9,10,11,.88);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar-in{max-width:880px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px clamp(18px,5vw,40px)}
.logo{font-family:var(--sans);font-size:20px;letter-spacing:-.01em;font-weight:400;white-space:nowrap}
.logo .j{color:var(--gold)}.logo .w{color:var(--ink)}
.bar-r{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;color:var(--mute);text-transform:uppercase;text-align:right}
.bar-r b{color:var(--green);font-weight:500}
.prog{position:absolute;left:0;bottom:-1px;height:1px;background:var(--green);width:0}
.pg{max-width:880px;margin:0 auto;padding:44px clamp(20px,5.5vw,48px) 36px;border-bottom:1px solid var(--line);position:relative}
.hd{display:flex;justify-content:space-between;gap:16px;font-family:var(--mono);font-size:10.5px;letter-spacing:.26em;color:var(--dim);text-transform:uppercase;border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:36px}
.hd span:last-child{text-align:right}
.eb{font-family:var(--mono);font-size:11.5px;letter-spacing:.28em;color:var(--green);text-transform:uppercase;margin:0 0 18px}
.eb i{font-style:normal;color:var(--mute)}
h1,h2{font-family:var(--sans);font-weight:800;text-transform:uppercase;margin:0;letter-spacing:-.025em}
h1{font-size:clamp(46px,11.5vw,100px);line-height:.9}
h2{font-size:clamp(36px,8.6vw,68px);line-height:.93}
h1 .g,h2 .g{color:var(--green)} h2 .h{color:var(--heat)}
.sub{font-size:clamp(26px,6vw,44px);font-weight:800;text-transform:uppercase;letter-spacing:-.02em;line-height:1;margin:14px 0 0}
.lede{color:var(--body);font-size:clamp(16px,2.3vw,19px);max-width:62ch;margin:22px 0 0}
.mono{font-family:var(--mono)}
.lab{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute)}
.fig{margin:30px 0 0}.swipe{display:none;font-family:var(--mono);font-size:10px;letter-spacing:.22em;color:var(--dim);text-transform:uppercase;margin-top:8px}
.panel{border:1px solid var(--line2);background:var(--panel)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:34px 0 0}
.stat b{display:block;font-family:var(--mono);font-weight:400;font-size:clamp(28px,5.6vw,40px);color:var(--green);line-height:1.1}
.stat span{display:block;margin-top:6px}
.ft{display:flex;justify-content:space-between;gap:16px;font-family:var(--mono);font-size:10px;letter-spacing:.24em;color:var(--dim);text-transform:uppercase;border-top:1px solid var(--line);padding-top:14px;margin-top:40px}
.rows{margin:28px 0 0;border-top:1px solid var(--line2)}
.row{display:grid;grid-template-columns:170px 1fr;gap:18px;padding:16px 0;border-bottom:1px solid var(--line)}
.row .lab{padding-top:4px}
.row p{margin:0;color:var(--body)} .row p b{color:var(--ink);font-weight:600}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:28px 0 0}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:28px 0 0}
.card{border:1px solid var(--line2);background:var(--panel);padding:20px}
.card h3{font-size:16px;letter-spacing:.02em;text-transform:uppercase;margin:12px 0 6px;font-weight:700}
.card p{margin:0;color:var(--body);font-size:15px}
.ico{width:22px;height:22px;stroke:var(--green);fill:none;stroke-width:1.5}
.legend{display:flex;flex-wrap:wrap;gap:8px 20px;margin:18px 0 0}
.legend span{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--mute)}
.sw{width:10px;height:10px;display:inline-block}
.pts{display:grid;grid-template-columns:1fr 1fr;gap:0 26px;margin:22px 0 0}
.pt{display:grid;grid-template-columns:40px 1fr;gap:10px;padding:14px 0;border-bottom:1px solid var(--line)}
.num{width:30px;height:30px;border-radius:50%;border:1.5px solid currentColor;display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:11.5px;font-weight:600}
.pt h4{margin:3px 0 3px;font-size:15px;font-weight:700}
.pt p{margin:0;color:var(--mute);font-size:14px;line-height:1.45}
.pt .tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;margin-top:6px;display:block}
.c-power{color:var(--green)}.c-heat{color:var(--heat)}.c-data{color:var(--data)}.c-esg{color:var(--esg)}
.seq{margin:26px 0 0;border-top:1px solid var(--line2)}
.st{display:grid;grid-template-columns:64px 1fr;gap:14px;padding:18px 0;border-bottom:1px solid var(--line)}
.st .n{font-family:var(--mono);color:var(--green);font-size:12px;letter-spacing:.2em;padding-top:4px}
.st h4{margin:0 0 4px;font-size:17px;text-transform:uppercase;letter-spacing:.01em}
.st p{margin:0;color:var(--body);font-size:15px}
.st .out{font-family:var(--mono);font-size:10px;letter-spacing:.22em;color:var(--esg);text-transform:uppercase;margin-top:8px}
.chk{list-style:none;padding:0;margin:14px 0 0;columns:2;column-gap:28px}
.chk li{break-inside:avoid;padding:8px 0 8px 22px;border-bottom:1px solid var(--line);position:relative;color:var(--body);font-size:14.5px}
.chk li:before{content:"";position:absolute;left:2px;top:14px;width:8px;height:8px;border:1.2px solid var(--green)}
.ladder{margin:26px 0 0}
.lrow{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1.4fr);gap:14px;align-items:center;padding:11px 0;border-bottom:1px solid var(--line)}
.lrow .nm{font-size:14.5px}.lrow .nm small{display:block;color:var(--mute);font-size:12.5px}
.track{position:relative;height:20px;background:repeating-linear-gradient(90deg,transparent 0 calc(12.5% - 1px),#1c2125 calc(12.5% - 1px) 12.5%)}
.track .rg{position:absolute;top:5px;height:10px}
.track .cap{position:absolute;top:-4px;bottom:-4px;width:0;border-left:1.5px dashed var(--heat)}
.scale{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1.4fr);gap:14px;margin-top:8px}
.scale div:last-child{position:relative;height:14px;font-family:var(--mono);font-size:10px;color:var(--dim)}.scale div:last-child span{position:absolute;transform:translateX(-50%);white-space:nowrap}.scale div:last-child span:first-child{transform:none}.scale div:last-child span:last-child{transform:translateX(-100%)}
.econ{margin:26px 0 0}
.erow{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.6fr) 88px;gap:12px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line)}
.erow .nm{font-size:14.5px}.erow .nm small{display:block;color:var(--mute);font-size:12px}
.ebar{height:12px;position:relative}.ebar i{position:absolute;left:0;top:0;bottom:0}
.erow .v{font-family:var(--mono);font-size:14px;text-align:right}
.ehead{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.6fr) 88px;gap:12px;padding-bottom:8px;border-bottom:1px solid var(--line2)}
.note{color:var(--dim);font-size:12.5px;line-height:1.5;margin:14px 0 0}
.callout{border:1px solid var(--line2);border-left:3px solid var(--green);background:var(--panel);padding:18px 20px;margin:26px 0 0;color:var(--body);font-size:15.5px}
.callout b{color:var(--ink)}
.cock{margin:26px 0 0;border:1px solid var(--line2);background:#0c0f11}
.cock-h{display:flex;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--line2);font-family:var(--mono);font-size:10px;letter-spacing:.2em;color:var(--mute);text-transform:uppercase}
.cock-h b{color:var(--green);font-weight:500}
.tiles{display:grid;grid-template-columns:repeat(3,1fr)}
.tile{padding:14px 16px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.tile:nth-child(3n){border-right:0}
.tile b{display:block;font-family:var(--mono);font-weight:400;font-size:clamp(20px,4.2vw,28px);margin-top:6px}
.tile small{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase}
.ops{padding:10px 16px 14px}
.op{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px;color:var(--body)}
.op:last-child{border-bottom:0}
.op i{font-style:normal;font-family:var(--mono);width:14px;flex:none}
.cock-f{padding:10px 16px;border-top:1px solid var(--line2);font-family:var(--mono);font-size:9.5px;letter-spacing:.16em;color:var(--dim);text-transform:uppercase}
.models{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:28px 0 0}
.model{border:1px solid var(--line2);background:var(--panel);padding:22px 20px;border-top:3px solid var(--c)}
.model .k{font-family:var(--mono);font-size:10.5px;letter-spacing:.22em;color:var(--c);text-transform:uppercase}
.model h3{font-size:clamp(22px,4.4vw,28px);text-transform:uppercase;letter-spacing:-.01em;margin:8px 0 8px;font-weight:800;line-height:1}
.model p{margin:0 0 12px;color:var(--body);font-size:14.5px}
.model dl{margin:0;border-top:1px solid var(--line)}
.model dl div{display:grid;grid-template-columns:92px 1fr;gap:10px;padding:8px 0;border-bottom:1px solid var(--line);font-size:13.5px}
.model dt{font-family:var(--mono);font-size:9.5px;letter-spacing:.18em;color:var(--dim);text-transform:uppercase;padding-top:3px}
.model dd{margin:0;color:var(--body)}
.cover{padding-top:56px}
.cover .fig{margin-top:18px}
.tbl{width:100%;border-collapse:collapse;margin:24px 0 0;font-size:15px}
.tbl th{font-family:var(--mono);font-weight:400;font-size:10px;letter-spacing:.22em;color:var(--mute);text-transform:uppercase;text-align:left;padding:10px 8px 10px 0;border-bottom:1px solid var(--line2)}
.tbl td{padding:12px 8px 12px 0;border-bottom:1px solid var(--line);color:var(--body)}
.tbl td:first-child{color:var(--ink)}
.tbl td.m{font-family:var(--mono);font-size:13.5px}
.big2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:26px 0 0}
.big2 .card b{font-family:var(--mono);font-weight:400;font-size:clamp(30px,6vw,40px);color:var(--green);display:block}
.contact{margin:26px 0 0;border-top:1px solid var(--line2)}
.disc{border:1px solid #3a2a26;background:var(--panel);padding:18px 20px;margin:28px 0 0}
.disc .lab{color:#d9846f}
.disc p{color:var(--mute);font-size:12.5px;margin:8px 0 0}
.loop-list{counter-reset:l;margin:18px 0 0}
a{color:var(--green)}
a:focus-visible{outline:2px solid var(--green);outline-offset:3px}
.flow{animation:dash 1.6s linear infinite}
@keyframes dash{to{stroke-dashoffset:-24}}
.rotor{animation:spin 7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
@media (prefers-reduced-motion:reduce){.flow,.rotor{animation:none}}
@media (max-width:640px){
 body{font-size:16px}
 .stats{grid-template-columns:1fr 1fr}
 .row{grid-template-columns:1fr;gap:4px}
 .grid2,.grid3,.pts,.models,.big2{grid-template-columns:1fr}
 .chk{columns:1}
 .tiles{grid-template-columns:1fr 1fr}.tile:nth-child(3n){border-right:1px solid var(--line)}.tile:nth-child(2n){border-right:0}
 .lrow,.scale{grid-template-columns:1fr;gap:6px}.scale div:first-child{display:none}
 .erow,.ehead{grid-template-columns:1fr 64px}.erow .ebar{grid-column:1/-1;grid-row:2}.ehead div:nth-child(2){display:none}
 .st{grid-template-columns:44px 1fr}
 .hd span:last-child{display:none}
 .fig.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-left:calc(-1*clamp(20px,5.5vw,48px));margin-right:calc(-1*clamp(20px,5.5vw,48px));padding:0 clamp(20px,5.5vw,48px)}
 .fig.scroll svg{min-width:680px}.fig.loop svg{min-width:560px}
 .swipe{display:block}
 .bar-r .x{display:none}
}
"""

ICONS = {
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
    "flame": '<path d="M12 22c4 0 7-3 7-7 0-4-3-6-4-10-2 2-3 4-3 6-1-1-2-2-2-4-3 3-5 5-5 8 0 4 3 7 7 7z"/>',
    "leaf": '<path d="M4 20c0-9 6-15 16-16-1 10-7 16-16 16zM4 20l8-8"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c1-4 4-6 7-6s6 2 7 6"/><circle cx="17" cy="9" r="2.5"/><path d="M17 14c2 0 4 2 5 5"/>',
    "rupee": '<path d="M6 4h12M6 9h12M6 4c7 0 7 10 0 10l9 7"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 4 8 8 9 4-1 8-4 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "box": '<path d="M3 7l9-4 9 4-9 4zM3 7v10l9 4 9-4V7M12 11v10"/>',
    "chart": '<path d="M4 20V4M4 20h16M8 16v-4M12 16V8M16 16v-7"/>',
}


def icon(k):
    return '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % ICONS[k]


def logo():
    return '<span class="logo"><span class="j">joule</span><span class="w">Wise</span></span>'


# ------------------------------------------------------------------ charts
def day_chart(ind):
    W, H, L, R, T, B = 720, 300, 30, 16, 40, 34
    pw, ph = W - L - R, H - T - B
    base_on, base_off, hp_kw = ind["load"]
    hp_start, hp_end = ind.get("hp_window", (9, 16))
    ts = [i / 4 for i in range(97)]

    def smooth(h, a, b, k=.8):
        return 1 / (1 + math.exp(-(h - a) / k * 3)) * (1 - 1 / (1 + math.exp(-(h - b) / k * 3)))

    base = [base_off + (base_on - base_off) * smooth(h, ind.get("shift", (6, 22))[0], ind.get("shift", (6, 22))[1]) for h in ts]
    hp = [hp_kw * smooth(h, hp_start, hp_end, .6) for h in ts]
    load = [b + p for b, p in zip(base, hp)]
    wind = [26 + 7 * math.sin((h - 2) / 24 * 2 * math.pi + 2.2) for h in ts]
    sol = [max(0, 105 * math.sin(math.pi * (h - 6) / 12)) if 6 < h < 18 else 0 for h in ts]
    sol = [min(s, l - w) for s, l, w in zip(sol, load, wind)]
    bess = [min(22, l - w - s) if 17.5 <= h <= 22 else 0 for h, l, w, s in zip(ts, load, wind, sol)]
    mx = 128.0

    def X(i): return L + pw * i / 96

    def Y(v): return T + ph * (1 - v / mx)

    def area(lo, hi, fill, op):
        top = " ".join("%.1f,%.1f" % (X(i), Y(hi[i])) for i in range(97))
        bot = " ".join("%.1f,%.1f" % (X(i), Y(lo[i])) for i in reversed(range(97)))
        return '<polygon points="%s %s" fill="%s" fill-opacity="%s"/>' % (top, bot, fill, op)

    z = [0] * 97
    c1 = wind
    c2 = [a + b for a, b in zip(c1, sol)]
    c3 = [a + b for a, b in zip(c2, bess)]
    o = []
    o.append('<rect x="0" y="0" width="%d" height="%d" fill="#0c0f11" stroke="#2c3237"/>' % (W, H))
    for hh in (0, 6, 12, 18, 24):
        x = L + pw * hh / 24
        o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#1e2327"/>' % (x, T, x, T + ph))
        o.append('<text x="%.1f" y="%d" fill="#5d666c" font-size="10" text-anchor="middle" font-family="IBM Plex Mono,monospace">%02d</text>' % (x, H - 14, hh))
    o.append(area(z, c1, "#1f7a55", .9))
    o.append(area(c1, c2, "#3dd68c", .75))
    o.append(area(c2, c3, "#5b8def", .8))
    o.append(area(c3, load, "#8fd9b6", .28))
    o.append(area(base, load, "#f2994a", .0))
    hpband = " ".join("%.1f,%.1f" % (X(i), Y(load[i])) for i in range(97)) + " " + " ".join("%.1f,%.1f" % (X(i), Y(base[i])) for i in reversed(range(97)))
    o.append('<polygon points="%s" fill="url(#hatch)" stroke="#f2994a" stroke-width="1"/>' % hpband)
    o.append('<polyline points="%s" fill="none" stroke="#dfe3e6" stroke-width="1.3" stroke-dasharray="4 3"/>' % " ".join("%.1f,%.1f" % (X(i), Y(load[i])) for i in range(97)))
    lab = 'font-family="IBM Plex Mono,monospace" font-size="10" letter-spacing="1.5"'
    o.append('<text x="%d" y="22" fill="#8b949a" %s>24 HOURS · 96 BLOCKS · ILLUSTRATIVE</text>' % (L, lab))
    o.append('<text x="%.1f" y="%.1f" fill="#f2994a" %s text-anchor="middle">HEAT PUMPS + STORE</text>' % (X(50), Y(load[50]) - 10, lab))
    o.append('<text x="%.1f" y="%.1f" fill="#0a0b0c" %s text-anchor="middle" font-weight="600">SOLAR</text>' % (X(48), Y(c2[48] * .55 + c1[48] * .45), lab))
    o.append('<text x="%.1f" y="%.1f" fill="#cfe9dc" %s>WIND · ISTS</text>' % (X(2), Y(c1[4] * .45), lab))
    o.append('<text x="%.1f" y="%.1f" fill="#dbe6ff" %s text-anchor="middle">BESS</text>' % (X(79), Y((c2[79] + c3[79]) / 2) + 3, lab))
    o.append('<text x="%.1f" y="%.1f" fill="#b9ecd3" %s text-anchor="middle">GREEN MARKET</text>' % (X(80), Y((c3[80] + load[80]) / 2) + 4, lab))
    o.append('<text x="%.1f" y="%.1f" fill="#dfe3e6" %s text-anchor="end">PLANT LOAD</text>' % (X(95), Y(load[92]) - 8, lab))
    defs = '<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#f2994a" fill-opacity=".18"/><line x1="0" y1="0" x2="0" y2="6" stroke="#f2994a" stroke-width="1.4" stroke-opacity=".6"/></pattern></defs>'
    return '<svg viewBox="0 0 %d %d" role="img" aria-label="Illustrative 24-hour green supply stack with heat pump load shifted into solar hours">%s%s</svg>' % (W, H, defs, "".join(o))


def loop_svg():
    W = 760
    cx, cy, r = 380, 262, 168
    nodes = [("GREEN POWER", "open access · rooftop · BESS", C["green"], -90),
             ("HEAT PUMPS", "hot water · LP steam", C["heat"], -18),
             ("THERMAL STORE", "heat made in cheap blocks", C["heat"], 54),
             ("ergOS", "meters · forecasts · trades", C["data"], 126),
             ("esgOS", "Scope 1·2·3 · BRSR", C["esg"], 198)]
    o = ['<defs><marker id="ar" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="#5d666c"/></marker></defs>']
    o.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#1e2327" stroke-width="1"/>' % (cx, cy, r))
    for i in range(5):
        a0 = math.radians(nodes[i][3] + 14)
        a1 = math.radians(nodes[(i + 1) % 5][3] - 14 + (360 if i == 4 else 0))
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        col = nodes[i][2]
        o.append('<path class="flow" d="M%.1f,%.1f A%d,%d 0 0 1 %.1f,%.1f" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="3 8" marker-end="url(#ar)"/>' % (x0, y0, r, r, x1, y1, col))
    for name, sub, col, ang in nodes:
        a = math.radians(ang)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        o.append('<circle cx="%.1f" cy="%.1f" r="34" fill="#0c0f11" stroke="%s" stroke-width="1.6"/><circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (x, y, col, x, y, col))
        tx, ty, anc = x, y + 58, "middle"
        if math.cos(a) > .5:
            tx, ty, anc = x + 46, y - 4, "start"
        elif math.cos(a) < -.5:
            tx, ty, anc = x - 46, y - 4, "end"
        if ang == -90:
            tx, ty, anc = x + 48, y - 8, "start"
        o.append('<text x="%.1f" y="%.1f" fill="%s" font-size="17" font-weight="700" letter-spacing="1" text-anchor="%s" font-family="Inter Tight,Helvetica,Arial,sans-serif">%s</text>' % (tx, ty, col, anc, name))
        o.append('<text x="%.1f" y="%.1f" fill="#8b949a" font-size="12.5" text-anchor="%s" font-family="IBM Plex Mono,monospace">%s</text>' % (tx, ty + 20, anc, sub))
    o.append('<text x="%d" y="%d" fill="#eef0f1" font-size="30" font-weight="800" text-anchor="middle" font-family="Inter Tight,Helvetica,Arial,sans-serif">ONE</text>' % (cx, cy - 8))
    o.append('<text x="%d" y="%d" fill="#eef0f1" font-size="30" font-weight="800" text-anchor="middle" font-family="Inter Tight,Helvetica,Arial,sans-serif">PROVIDER</text>' % (cx, cy + 24))
    o.append('<text x="%d" y="%d" fill="#3dd68c" font-size="11" letter-spacing="2.5" text-anchor="middle" font-family="IBM Plex Mono,monospace">SAVINGS FUND THE NEXT STEP</text>' % (cx, cy + 52))
    return '<svg viewBox="0 0 %d 480" role="img" aria-label="Ecosystem loop: green power feeds heat pumps and thermal storage, ergOS orchestrates, esgOS discloses">%s</svg>' % (W, "".join(o).replace('cy="300"', 'cy="300"'))


def econ(ind):
    cop = ind["cop"]
    rows = [
        ("PNG-fired boiler", "₹55/SCM · 85% efficiency", 55 / (10.4 * .85), 1.95 / (10.4 * .85), "#5d666c"),
        ("Diesel (HSD) boiler", "₹90/L · 85% efficiency", 90 / (10.0 * .85), 2.68 / (10.0 * .85), "#5d666c"),
    ] + ind.get("extra_fuels", []) + [
        ("Heat pump on DISCOM power", "₹8.5/kWh · COP %.1f" % cop, 8.5 / cop, .716 / cop, "#f2994a"),
        ("Heat pump on green open access", "₹5.5/kWh landed · COP %.1f" % cop, 5.5 / cop, 0.0, "#3dd68c"),
        ("Heat pump in solar blocks + store", "₹4.0/kWh · COP %.1f" % cop, 4.0 / cop, 0.0, "#3dd68c"),
    ]
    mxc = max(r[2] for r in rows)
    mxe = max(r[3] for r in rows)
    o = ['<div class="econ"><div class="ehead"><div class="lab">Source of heat</div><div class="lab">₹ per kWh of useful heat</div><div class="lab" style="text-align:right">₹/kWh-th</div></div>']
    for n, s, c, e, col in rows:
        o.append('<div class="erow"><div class="nm">%s<small>%s</small></div><div class="ebar"><i style="width:%.1f%%;background:%s"></i></div><div class="v">%.2f</div></div>' % (n, s, 100 * c / mxc, col, c))
    o.append('</div><div class="econ"><div class="ehead"><div class="lab">Source of heat</div><div class="lab">kg CO₂ per kWh of useful heat</div><div class="lab" style="text-align:right">kg/kWh-th</div></div>')
    for n, s, c, e, col in rows:
        w = 100 * e / mxe
        o.append('<div class="erow"><div class="nm">%s</div><div class="ebar"><i style="width:%.1f%%;background:%s;opacity:.75"></i></div><div class="v">%s</div></div>' % (n, max(w, .6), col, "%.2f" % e if e else "≈ 0"))
    o.append('</div>')
    return "".join(o), rows


# ------------------------------------------------------------------ page shell
def page(num, total, left, right, body, ind):
    return '<section class="pg" id="p%02d"><div class="hd"><span>%02d / %s</span><span>%s</span></div>%s<div class="ft"><span>jouleWise · decarbonisation stack · %s</span><span>%02d / %02d</span></div></section>' % (
        num, num, left, right, body, ind["short"], num, total)


def build(ind):
    pages = []
    scene_svg = getattr(scenes, ind["scene"])()

    # 00 cover
    cover = ('<div class="eb">%s <i>/ power · heat · proof</i></div>' % E(ind["short"]) +
             '<h1>Green power.<br>Green heat.<br><span class="g">One stack.</span></h1>' +
             '<p class="sub">%s</p>' % ind["cover_h2"] +
             '<p class="lede">%s</p>' % ind["cover_p"] +
             '<div class="fig">%s</div>' % scenes.cover_stack() +
             '<div class="stats">' + "".join('<div class="stat"><b>%s</b><span class="lab">%s</span></div>' % s for s in [
                 ("4", "layers · power, heat, data, ESG"), ("120 °C", "heat pump range · hot water and steam"),
                 ("15-min", "metered heartbeat on ergOS"), ("1", "accountable provider")]) + '</div>')
    pages.append(("Cover", "Industrial decarbonisation", cover))

    # 01 executive summary
    ex = ind["exec"]
    rows = "".join('<div class="row"><div class="lab">%s</div><p>%s</p></div>' % r for r in [
        ("The situation", ex["situation"]),
        ("The gap", "Power, heat and ESG reporting are bought from different vendors on different clocks. Solar is sized without the heat load; boilers are replaced without a plan for cheaper power; ESG data is typed in once a year. Each fix leaves money and carbon on the table."),
        ("What we do", "jouleWise runs the whole decarbonisation stack: <b>green power</b> — intrastate and ISTS solar and wind, rooftop solar, BESS and green-market purchase, each source orchestrated to fulfil industrial demand at least cost; <b>ABT metering and data loggers</b> on every source and load; <b>green heat</b> from industrial heat pumps up to 120 °C; <b>ergOS</b> to meter and orchestrate both every 15 minutes; <b>esgOS</b> to turn the same data into audit-ready disclosure."),
        ("Why it compounds", "Cheaper green power lowers the cost of every unit of heat a heat pump makes. Thermal storage lets that heat be made in the cheapest solar blocks. ergOS proves it; esgOS reports it. Savings from one layer fund the next."),
        ("The value", ex["value"]),
        ("How to engage", "Four models, mix and match: <b>Advisory</b>, <b>SaaS</b> (ergOS + esgOS), <b>Heat Advisory</b>, and <b>Heat as a Service</b>, where you pay per unit of heat and invest nothing upfront."),
        ("First step", ex["first"]),
    ])
    exs = ('<div class="eb">Executive summary <i>/ %s</i></div>' % E(ind["short"]) +
           '<h2>%s</h2>' % ex["headline"] + '<div class="rows">%s</div>' % rows +
           '<div class="big2"><div class="card"><b>up to 25%</b><span class="lab">cost savings on DISCOM tariff</span></div><div class="card"><b>up to 65%</b><span class="lab">renewable share achieved</span></div></div>' +
           '<p class="note">Reported client impact, year 1 of ergOS; C&amp;I client outcomes. Results vary with state, tariff structure and load profile. %s-specific value is quantified in the baseline.</p>' % E(ind["short"]))
    pages.append(("Executive summary", "For leadership", exs))

    # 02 why now
    cards = "".join('<div class="card">%s<h3>%s</h3><p>%s</p></div>' % (icon(i), t, d) for i, t, d in ind["drivers"])
    why = ('<div class="eb">Why now <i>/ %s</i></div>' % E(ind["short"]) + '<h2>%s</h2>' % ind["why_h"] +
           '<p class="lede">%s</p>' % ind["why_p"] + '<div class="grid2">%s</div>' % cards)
    pages.append(("Why now", "Pressures on the plant", why))

    # 03 the stack / loop
    loop_items = [
        ("power", "Green power", "Intrastate and ISTS solar and wind, rooftop solar, BESS and green-market purchase — each source orchestrated to fulfil industrial demand at least cost."),
        ("heat", "Heat pumps", "Every kWh in becomes three to four kWh of useful heat. The boiler stops burning fuel for loads up to 120 °C."),
        ("heat", "Thermal storage", "Heat is made when power is cheapest and greenest, and used when the process needs it."),
        ("data", "ergOS", "Meters power, steam, fuel and water every 15 minutes; forecasts, schedules and trades; runs heat pumps against price."),
        ("esg", "esgOS", "Converts the same metered data to Scope 1, 2 and 3, BRSR Core-format, CBAM, CDP and customer disclosures."),
    ]
    li = "".join('<div class="pt"><span class="num c-%s">%02d</span><div><h4>%s</h4><p>%s</p></div></div>' % (l, i + 1, t, d) for i, (l, t, d) in enumerate(loop_items))
    stack = ('<div class="eb">The ecosystem <i>/ first of its kind</i></div>' +
             '<h2>One stack.<br><span class="g">Every layer feeds the next.</span></h2>' +
             '<p class="lede">Most plants buy decarbonisation in pieces. We built it as a loop: low-cost green power feeds heat pumps, storage moves heat into the cheapest blocks, ergOS runs it, esgOS proves it.</p>' +
             '<div class="fig scroll loop">%s</div><div class="pts">%s</div>' % (loop_svg(), li) +
             '<div class="callout"><b>Why the order matters.</b> A heat pump on grid power cuts fuel cost but, at today\'s grid emission factor, barely cuts carbon against gas. Put the same heat pump on green power and its heat is close to zero-carbon. Power first, then heat — from one provider.</div>')
    pages.append(("The stack", "Power → heat → data → ESG", stack))

    # 04 supply chain
    pts = "".join('<div class="pt"><span class="num c-%s">%02d</span><div><h4>%s</h4><p>%s</p><span class="tag c-%s">%s</span></div></div>' % (
        l, n, t, d, l, {"power": "Power", "heat": "Heat", "data": "Data · ergOS", "esg": "ESG · esgOS"}[l]) for n, l, t, d in ind["marks"])
    sc = ('<div class="eb">%s <i>/ where we intervene</i></div>' % E(ind["chain_eb"]) + '<h2>%s</h2>' % ind["chain_h"] +
          '<p class="lede">%s</p>' % ind["chain_p"] + '<div class="fig scroll">%s</div><span class="swipe">Swipe to see the whole plant</span>' % scene_svg +
          '<div class="legend"><span><i class="sw" style="background:var(--green)"></i>Power</span><span><i class="sw" style="background:var(--heat)"></i>Heat</span><span><i class="sw" style="background:var(--data)"></i>Data · ergOS</span><span><i class="sw" style="background:var(--esg)"></i>ESG · esgOS</span></div>' +
          '<div class="pts">%s</div><p class="note">Illustrative plant. Actual intervention map built site by site in the baseline.</p>' % pts)
    pages.append(("Supply chain", "Intervention map", sc))

    # 05 power
    steps = [("Plan", "Meter-data due diligence: bills, load survey, rooftop and captive parameters. Solar, wind, hybrid, BESS and exchange power optimised together, capex or opex, with each state's ToD, banking and open access charges in the landed-cost model.", "RE-100 roadmap · size, location, savings, NPV"),
             ("Implement", "RfP over a 25-year horizon, developer evaluation, reverse auction, PPA and shareholder agreements (26% SPV equity for captive status), open access approvals and connection agreement.", "Green power contracted · ~3 months once planning closes"),
             ("Meter and log", "ABT meters at injection and drawal points — main and check meters on CTs and PTs of the required accuracy class — plus data loggers on every incomer, heat pump, steam, fuel and water line. Installed, tested, sealed and linked to the SLDC and to ergOS.", "Every source and load visible in 15-minute blocks"),
             ("Orchestrate", "ergOS forecasts 96 blocks, schedules with the SLDC, trades DAM, GDAM, RTM and GTAM, manages banking and battery health — and now dispatches heat pumps and thermal storage against price.", "For the life of the assets")]
    st = "".join('<div class="st"><div class="n">%02d</div><div><h4>%s</h4><p>%s</p><div class="out">%s</div></div></div>' % (i + 1, a, b, c) for i, (a, b, c) in enumerate(steps))
    pw = ('<div class="eb">Layer 01 <i>/ power</i></div>' + '<h2>Low-cost<br><span class="g">green power.</span></h2>' +
          '<p class="lede">%s</p>' % ind["power_p"] + '<div class="callout"><b>Every source, one dispatch.</b> Intrastate and ISTS solar and wind, rooftop solar, BESS and green-market purchase — each source orchestrated to fulfil industrial demand at least cost.</div>' + '<div class="fig">%s</div>' % day_chart(ind) +
          '<div class="legend"><span><i class="sw" style="background:#1f7a55"></i>Wind · ISTS</span><span><i class="sw" style="background:#3dd68c"></i>Solar</span><span><i class="sw" style="background:#5b8def"></i>BESS</span><span><i class="sw" style="background:#8fd9b6;opacity:.5"></i>Green market</span><span><i class="sw" style="border:1px solid #f2994a;background:rgba(242,153,74,.25)"></i>Heat pump load</span></div>' +
          '<div class="seq">%s</div>' % st)
    pages.append(("Power", "Plan · implement · meter · orchestrate", pw))

    # 05b heat pump 101
    pages.append(("Heat pump 101", "What is a heat pump", hp101.page_body(icon)))

    # 06 heat
    lad = []
    for n, sub, lo, hi in ind["heat_loads"]:
        fits = hi <= 120
        col = "var(--heat)" if fits else "#5d666c"
        lad.append('<div class="lrow"><div class="nm">%s<small>%s</small></div><div class="track"><span class="rg" style="left:%.1f%%;width:%.1f%%;background:%s"></span><span class="cap" style="left:60%%"></span></div></div>' % (
            n, sub, lo / 2, max((hi - lo) / 2, 1.2), col))
    heat = ('<div class="eb">Layer 02 <i>/ heat</i></div>' + '<h2>The boiler,<br><span class="h">reinvented.</span></h2>' +
            '<p class="lede">%s</p>' % ind["heat_p"] +
            '<div class="ladder">%s</div><div class="scale"><div></div><div><span style="left:0">0 °C</span><span style="left:25%%">50</span><span style="left:50%%">100</span><span class="c-heat" style="left:60%%">120</span><span style="left:75%%">150</span><span style="left:100%%">200 °C</span></div></div>' % "".join(lad) +
            '<div class="legend"><span><i class="sw" style="background:var(--heat)"></i>Heat pump range</span><span><i class="sw" style="background:#5d666c"></i>Stays on existing burners or electrode heat</span><span><i class="sw" style="border-left:2px dashed var(--heat)"></i>120 °C ceiling</span></div>' +
            '<div class="grid3">' + "".join('<div class="card">%s<h3>%s</h3><p>%s</p></div>' % x for x in [
                (icon("flame"), "Heat sources we reuse", ind["heat_src"]),
                (icon("bolt"), ind.get("heat_dual_t", "Heating and cooling at once"), ind["heat_dual"]),
                (icon("chart"), "Sized from metered heat", "Portable heat meters log flow and temperature on candidate processes for two to four weeks before anything is sized.")]) + '</div>')
    pages.append(("Heat", "Industrial heat pumps", heat))

    # 07 economics
    etab, erows = econ(ind)
    ec = ('<div class="eb">The loop in numbers <i>/ illustrative</i></div>' + '<h2>Cheaper power<br><span class="g">makes cheaper heat.</span></h2>' +
          '<p class="lede">What one kWh of useful process heat costs, and what it emits, depending on where the heat comes from. The heat pump cuts cost on any power; green power is what cuts the carbon.</p>' + etab +
          '<p class="note">Illustrative only, not an offer. Assumptions: PNG 10.4 kWh/SCM, 1.95 kg CO₂/SCM; HSD 10.0 kWh/L, 2.68 kg CO₂/L; grid 0.716 kg CO₂/kWh (CEA baseline order of magnitude); green power treated as zero-emission on a market basis with green attributes retired. Heat pump COP %.1f reflects %s; COP falls as delivery temperature rises. Tariffs, fuel prices and COP vary by site and are replaced with metered values in the baseline.%s</p>' % (ind["cop"], ind["cop_note"], ind.get("extra_note", "")))
    pages.append(("Economics", "Cost and carbon per unit of heat", ec))

    # 08 ergOS
    ck = ind["cockpit"]
    tiles = "".join('<div class="tile"><small style="color:var(--mute)">%s</small><b style="color:%s">%s</b><small style="color:%s">%s</small></div>' % t for t in ck["tiles"])
    ops = "".join('<div class="op"><i style="color:%s">%s</i><span>%s</span></div>' % o for o in ck["ops"])
    eo = ('<div class="eb">Layer 03 <i>/ data · ergOS</i></div>' + '<h2>One screen.<br><span class="g">Power and heat.</span></h2>' +
          '<p class="lede">ergOS is the operating layer. It sits on every meter, every source and every heat pump — watching prices, weather, storage and the production plan, and acting every 15 minutes.</p>' +
          '<div class="cock"><div class="cock-h"><span>ergOS · %s</span><b>● Live</b></div><div class="tiles">%s</div><div class="ops">%s</div><div class="cock-f">Illustrative screen · values indicative</div></div>' % (ck["title"], tiles, ops) +
          '<div class="grid3">' + "".join('<div class="card">%s<h3>%s</h3><p>%s</p></div>' % x for x in [
              (icon("chart"), "Forecast and trade", "96-block day-ahead load, SLDC scheduling, DAM, GDAM, RTM and GTAM bids, deviation settled block by block."),
              (icon("flame"), "Dispatch heat", "Heat pumps and thermal stores charged in the cheapest, greenest blocks, within process temperature limits."),
              (icon("shield"), "Bill and bank", "Banked-energy ledger, audit-ready billing and state-wise compliance tracked continuously.")]) + '</div>')
    pages.append(("ergOS", "Orchestration", eo))

    # 09 esgOS
    outs = "".join("<li>%s</li>" % x for x in ind["esg_out"])
    es = ('<div class="eb">Layer 04 <i>/ ESG · esgOS</i></div>' + '<h2>ESG, operated.<br><span class="g">Not reported.</span></h2>' +
          '<p class="lede">The same data that runs the plant produces the disclosure. Metered where possible, integrated where the data already lives, audited where it does not.</p>' +
          '<div class="grid3">' + "".join('<div class="card" style="border-top:3px solid %s"><div class="lab" style="color:%s">%s</div><h3>%s</h3><p>%s</p></div>' % x for x in [
              ("var(--green)", "var(--green)", "First choice", "Meter", "Electricity, steam, thermal energy, fuel flow and water — every 15 minutes."),
              ("var(--data)", "var(--data)", "Second", "Integrate", "ERP, HRMS, EHS tools and portals — no retyping."),
              ("var(--esg)", "var(--esg)", "Last resort", "Audit", "Refrigerant, waste, safety and supplier data — photo-evidenced and signed off.")]) + '</div>' +
          '<p class="lab" style="margin-top:30px">What esgOS produces for %s</p><ul class="chk">%s</ul>' % (E(ind["short"].lower()), outs) +
          '<div class="callout"><b>Deterministic by design.</b> Regulations and methodologies are stored as versioned, machine-readable rules and run by a rule engine. AI extracts, explains and drafts — it never produces a reported number.</div>')
    pages.append(("esgOS", "Disclosure", es))

    # 10 models
    models = [
        ("var(--green)", "Model 01", "Advisory", "Power strategy and delivery, from RE-100 roadmap to live open access.",
         [("Scope", "RE-100 roadmap, RfP and reverse auction, PPA, approvals, ABT metering, regulatory filings"), ("You pay", "Fixed fee, with a success-fee option"), ("Assets", "Owned by you or your developer"), ("Best for", "Plants ready to contract green power")]),
        ("var(--data)", "Model 02", "SaaS", "ergOS and esgOS as a subscription — the operating and disclosure layers.",
         [("Scope", "15-minute metering, forecasting, trading support, heat dispatch, ESG pipeline and reports"), ("You pay", "Per plant, per year"), ("Assets", "Meters per BOQ; platform hosted"), ("Best for", "Multi-plant groups that want one source of truth")]),
        ("var(--heat)", "Model 03", "Heat Advisory", "Engineering-grade route from boiler to heat pump, with you owning the asset.",
         [("Scope", "Heat audit and metering, pinch and waste-heat study, heat pump sizing, vendor selection, EPC oversight, commissioning"), ("You pay", "Fixed fee per study and per project stage"), ("Assets", "Owned by you (capex)"), ("Best for", "Plants with capex budget and a fuel-cost target")]),
        ("var(--heat)", "Model 04", "Heat as a Service", "You buy heat, not equipment. Hot water and low-pressure steam delivered to your header.",
         [("Scope", "Design, install, own, operate and maintain heat pumps and storage; powered by jouleWise green power; run on ergOS"), ("You pay", "Per unit of heat delivered, priced against your current fuel cost"), ("Assets", "Owned on the jouleWise side — zero upfront capex"), ("Best for", "Plants that want green steam now, off balance sheet")]),
    ]
    mh = "".join('<div class="model" style="--c:%s"><div class="k">%s</div><h3>%s</h3><p>%s</p><dl>%s</dl></div>' % (
        c, k, t, d, "".join("<div><dt>%s</dt><dd>%s</dd></div>" % x for x in dl)) for c, k, t, d, dl in models)
    md = ('<div class="eb">Working models <i>/ how to engage</i></div>' + '<h2>Four ways in.<br><span class="g">One provider.</span></h2>' +
          '<p class="lede">Start where the value is largest for your plant. Models combine — most clients begin with Advisory and SaaS on power, then add heat.</p>' +
          '<div class="models">%s</div><p class="note">Commercial terms indicative and finalised per engagement.</p>' % mh)
    pages.append(("Models", "Advisory · SaaS · Heat", md))

    # 11 roadmap
    rm = [("Baseline", "Weeks 1–4", "Bills, load survey, fuel and steam records, portable heat metering on candidate processes, ESG data map.", "Signed-off energy, heat and carbon baseline"),
          ("Roadmap", "Weeks 4–8", ind["roadmap2"], "One business case — power, heat, ESG"),
          ("Meter and log", "Weeks 6–12", "ABT metering at the incomer and data loggers on power, heat, fuel and water lines — the measured base every later step is sized, settled and reported on.", "ergOS live on metered data"),
          ("Power live", "~3 months after roadmap", "Open access contracted and approved; rooftop solar and BESS where they fit; every source orchestrated against demand on ergOS.", "Green power flowing"),
          ("Heat live", "Pilot, then scale", ind["roadmap4"], "Fuel displaced, measured on ergOS"),
          ("Operate and disclose", "Every block · every year", "ergOS runs power and heat; esgOS publishes BRSR Core-format, CBAM, CDP and customer disclosures with an audit trail.", "Assurance-ready numbers")]
    rs = "".join('<div class="st"><div class="n">%02d</div><div><h4>%s <span class="lab" style="margin-left:8px">%s</span></h4><p>%s</p><div class="out">%s</div></div></div>' % (i + 1, a, w, b, c) for i, (a, w, b, c) in enumerate(rm))
    rd = ('<div class="eb">The roadmap <i>/ indicative</i></div>' + '<h2>Baseline.<br>Power. Heat.<br><span class="g">Proof.</span></h2>' +
          '<div class="seq">%s</div><p class="note">Timelines indicative; confirmed after the baseline and dependent on state approvals and equipment lead times.</p>' % rs)
    pages.append(("Roadmap", "From baseline to proof", rd))

    # 12 track record
    clients = [("Dalmia Cement", "Cement", "~300 MW"), ("Chettinad Cement", "Cement", "~200 MW"), ("SAEL", "Solar cells", "~160 MW"),
               ("Wonder Cement", "Cement", "~140 MW"), ("Haldiram's", "Snacks &amp; beverages", "~35 MW"), ("Bikaji", "Snacks", "~25 MW"),
               ("Bharatiyam (Campa)", "Beverages", "~19 MW")]
    tb = "".join('<tr><td>%s</td><td>%s</td><td class="m">%s</td></tr>' % c for c in clients)
    tr = ('<div class="eb">Track record <i>/ RE-100 assignments</i></div>' + '<h2>~1 GW of<br>RE-100 study scope.</h2>' +
          '<p class="lede">RE-100 assignments across eight industrial groups, cement to FMCG. Deep Indian power-sector regulatory work, with team experience on lender\'s-engineer mandates.</p>' +
          '<table class="tbl"><thead><tr><th>Client</th><th>Industry</th><th>RE study scope</th></tr></thead><tbody>%s</tbody></table>' % tb +
          '<div class="stats">' + "".join('<div class="stat"><b>%s</b><span class="lab">%s</span></div>' % s for s in [
              ("1 GW+", "RE project work by our team"), ("15+", "state regulatory jurisdictions"), ("8", "industries served"), ("20+", "years of leadership in energy")]) + '</div>' +
          '<p class="note">Industries: food &amp; beverages, FMCG, cement, chemicals, textiles, metals, automotive ancillary, solar manufacturing, real estate. ISO 9001:2015 · ISO 27001.</p>')
    pages.append(("Track record", "Clients", tr))

    # 13 contact
    ct = ('<div class="eb">Let\'s talk <i>/ start with one plant</i></div>' + '<h2>Tell us the plant.<br><span class="g">We\'ll map the stack.</span></h2>' +
          '<p class="lede">Send one year of electricity bills and fuel records. We return the baseline, the power-and-heat roadmap and the business case.</p>' +
          '<div class="contact"><div class="row"><div class="lab" style="color:var(--green)">Electricity</div><p><b>Praveen Sharma</b><br><a href="mailto:praveen.sharma@joulewise.com">praveen.sharma@joulewise.com</a> · <a href="tel:+919214337500">+91 92143 37500</a></p></div><div class="row"><div class="lab" style="color:var(--heat)">Heat</div><p><b>Gautam Prasad</b><br><a href="mailto:gautam.prasad@joulewise.com">gautam.prasad@joulewise.com</a></p></div><div class="row"><div class="lab">jouleWise</div><p>joulewise.com<br><span style="color:var(--mute)">jouleWise Advisory Services Pvt Ltd · Noida, India · Spain · ISO 9001:2015 · ISO 27001</span></p></div></div>' +
          '<div class="disc"><div class="lab">Disclaimer</div><p>This presentation is issued for discussion purposes only. Prices, durations, heat pump performance and outcomes shown are indicative, depend on site, state, load profile, process temperatures, contracted terms, exchange prices and the regulatory orders in force, and do not constitute an offer, warranty or commitment by jouleWise. Screens and plant illustrations are illustrative. Client names are cited from jouleWise assignments. Any engagement is governed solely by definitive agreements between the parties.</p></div>')
    pages.append(("Contact", "Let's talk", ct))

    total = len(pages) - 1
    body = []
    for i, (l, r, b) in enumerate(pages):
        if i == 0:
            body.append('<section class="pg cover" id="p00">%s<div class="ft"><span>joulewise.com</span><span>For discussion purposes only</span></div></section>' % b)
        else:
            body.append(page(i, total, l, r, b, ind))
    js = """<script>(function(){var p=document.querySelector('.prog'),c=document.getElementById('cur'),s=[].slice.call(document.querySelectorAll('.pg'));
function u(){var h=document.documentElement,m=h.scrollHeight-h.clientHeight;p.style.width=(m>0?100*h.scrollTop/m:0)+'%';var k=0;s.forEach(function(e,i){if(e.getBoundingClientRect().top<120)k=i});c.textContent=(k<10?'0':'')+k}
addEventListener('scroll',u,{passive:true});u()})()</script>"""
    out = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>jouleWise · Decarbonisation stack · %s</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter+Tight:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>%s%s</style></head><body>
<header class="bar"><div class="bar-in">%s<div class="bar-r"><span class="x">Decarbonisation stack · </span><b>%s</b> · <span id="cur">00</span>/%02d</div></div><div class="prog"></div></header>
<main>%s</main>%s</body></html>""" % (ind["short"], CSS, hp101.CSS, logo(), ind["short"], total, "".join(body), js)
    for a, b in ind.get("subs", []):
        out = out.replace(a, b)
    return out
