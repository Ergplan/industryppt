def cycle_svg():
    M = 'font-family="IBM Plex Mono,monospace"'
    S = 'font-family="Inter Tight,Helvetica,Arial,sans-serif"'
    o = ['<defs><marker id="ah" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="context-stroke"/></marker>'
         '<marker id="ahb" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="#5b8def"/></marker>'
         '<marker id="aho" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="#f2994a"/></marker></defs>']
    # refrigerant loop
    segs = [("M180,160 L180,110 L346,110", "#8fb3f5"), ("M414,110 L580,110 L580,160", "#f2994a"),
            ("M580,280 L580,330 L404,330", "#f7c08f"), ("M356,330 L180,330 L180,280", "#5b8def")]
    for d, c in segs:
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="7" stroke-opacity=".18"/>' % (d, c))
        o.append('<path class="flow" d="%s" fill="none" stroke="%s" stroke-width="2.4" stroke-dasharray="4 8"/>' % (d, c))
    # evaporator + condenser coils
    for x, c, f in ((150, "#5b8def", "#0f1726"), (550, "#f2994a", "#231709")):
        o.append('<rect x="%d" y="160" width="60" height="120" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, f, c))
        zz = " ".join("%d,%d" % (x + (12 if i % 2 == 0 else 48), 170 + i * 10) for i in range(11))
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="1.4"/>' % (zz, c))
    # compressor
    o.append('<circle cx="380" cy="110" r="34" fill="#141719" stroke="#dfe3e6" stroke-width="1.6"/><path d="M366,98 L394,110 L366,122" fill="none" stroke="#dfe3e6" stroke-width="1.6"/>')
    o.append('<line x1="380" y1="30" x2="380" y2="70" stroke="#3dd68c" stroke-width="2.2" marker-end="url(#ah)"/>')
    o.append('<path d="M388,14 l-8,11 h7 l-3,9 l9,-12 h-7z" fill="#3dd68c"/>')
    o.append('<text x="400" y="30" fill="#3dd68c" font-size="13" letter-spacing="1.5" %s>ELECTRICITY · 1 kWh</text>' % M)
    # valve
    o.append('<path d="M356,316 L404,344 L404,316 L356,344z" fill="#141719" stroke="#dfe3e6" stroke-width="1.6"/>')
    # source / sink arrows
    for y in (190, 220, 250):
        o.append('<line x1="20" y1="%d" x2="136" y2="%d" stroke="#5b8def" stroke-width="2" marker-end="url(#ahb)"/>' % (y, y))
        o.append('<line x1="624" y1="%d" x2="740" y2="%d" stroke="#f2994a" stroke-width="2" marker-end="url(#aho)"/>' % (y, y))
    for x, a, col, t1, t2, subs in ((20, "start", "#5b8def", "FREE HEAT", "2.5 kWh", ("air · waste heat", "chiller return", "20–40 °C")),
                                   (740, "end", "#f2994a", "USEFUL HEAT", "3.5 kWh", ("hot water", "low-pressure steam", "up to 120 °C"))):
        o.append('<text x="%d" y="140" fill="%s" font-size="17" font-weight="700" text-anchor="%s" %s>%s</text>' % (x, col, a, S, t1))
        o.append('<text x="%d" y="162" fill="%s" font-size="15" text-anchor="%s" %s>%s</text>' % (x, col, a, M, t2))
        for k, t in enumerate(subs):
            o.append('<text x="%d" y="%d" fill="#8b949a" font-size="11.5" text-anchor="%s" %s>%s</text>' % (x, 284 + k * 16, a, M, t))
    # step labels
    L = [(222, 222, "start", "01 EVAPORATE", "refrigerant boils,", "soaking up low heat"),
         (380, 170, "middle", "02 COMPRESS", "electricity squeezes the", "gas — it gets hot"),
         (538, 222, "end", "03 CONDENSE", "hot gas gives its heat", "to process water"),
         (380, 364, "middle", "04 EXPAND", "pressure drops, it goes", "cold — and repeats")]
    for x, y, a, t, s1, s2 in L:
        o.append('<text x="%d" y="%d" fill="#eef0f1" font-size="12.5" font-weight="600" letter-spacing="1.2" text-anchor="%s" %s>%s</text>' % (x, y, a, M, t))
        o.append('<text x="%d" y="%d" fill="#8b949a" font-size="11" text-anchor="%s" %s>%s</text>' % (x, y + 17, a, M, s1))
        o.append('<text x="%d" y="%d" fill="#8b949a" font-size="11" text-anchor="%s" %s>%s</text>' % (x, y + 31, a, M, s2))
    o.append('<text x="380" y="422" fill="#5d666c" font-size="10.5" letter-spacing="2" text-anchor="middle" %s>REFRIGERANT CIRCUIT · CLOSED LOOP · ILLUSTRATIVE COP 3.5</text>' % M)
    return '<svg viewBox="0 0 760 432" role="img" aria-label="Heat pump cycle: evaporator absorbs free heat, compressor lifts it with electricity, condenser releases useful heat, expansion valve resets">%s</svg>' % "".join(o)


def balance():
    def seg(v, col, lab):
        return '<span style="width:%.2f%%;background:%s" title="%s"></span>' % (100 * v / 3.5, col, lab)
    rows = [("Fuel boiler", [seg(1, "#5d666c", "fuel")], "1 kWh fuel", [seg(.85, "#f2994a", "heat")], "0.85 kWh heat",
             '[["fuel",1.0]]', 0.85),
            ("Heat pump", [seg(1, "#3dd68c", "electricity"), seg(2.5, "#5b8def", "free heat")], "1 kWh power + 2.5 free", [seg(3.5, "#f2994a", "heat")], "3.5 kWh heat",
             '[["electricity",1.0],["free",2.5]]', 3.5)]
    # data-* mirror the bars for lib/deck-interactive.js; the bars alone carry no numbers
    h = ['<div class="bal" data-jw="balance">']
    for n, i, il, oo, ol, ins, out in rows:
        h.append('<div class="brow" data-name="%s" data-in=\'%s\' data-out="%s"><div class="bn">%s</div><div class="bb"><div class="bt">%s</div><small>in · %s</small><div class="bt">%s</div><small class="c-heat">out · %s</small></div></div>' % (n, ins, out, n, "".join(i), il, "".join(oo), ol))
    h.append('</div>')
    return "".join(h)


CSS = """
.bal{margin:26px 0 0;border-top:1px solid var(--line2)}
.brow{display:grid;grid-template-columns:130px 1fr;gap:14px;padding:14px 0;border-bottom:1px solid var(--line)}
.bn{font-weight:700;font-size:15px;padding-top:2px}
.bt{display:flex;height:12px;margin-top:4px}.bt span{display:block;height:100%}
.bb small{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:5px 0 6px}
.lifts{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line2);margin:26px 0 0}
.lifts div{padding:14px 16px;border-right:1px solid var(--line)}.lifts div:last-child{border-right:0}
.lifts b{display:block;font-family:var(--mono);font-weight:400;font-size:clamp(22px,4.6vw,30px);color:var(--heat)}
@media (max-width:640px){.brow{grid-template-columns:1fr;gap:4px}.lifts{grid-template-columns:1fr 1fr}.lifts div:nth-child(2){border-right:0}.lifts div:nth-child(-n+2){border-bottom:1px solid var(--line)}
.fig.cyc svg{min-width:620px}}
"""


def page_body(icon):
    faq = [("Does it replace my boiler?", "For loads up to 120 °C, yes — as the primary heat source. The boiler usually stays on standby and for any loads above that range."),
           ("What if power is expensive?", "Each kWh of power returns three to four kWh of heat, so heat costs roughly a third of the power price. On green open access, the carbon falls close to zero as well."),
           ("What does the site need?", "Spare electrical capacity, space near the heat users and a steady heat demand. A hot-water store smooths peaks and lets the unit run in the cheapest blocks."),
           ("Is it proven?", "It is the same refrigeration cycle as the chillers already on your site, run for heat. Industrial units are in service worldwide in food, chemicals, pharma and textiles.")]
    rows = "".join('<div class="row"><div class="lab">%s</div><p>%s</p></div>' % q for q in faq)
    return ('<div class="eb" style="color:var(--heat)">Heat pump 101 <i>/ the question clients ask most</i></div>' +
            '<h2>What is a<br><span class="h">heat pump?</span></h2>' +
            '<p class="lede">A heat pump is a refrigerator run the other way round. It does not make heat by burning anything — it moves heat that already exists, from a cooler place to a hotter one, and uses electricity only to do the lifting.</p>' +
            '<div class="fig scroll cyc">%s</div><span class="swipe">Swipe to see the whole cycle</span>' % cycle_svg() +
            '<p class="lab" style="margin-top:30px">What goes in, what comes out</p>' + balance() +
            '<p class="note">COP (coefficient of performance) = useful heat ÷ electricity. A boiler can never exceed 1; a heat pump typically delivers 2 to 5.</p>' +
            '<p class="lab" style="margin-top:30px">Temperature lift sets the COP · indicative</p>' +
            '<div class="lifts">' + "".join('<div><b>~%s</b><span class="lab">COP at %s K lift</span></div>' % x for x in [("5", "30"), ("3.5", "50"), ("2.5", "70"), ("2", "90")]) + '</div>' +
            '<p class="note">Lift = delivery temperature minus source temperature. Recovering warm waste heat first and delivering no hotter than the process needs keeps the COP high.</p>' +
            '<div class="rows">%s</div>' % rows)
