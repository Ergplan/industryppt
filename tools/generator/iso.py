import math

C = dict(
    top="#1c2024", left="#15181b", right="#101315", stroke="#3d454c",
    green="#3dd68c", heat="#f2994a", data="#5b8def", esg="#c9a43a",
    solar="#2a4a7a", solarline="#5b8def", ground="#2a3035",
)
LAYER = {"power": C["green"], "heat": C["heat"], "data": C["data"], "esg": C["esg"]}


class Iso:
    def __init__(self, S=8.0, ox=400, oy=140, w=800, h=620):
        self.S, self.ox, self.oy, self.w, self.h = S, ox, oy, w, h
        self.out, self.marks, self.flows = [], [], []

    def xy(self, x, y, z=0):
        return (self.ox + (x - y) * 0.8660 * self.S, self.oy + (x + y) * 0.5 * self.S - z * self.S)

    def pts(self, ps):
        return " ".join("%.1f,%.1f" % self.xy(*p) for p in ps)

    def poly(self, ps, fill, stroke=None, sw=1, extra=""):
        stroke = stroke or C["stroke"]
        self.out.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round" %s/>' % (self.pts(ps), fill, stroke, sw, extra))

    def line(self, ps, stroke, sw=1.2, dash=None, cls="", op=1):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        c = ' class="%s"' % cls if cls else ""
        self.out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" opacity="%s"%s%s/>' % (self.pts(ps), stroke, sw, op, d, c))

    def flow_now(self, ps, color, sw=1.6):
        """animated flow drawn in painter order (can be hidden by buildings)"""
        self.out.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" opacity=".3"/>' % (self.pts(ps), color, sw + 2))
        self.out.append('<polyline class="flow" points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-dasharray="3 9"/>' % (self.pts(ps), color, sw))

    def flow(self, ps, color, sw=2.2):
        """animated energy flow line (drawn over buildings at the end)"""
        self.flows.append((ps, color, sw))

    # ---------- solids
    def box(self, x, y, z, w, d, h, accent=None, top=None, left=None, right=None, sw=1):
        s = accent or C["stroke"]
        self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)], left or C["left"], s, sw)
        self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)], right or C["right"], s, sw)
        self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)], top or C["top"], s, sw)

    def windows(self, x, y, z, w, d, h, n=4, face="left", color="#2b3238"):
        """strip of window panes on +y (left) or +x (right) face"""
        if face == "left":
            step = w / n
            for i in range(n):
                x0 = x + i * step + step * 0.2
                self.poly([(x0, y + d, z + h * .45), (x0 + step * .6, y + d, z + h * .45), (x0 + step * .6, y + d, z + h * .75), (x0, y + d, z + h * .75)], color, color, 0.6)
        else:
            step = d / n
            for i in range(n):
                y0 = y + i * step + step * 0.2
                self.poly([(x + w, y0, z + h * .45), (x + w, y0 + step * .6, z + h * .45), (x + w, y0 + step * .6, z + h * .75), (x + w, y0, z + h * .75)], color, color, 0.6)

    def shed(self, x, y, z, w, d, h, r, accent=None):
        """gable roof building, ridge along x"""
        s = accent or C["stroke"]
        self.box(x, y, z, w, d, h, accent)
        ym = y + d / 2
        self.poly([(x, y, z + h), (x + w, y, z + h), (x + w, ym, z + h + r), (x, ym, z + h + r)], "#181b1e", s)
        self.poly([(x, y + d, z + h), (x + w, y + d, z + h), (x + w, ym, z + h + r), (x, ym, z + h + r)], "#22272b", s)
        self.poly([(x + w, y, z + h), (x + w, y + d, z + h), (x + w, ym, z + h + r)], C["right"], s)

    def sawtooth(self, x, y, z, w, d, h, teeth=4, r=2.2, accent=None):
        s = accent or C["stroke"]
        self.box(x, y, z, w, d, h, accent)
        step = w / teeth
        for i in range(teeth):
            x0 = x + i * step
            self.poly([(x0, y, z + h), (x0, y + d, z + h), (x0 + step, y + d, z + h + r), (x0 + step, y, z + h + r)], "#22272b", s)
            self.poly([(x0 + step, y, z + h), (x0 + step, y + d, z + h), (x0 + step, y + d, z + h + r), (x0 + step, y, z + h + r)], "#1a2a3a", s)

    def cyl(self, cx, cy, z, r, h, accent=None, fill=None, topfill=None, sw=1):
        s = accent or C["stroke"]
        X, Yb = self.xy(cx, cy, z)
        _, Yt = self.xy(cx, cy, z + h)
        rx, ry = r * self.S * 1.2247, r * self.S * 0.7071
        f = fill or C["left"]
        self.out.append('<path d="M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f L%.1f,%.1f Z" fill="%s" stroke="%s" stroke-width="%s"/>' % (X - rx, Yt, X - rx, Yb, rx, ry, X + rx, Yb, X + rx, Yt, f, s, sw))
        self.out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (X, Yt, rx, ry, topfill or C["top"], s, sw))
        return X, Yt

    def rings(self, cx, cy, z, r, hs, color):
        X, _ = self.xy(cx, cy, 0)
        for hh in hs:
            _, Y = self.xy(cx, cy, z + hh)
            rx, ry = r * self.S * 1.2247, r * self.S * 0.7071
            self.out.append('<path d="M%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f" fill="none" stroke="%s" stroke-width=".8"/>' % (X - rx, Y, rx, ry, X + rx, Y, color))

    def ellipse_top(self, cx, cy, z, r, color, fill="none", sw=1):
        X, Y = self.xy(cx, cy, z)
        self.out.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"/>' % (X, Y, r * self.S * 1.2247, r * self.S * .7071, fill, color, sw))

    def panels(self, x, y, z, w, d, rows=3, tilt=0.9):
        """solar rows running along x on a flat surface"""
        gap = d / rows
        for i in range(rows):
            y0 = y + i * gap + gap * 0.15
            y1 = y0 + gap * 0.62
            ps = [(x, y0, z + tilt), (x + w, y0, z + tilt), (x + w, y1, z + 0.1), (x, y1, z + 0.1)]
            self.poly(ps, C["solar"], C["solarline"], 0.7)
            n = max(2, int(w / 2.2))
            for k in range(1, n):
                xk = x + w * k / n
                self.line([(xk, y0, z + tilt), (xk, y1, z + 0.1)], C["solarline"], 0.4, op=.6)

    def solarfield(self, x, y, w, rows=4, d=1.6, gap=2.4):
        for i in range(rows):
            y0 = y + i * gap
            self.poly([(x, y0, 1.1), (x + w, y0, 1.1), (x + w, y0 + d, 0.3), (x, y0 + d, 0.3)], C["solar"], C["solarline"], .8)
            n = int(w / 2)
            for k in range(1, n):
                xk = x + w * k / n
                self.line([(xk, y0, 1.1), (xk, y0 + d, .3)], C["solarline"], .4, op=.6)

    def turbine(self, x, y, h=16, ang=0):
        X, Yb = self.xy(x, y, 0)
        _, Yt = self.xy(x, y, h)
        self.out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#8a949b" stroke-width="1.6"/>' % (X, Yb, X, Yt))
        L = h * self.S * 0.34
        g = ['<g class="rotor" style="transform-origin:%.1fpx %.1fpx">' % (X, Yt)]
        for k in range(3):
            a = math.radians(ang + k * 120)
            g.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#c9d1d6" stroke-width="1.4" stroke-linecap="round"/>' % (X, Yt, X + L * math.cos(a), Yt + L * math.sin(a)))
        g.append('</g><circle cx="%.1f" cy="%.1f" r="1.8" fill="#c9d1d6"/>' % (X, Yt))
        self.out.append("".join(g))

    def pylon(self, x, y, h=12):
        a, b = self.xy(x - .8, y, 0), self.xy(x + .8, y, 0)
        t = self.xy(x, y, h)
        arm = self.xy(x, y, h * .8)
        self.out.append('<path d="M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f M%.1f,%.1f L%.1f,%.1f M%.1f,%.1f L%.1f,%.1f" fill="none" stroke="#6b757c" stroke-width="1"/>' % (
            a[0], a[1], t[0], t[1], b[0], b[1], arm[0] - 9, arm[1], arm[0] + 9, arm[1], (a[0] + t[0]) / 2, (a[1] + t[1]) / 2, (b[0] + t[0]) / 2, (b[1] + t[1]) / 2))
        return (x, y, h * .8)

    def truck(self, x, y, L=6, accent=None, cargo=None):
        self.box(x, y, 0.6, L, 2.2, 2.6, accent, top=cargo)
        self.box(x + L + .2, y + .2, 0.6, 1.8, 1.8, 1.9, accent)
        for xx in (x + 1, x + L - 1, x + L + 1.1):
            X, Y = self.xy(xx, y + 2.2, .6)
            self.out.append('<ellipse cx="%.1f" cy="%.1f" rx="3.3" ry="4" fill="#0c0e10" stroke="%s" stroke-width="1"/>' % (X, Y, accent or C["stroke"]))

    def carcarrier(self, x, y, accent=None):
        self.box(x, y, .6, 9, 2.2, .5, accent)
        for i in range(3):
            self.box(x + .4 + i * 2.9, y + .3, 1.1, 2.4, 1.6, .9, accent, top="#2a3b4a")
        self.box(x + 9.2, y + .2, .6, 1.8, 1.8, 1.9, accent)
        for xx in (x + 1, x + 8, x + 10.1):
            X, Y = self.xy(xx, y + 2.2, .6)
            self.out.append('<ellipse cx="%.1f" cy="%.1f" rx="3.3" ry="4" fill="#0c0e10" stroke="%s" stroke-width="1"/>' % (X, Y, accent or C["stroke"]))

    def person(self, x, y, z=0, hat="#e0a84a"):
        X, Y = self.xy(x, y, z)
        self.out.append('<g><rect x="%.1f" y="%.1f" width="4.4" height="9" rx="1.2" fill="#2a3036"/><rect x="%.1f" y="%.1f" width="4.4" height="2" fill="%s"/><circle cx="%.1f" cy="%.1f" r="2.3" fill="#c9a88a"/><path d="M%.1f,%.1f a2.5,2.5 0 0 1 5,0z" fill="%s"/></g>' % (
            X - 2.2, Y - 10, X - 2.2, Y - 7.5, C["green"], X, Y - 12.2, X - 2.5, Y - 12.6, hat))

    def hp(self, x, y, z=0, w=4, d=3, h=2.6):
        """heat pump skid: box + two fans, heat accent"""
        a = C["heat"]
        self.box(x, y, z, w, d, h, a, sw=1.2)
        self.ellipse_top(x + w * .28, y + d / 2, z + h, min(w, d) * .28, a, "#2a1d10")
        self.ellipse_top(x + w * .72, y + d / 2, z + h, min(w, d) * .28, a, "#2a1d10")
        self.windows(x, y, z, w, d, h, 3, "left", "#3a2a18")

    def container(self, x, y, z=0, w=6, d=2.4, h=2.6, accent=None, n=6):
        a = accent or C["green"]
        self.box(x, y, z, w, d, h, a, left="#0f1a14")
        for i in range(1, n):
            xx = x + w * i / n
            self.line([(xx, y + d, z + .2), (xx, y + d, z + h - .2)], a, .5, op=.6)

    def ground(self, x0, y0, x1, y1):
        self.poly([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], "none", C["ground"], 1, 'stroke-dasharray="4 5"')

    def mark(self, n, anchor, layer, dx=0, dy=-46):
        self.marks.append((n, anchor, layer, dx, dy))

    def render(self, title):
        o = list(self.out)
        for ps, col, sw in self.flows:
            o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" opacity=".35"/>' % (self.pts(ps), col, sw + 2))
            o.append('<polyline class="flow" points="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="3 9"/>' % (self.pts(ps), col, sw))
        for n, a, layer, dx, dy in self.marks:
            col = LAYER[layer]
            X, Y = self.xy(*a)
            mx, my = X + dx, Y + dy
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1" opacity=".9"/>' % (X, Y, mx, my, col))
            o.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (X, Y, col))
            o.append('<g class="mk"><circle cx="%.1f" cy="%.1f" r="15" fill="#0a0b0c" stroke="%s" stroke-width="1.6"/><text x="%.1f" y="%.1f" text-anchor="middle" dominant-baseline="central" fill="%s" font-size="12.5" font-family="IBM Plex Mono, ui-monospace, monospace" font-weight="600">%02d</text></g>' % (mx, my, col, mx, my + .5, col, n))
        return '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">%s</svg>' % (self.w, self.h, title, "".join(o))


def _cut_open(self, x, y, z, w, d, h):
    self.poly([(x, y, z), (x + w, y, z), (x + w, y + d, z), (x, y + d, z)], "#171b1e", C["stroke"], 1)
    for k in range(1, int(w / 2)):
        self.line([(x + k * 2, y, z + .01), (x + k * 2, y + d, z + .01)], "#20262a", .5)
    self.poly([(x, y, z), (x + w, y, z), (x + w, y, z + h), (x, y, z + h)], "#121619", C["stroke"], 1)
    self.poly([(x, y, z), (x, y + d, z), (x, y + d, z + h), (x, y, z + h)], "#0e1113", C["stroke"], 1)


def _cut_close(self, x, y, z, w, d, h, cut=1.0):
    self.poly([(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + cut), (x, y + d, z + cut)], C["left"], C["stroke"], 1)
    self.poly([(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + cut), (x + w, y, z + cut)], C["right"], C["stroke"], 1)
    g = "#58626a"
    self.line([(x, y + d, z + h), (x + w, y + d, z + h), (x + w, y, z + h)], g, .9, dash="3 4")
    for p in ((x, y + d), (x + w, y + d), (x + w, y)):
        self.line([(p[0], p[1], z + cut), (p[0], p[1], z + h)], g, .9, dash="3 4")


def _disc_y(self, cx, y, cz, r, fill, stroke):
    import math as m
    ps = [(cx + r * m.cos(t), y, cz + r * m.sin(t)) for t in [i * m.pi / 8 for i in range(16)]]
    self.poly(ps, fill, stroke, .8)


def _car(self, x, y, z, col="#2c4a66"):
    self.box(x, y, z, 3.6, 1.6, .9, top=col, left="#1e3348", right="#172838")
    self.box(x + .9, y + .15, z + .9, 1.8, 1.3, .6, top="#8fb3d9", left="#243a52", right="#1b2c3e")


def _bottle(self, x, y, z):
    self.cyl(x, y, z, .22, .75, fill="#174a33", topfill="#3dd68c", sw=.5)
    self.cyl(x, y, z + .75, .1, .22, fill="#b14a3a", topfill="#d9624f", sw=.4)


Iso.cut_open = _cut_open
Iso.cut_close = _cut_close
Iso.disc_y = _disc_y
Iso.car = _car
Iso.bottle = _bottle
