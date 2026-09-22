"""Export each industry deck as a self-contained JSON document for the Next.js site.
Text is plain strings; fields ending in `Html` may contain <b>, <br> and <span class="g|h"> only.
SVG artwork is generated here (scenes.py / iso.py) and embedded as strings."""
import json, os, sys
import scenes, industries, hp101
from build import day_chart, loop_svg

GP = "Intrastate and ISTS solar and wind, rooftop solar, BESS and green-market purchase — each source orchestrated to fulfil industrial demand at least cost."
LAYER_TAG = {"power": "Power", "heat": "Heat", "data": "Data · ergOS", "esg": "ESG · esgOS"}


def econ_rows(ind):
    cop = ind["cop"]
    rows = [("PNG-fired boiler", "₹55/SCM · 85% efficiency", 55 / (10.4 * .85), 1.95 / (10.4 * .85), "fuel"),
            ("Diesel (HSD) boiler", "₹90/L · 85% efficiency", 90 / (10.0 * .85), 2.68 / (10.0 * .85), "fuel")]
    rows += [(a, b, c, d, "fuel") for a, b, c, d, _ in ind.get("extra_fuels", [])]
    rows += [("Heat pump on DISCOM power", "₹8.5/kWh · COP %.1f" % cop, 8.5 / cop, .716 / cop, "grid"),
             ("Heat pump on green open access", "₹5.5/kWh landed · COP %.1f" % cop, 5.5 / cop, 0.0, "green"),
             ("Heat pump in solar blocks + store", "₹4.0/kWh · COP %.1f" % cop, 4.0 / cop, 0.0, "green")]
    return [dict(name=a, sub=b, costPerKwhTh=round(c, 2), co2PerKwhTh=round(d, 3), kind=k) for a, b, c, d, k in rows]


def deck(ind):
    ex = ind["exec"]
    short = ind["short"]
    d = {
        "slug": ind["slug"], "short": short,
        "meta": {"title": "jouleWise · Decarbonisation stack · %s" % short, "description": ind["cover_p"]},
        "cover": {
            "eyebrow": "%s / power · heat · proof" % short,
            "titleHtml": 'Green power.<br>Green heat.<br><span class="g">One stack.</span>',
            "sub": ind["cover_h2"], "lede": ind["cover_p"],
            "stats": [["4", "layers · power, heat, data, ESG"], ["120 °C", "heat pump range · hot water and steam"],
                      ["15-min", "metered heartbeat on ergOS"], ["1", "accountable provider"]],
        },
        "execSummary": {
            "titleHtml": ex["headline"],
            "rows": [
                ["The situation", ex["situation"]],
                ["The gap", "Power, heat and ESG reporting are bought from different vendors on different clocks. Solar is sized without the heat load; boilers are replaced without a plan for cheaper power; ESG data is typed in once a year. Each fix leaves money and carbon on the table."],
                ["What we do", "jouleWise runs the whole decarbonisation stack: <b>green power</b> — intrastate and ISTS solar and wind, rooftop solar, BESS and green-market purchase, each source orchestrated to fulfil industrial demand at least cost; <b>ABT metering and data loggers</b> on every source and load; <b>green heat</b> from industrial heat pumps up to 120 °C; <b>ergOS</b> to meter and orchestrate both every 15 minutes; <b>esgOS</b> to turn the same data into audit-ready disclosure."],
                ["Why it compounds", "Cheaper green power lowers the cost of every unit of heat a heat pump makes. Thermal storage lets that heat be made in the cheapest solar blocks. ergOS proves it; esgOS reports it. Savings from one layer fund the next."],
                ["The value", ex["value"]],
                ["How to engage", "Four models, mix and match: <b>Advisory</b>, <b>SaaS</b> (ergOS + esgOS), <b>Heat Advisory</b>, and <b>Heat as a Service</b>, where you pay per unit of heat and invest nothing upfront."],
                ["First step", ex["first"]],
            ],
            "outcomes": [["up to 25%", "cost savings on DISCOM tariff"], ["up to 65%", "renewable share achieved"]],
            "note": "Reported client impact, year 1 of ergOS; C&I client outcomes. Results vary with state, tariff structure and load profile. %s-specific value is quantified in the baseline." % short,
        },
        "whyNow": {"titleHtml": ind["why_h"], "lede": ind["why_p"],
                   "drivers": [{"icon": i, "title": t, "text": x} for i, t, x in ind["drivers"]]},
        "stack": {
            "titleHtml": 'One stack.<br><span class="g">Every layer feeds the next.</span>',
            "lede": "Most plants buy decarbonisation in pieces. We built it as a loop: low-cost green power feeds heat pumps, storage moves heat into the cheapest blocks, ergOS runs it, esgOS proves it.",
            "items": [{"layer": l, "title": t, "text": x} for l, t, x in [
                ("power", "Green power", GP),
                ("heat", "Heat pumps", "Every kWh in becomes three to four kWh of useful heat. The boiler stops burning fuel for loads up to 120 °C."),
                ("heat", "Thermal storage", "Heat is made when power is cheapest and greenest, and used when the process needs it."),
                ("data", "ergOS", "Meters power, steam, fuel and water every 15 minutes; forecasts, schedules and trades; runs heat pumps against price."),
                ("esg", "esgOS", "Converts the same metered data to Scope 1, 2 and 3, BRSR Core-format, CBAM, CDP and customer disclosures.")]],
            "calloutHtml": "<b>Why the order matters.</b> A heat pump on grid power cuts fuel cost but, at today's grid emission factor, barely cuts carbon against gas. Put the same heat pump on green power and its heat is close to zero-carbon. Power first, then heat — from one provider.",
        },
        "supplyChain": {"eyebrow": ind["chain_eb"], "titleHtml": ind["chain_h"], "lede": ind["chain_p"],
                        "points": [{"n": n, "layer": l, "tag": LAYER_TAG[l], "title": t, "text": x} for n, l, t, x in ind["marks"]],
                        "note": "Illustrative plant. Actual intervention map built site by site in the baseline."},
        "power": {
            "titleHtml": 'Low-cost<br><span class="g">green power.</span>', "lede": ind["power_p"],
            "calloutHtml": "<b>Every source, one dispatch.</b> " + GP,
            "steps": [{"title": a, "text": b, "outcome": c} for a, b, c in [
                ("Plan", "Meter-data due diligence: bills, load survey, rooftop and captive parameters. Solar, wind, hybrid, BESS and exchange power optimised together, capex or opex, with each state's ToD, banking and open access charges in the landed-cost model.", "RE-100 roadmap · size, location, savings, NPV"),
                ("Implement", "RfP over a 25-year horizon, developer evaluation, reverse auction, PPA and shareholder agreements (26% SPV equity for captive status), open access approvals and connection agreement.", "Green power contracted · ~3 months once planning closes"),
                ("Meter and log", "ABT meters at injection and drawal points — main and check meters on CTs and PTs of the required accuracy class — plus data loggers on every incomer, heat pump, steam, fuel and water line. Installed, tested, sealed and linked to the SLDC and to ergOS.", "Every source and load visible in 15-minute blocks"),
                ("Orchestrate", "ergOS forecasts 96 blocks, schedules with the SLDC, trades DAM, GDAM, RTM and GTAM, manages banking and battery health — and now dispatches heat pumps and thermal storage against price.", "For the life of the assets")]],
        },
        "heatPump101": {
            "titleHtml": 'What is a<br><span class="h">heat pump?</span>',
            "lede": "A heat pump is a refrigerator run the other way round. It does not make heat by burning anything — it moves heat that already exists, from a cooler place to a hotter one, and uses electricity only to do the lifting.",
            "balance": [{"name": "Fuel boiler", "in": [["fuel", 1.0]], "inLabel": "1 kWh fuel", "out": 0.85, "outLabel": "0.85 kWh heat"},
                        {"name": "Heat pump", "in": [["electricity", 1.0], ["free", 2.5]], "inLabel": "1 kWh power + 2.5 free", "out": 3.5, "outLabel": "3.5 kWh heat"}],
            "copNote": "COP (coefficient of performance) = useful heat ÷ electricity. A boiler can never exceed 1; a heat pump typically delivers 2 to 5.",
            "lifts": [["~5", "30"], ["~3.5", "50"], ["~2.5", "70"], ["~2", "90"]],
            "liftNote": "Lift = delivery temperature minus source temperature. Recovering warm waste heat first and delivering no hotter than the process needs keeps the COP high.",
            "faq": [["Does it replace my boiler?", "For loads up to 120 °C, yes — as the primary heat source. The boiler usually stays on standby and for any loads above that range."],
                    ["What if power is expensive?", "Each kWh of power returns three to four kWh of heat, so heat costs roughly a third of the power price. On green open access, the carbon falls close to zero as well."],
                    ["What does the site need?", "Spare electrical capacity, space near the heat users and a steady heat demand. A hot-water store smooths peaks and lets the unit run in the cheapest blocks."],
                    ["Is it proven?", "It is the same refrigeration cycle as the chillers already on your site, run for heat. Industrial units are in service worldwide in food, chemicals, pharma and textiles."]],
        },
        "heat": {
            "titleHtml": 'The boiler,<br><span class="h">reinvented.</span>', "lede": ind["heat_p"],
            "loads": [{"name": n, "sub": s, "min": lo, "max": hi, "heatPump": hi <= 120} for n, s, lo, hi in ind["heat_loads"]],
            "cards": [{"icon": "flame", "title": "Heat sources we reuse", "text": ind["heat_src"]},
                      {"icon": "bolt", "title": ind.get("heat_dual_t", "Heating and cooling at once"), "text": ind["heat_dual"]},
                      {"icon": "chart", "title": "Sized from metered heat", "text": "Portable heat meters log flow and temperature on candidate processes for two to four weeks before anything is sized."}],
        },
        "economics": {
            "titleHtml": 'Cheaper power<br><span class="g">makes cheaper heat.</span>',
            "lede": "What one kWh of useful process heat costs, and what it emits, depending on where the heat comes from. The heat pump cuts cost on any power; green power is what cuts the carbon.",
            "rows": econ_rows(ind),
            "note": "Illustrative only, not an offer. Assumptions: PNG 10.4 kWh/SCM, 1.95 kg CO₂/SCM; HSD 10.0 kWh/L, 2.68 kg CO₂/L; grid 0.716 kg CO₂/kWh (CEA baseline order of magnitude); green power treated as zero-emission on a market basis with green attributes retired. Heat pump COP %.1f reflects %s; COP falls as delivery temperature rises. Tariffs, fuel prices and COP vary by site and are replaced with metered values in the baseline.%s" % (ind["cop"], ind["cop_note"], ind.get("extra_note", "")),
        },
        "ergos": {
            "titleHtml": 'One screen.<br><span class="g">Power and heat.</span>',
            "lede": "ergOS is the operating layer. It sits on every meter, every source and every heat pump — watching prices, weather, storage and the production plan, and acting every 15 minutes.",
            "cockpit": {"title": ind["cockpit"]["title"],
                        "tiles": [{"label": a, "valueColor": b, "value": c, "subColor": d, "sub": e} for a, b, c, d, e in ind["cockpit"]["tiles"]],
                        "ops": [{"color": a, "icon": b, "text": c} for a, b, c in ind["cockpit"]["ops"]]},
            "cards": [{"icon": "chart", "title": "Forecast and trade", "text": "96-block day-ahead load, SLDC scheduling, DAM, GDAM, RTM and GTAM bids, deviation settled block by block."},
                      {"icon": "flame", "title": "Dispatch heat", "text": "Heat pumps and thermal stores charged in the cheapest, greenest blocks, within process temperature limits."},
                      {"icon": "shield", "title": "Bill and bank", "text": "Banked-energy ledger, audit-ready billing and state-wise compliance tracked continuously."}],
        },
        "esgos": {
            "titleHtml": 'ESG, operated.<br><span class="g">Not reported.</span>',
            "lede": "The same data that runs the plant produces the disclosure. Metered where possible, integrated where the data already lives, audited where it does not.",
            "modes": [{"color": "green", "kicker": "First choice", "title": "Meter", "text": "Electricity, steam, thermal energy, fuel flow and water — every 15 minutes."},
                      {"color": "data", "kicker": "Second", "title": "Integrate", "text": "ERP, HRMS, EHS tools and portals — no retyping."},
                      {"color": "esg", "kicker": "Last resort", "title": "Audit", "text": "Refrigerant, waste, safety and supplier data — photo-evidenced and signed off."}],
            "outputsLabel": "What esgOS produces for %s" % short.lower(), "outputs": ind["esg_out"],
            "calloutHtml": "<b>Deterministic by design.</b> Regulations and methodologies are stored as versioned, machine-readable rules and run by a rule engine. AI extracts, explains and drafts — it never produces a reported number.",
        },
        "models": {
            "titleHtml": 'Four ways in.<br><span class="g">One provider.</span>',
            "lede": "Start where the value is largest for your plant. Models combine — most clients begin with Advisory and SaaS on power, then add heat.",
            "items": [{"color": c, "kicker": k, "title": t, "text": x, "rows": r} for c, k, t, x, r in [
                ("green", "Model 01", "Advisory", "Power strategy and delivery, from RE-100 roadmap to live open access.",
                 [["Scope", "RE-100 roadmap, RfP and reverse auction, PPA, approvals, ABT metering, regulatory filings"], ["You pay", "Fixed fee, with a success-fee option"], ["Assets", "Owned by you or your developer"], ["Best for", "Plants ready to contract green power"]]),
                ("data", "Model 02", "SaaS", "ergOS and esgOS as a subscription — the operating and disclosure layers.",
                 [["Scope", "15-minute metering, forecasting, trading support, heat dispatch, ESG pipeline and reports"], ["You pay", "Per plant, per year"], ["Assets", "Meters per BOQ; platform hosted"], ["Best for", "Multi-plant groups that want one source of truth"]]),
                ("heat", "Model 03", "Heat Advisory", "Engineering-grade route from boiler to heat pump, with you owning the asset.",
                 [["Scope", "Heat audit and metering, pinch and waste-heat study, heat pump sizing, vendor selection, EPC oversight, commissioning"], ["You pay", "Fixed fee per study and per project stage"], ["Assets", "Owned by you (capex)"], ["Best for", "Plants with capex budget and a fuel-cost target"]]),
                ("heat", "Model 04", "Heat as a Service", "You buy heat, not equipment. Hot water and low-pressure steam delivered to your header.",
                 [["Scope", "Design, install, own, operate and maintain heat pumps and storage; powered by jouleWise green power; run on ergOS"], ["You pay", "Per unit of heat delivered, priced against your current fuel cost"], ["Assets", "Owned on the jouleWise side — zero upfront capex"], ["Best for", "Plants that want green steam now, off balance sheet"]])]],
            "note": "Commercial terms indicative and finalised per engagement.",
        },
        "roadmap": {
            "titleHtml": 'Baseline.<br>Power. Heat.<br><span class="g">Proof.</span>',
            "steps": [{"title": a, "when": w, "text": b, "outcome": c} for a, w, b, c in [
                ("Baseline", "Weeks 1–4", "Bills, load survey, fuel and steam records, portable heat metering on candidate processes, ESG data map.", "Signed-off energy, heat and carbon baseline"),
                ("Roadmap", "Weeks 4–8", ind["roadmap2"], "One business case — power, heat, ESG"),
                ("Meter and log", "Weeks 6–12", "ABT metering at the incomer and data loggers on power, heat, fuel and water lines — the measured base every later step is sized, settled and reported on.", "ergOS live on metered data"),
                ("Power live", "~3 months after roadmap", "Open access contracted and approved; rooftop solar and BESS where they fit; every source orchestrated against demand on ergOS.", "Green power flowing"),
                ("Heat live", "Pilot, then scale", ind["roadmap4"], "Fuel displaced, measured on ergOS"),
                ("Operate and disclose", "Every block · every year", "ergOS runs power and heat; esgOS publishes BRSR Core-format, CBAM, CDP and customer disclosures with an audit trail.", "Assurance-ready numbers")]],
            "note": "Timelines indicative; confirmed after the baseline and dependent on state approvals and equipment lead times.",
        },
        "trackRecord": {
            "titleHtml": "~1 GW of<br>RE-100 study scope.",
            "lede": "RE-100 assignments across eight industrial groups, cement to FMCG. Deep Indian power-sector regulatory work, with team experience on lender's-engineer mandates.",
            "clients": [["Dalmia Cement", "Cement", "~300 MW"], ["Chettinad Cement", "Cement", "~200 MW"], ["SAEL", "Solar cells", "~160 MW"],
                        ["Wonder Cement", "Cement", "~140 MW"], ["Haldiram's", "Snacks & beverages", "~35 MW"], ["Bikaji", "Snacks", "~25 MW"],
                        ["Bharatiyam (Campa)", "Beverages", "~19 MW"]],
            "stats": [["1 GW+", "RE project work by our team"], ["15+", "state regulatory jurisdictions"], ["8", "industries served"], ["20+", "years of leadership in energy"]],
            "note": "Industries: food & beverages, FMCG, cement, chemicals, textiles, metals, automotive ancillary, solar manufacturing, real estate. ISO 9001:2015 · ISO 27001.",
        },
        "contact": {
            "titleHtml": 'Tell us the plant.<br><span class="g">We\'ll map the stack.</span>',
            "lede": "Send one year of electricity bills and fuel records. We return the baseline, the power-and-heat roadmap and the business case.",
            "people": [{"area": "Electricity", "color": "green", "name": "Praveen Sharma", "email": "praveen.sharma@joulewise.com", "phone": "+91 92143 37500"},
                       {"area": "Heat", "color": "heat", "name": "Gautam Prasad", "email": "gautam.prasad@joulewise.com", "phone": None}],
            "company": {"site": "joulewise.com", "legal": "jouleWise Advisory Services Pvt Ltd · Noida, India · Spain · ISO 9001:2015 · ISO 27001"},
            "disclaimer": "This presentation is issued for discussion purposes only. Prices, durations, heat pump performance and outcomes shown are indicative, depend on site, state, load profile, process temperatures, contracted terms, exchange prices and the regulatory orders in force, and do not constitute an offer, warranty or commitment by jouleWise. Screens and plant illustrations are illustrative. Client names are cited from jouleWise assignments. Any engagement is governed solely by definitive agreements between the parties.",
        },
        "svg": {"coverStack": scenes.cover_stack(), "loop": loop_svg(), "cycle": hp101.cycle_svg(),
                "scene": getattr(scenes, ind["scene"])(), "dayChart": day_chart(ind)},
    }
    s = json.dumps(d, ensure_ascii=False, indent=1)
    for a, b in ind.get("subs", []):
        s = s.replace(a, b)
    return s


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "content", "decks")
    os.makedirs(out, exist_ok=True)
    for ind in industries.ALL:
        open(os.path.join(out, ind["slug"] + ".json"), "w").write(deck(ind) + "\n")
        print("wrote", ind["slug"])
