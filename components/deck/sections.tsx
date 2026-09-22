import type { DeckData } from "@/lib/types";
import { Art, Card, Eyebrow, Legend, Rich, Stats, layerClass, pad2, swatch } from "./ui";

type S = { d: DeckData };

export function Cover({ d }: S) {
  const c = d.cover;
  const [lead, ...rest] = c.eyebrow.split(" / ");
  return (
    <>
      <Eyebrow lead={lead} rest={rest.join(" / ")} />
      <Rich as="h1" html={c.titleHtml} />
      <p className="sub">{c.sub}</p>
      <p className="lede">{c.lede}</p>
      <Art svg={d.svg.coverStack} />
      <Stats items={c.stats} />
    </>
  );
}

export function ExecSummary({ d }: S) {
  const e = d.execSummary;
  return (
    <>
      <Eyebrow lead="Executive summary" rest={d.short} />
      <Rich as="h2" html={e.titleHtml} />
      <div className="rows">
        {e.rows.map(([k, v]) => (
          <div className="row" key={k}><div className="lab">{k}</div><Rich as="p" html={v} /></div>
        ))}
      </div>
      <div className="big2">
        {e.outcomes.map(([v, l]) => (
          <div className="card" key={l}><b>{v}</b><span className="lab">{l}</span></div>
        ))}
      </div>
      <p className="note">{e.note}</p>
    </>
  );
}

export function WhyNow({ d }: S) {
  const w = d.whyNow;
  return (
    <>
      <Eyebrow lead="Why now" rest={d.short} />
      <Rich as="h2" html={w.titleHtml} />
      <p className="lede">{w.lede}</p>
      <div className="grid2">{w.drivers.map((x) => <Card key={x.title} {...x} />)}</div>
    </>
  );
}

function Points({ items }: { items: { n: number; layer: DeckData["stack"]["items"][number]["layer"]; title: string; text: string; tag?: string }[] }) {
  return (
    <div className="pts">
      {items.map((p) => (
        <div className="pt" key={p.n}>
          <span className={`num ${layerClass(p.layer)}`}>{pad2(p.n)}</span>
          <div>
            <h4>{p.title}</h4>
            <p>{p.text}</p>
            {p.tag ? <span className={`tag ${layerClass(p.layer)}`}>{p.tag}</span> : null}
          </div>
        </div>
      ))}
    </div>
  );
}

export function Stack({ d }: S) {
  const s = d.stack;
  return (
    <>
      <Eyebrow lead="The ecosystem" rest="first of its kind" />
      <Rich as="h2" html={s.titleHtml} />
      <p className="lede">{s.lede}</p>
      <Art svg={d.svg.loop} className="fig scroll loop" />
      <Points items={s.items.map((x, i) => ({ ...x, n: i + 1 }))} />
      <Rich as="div" className="callout" html={s.calloutHtml} />
    </>
  );
}

export function SupplyChain({ d }: S) {
  const s = d.supplyChain;
  return (
    <>
      <Eyebrow lead={s.eyebrow} rest="where we intervene" />
      <Rich as="h2" html={s.titleHtml} />
      <p className="lede">{s.lede}</p>
      <Art svg={d.svg.scene} className="fig scroll" swipe="Swipe to see the whole plant" />
      <Legend items={[
        { label: "Power", style: { background: "var(--green)" } },
        { label: "Heat", style: { background: "var(--heat)" } },
        { label: "Data · ergOS", style: { background: "var(--data)" } },
        { label: "ESG · esgOS", style: { background: "var(--esg)" } },
      ]} />
      <Points items={s.points} />
      <p className="note">{s.note}</p>
    </>
  );
}

function Seq({ steps }: { steps: { title: string; text: string; outcome: string; when?: string }[] }) {
  return (
    <div className="seq">
      {steps.map((s, i) => (
        <div className="st" key={s.title}>
          <div className="n">{pad2(i + 1)}</div>
          <div>
            <h4>{s.title}{s.when ? <span className="lab" style={{ marginLeft: 8 }}>{s.when}</span> : null}</h4>
            <p>{s.text}</p>
            <div className="out">{s.outcome}</div>
          </div>
        </div>
      ))}
    </div>
  );
}

export function Power({ d }: S) {
  const p = d.power;
  return (
    <>
      <Eyebrow lead="Layer 01" rest="power" />
      <Rich as="h2" html={p.titleHtml} />
      <p className="lede">{p.lede}</p>
      <Rich as="div" className="callout" html={p.calloutHtml} />
      <Art svg={d.svg.dayChart} />
      <Legend items={[
        { label: "Wind · ISTS", style: { background: "#1f7a55" } },
        { label: "Solar", style: { background: "#3dd68c" } },
        { label: "BESS", style: { background: "#5b8def" } },
        { label: "Green market", style: { background: "#8fd9b6", opacity: 0.5 } },
        { label: "Heat pump load", style: { border: "1px solid #f2994a", background: "rgba(242,153,74,.25)" } },
      ]} />
      <Seq steps={p.steps} />
    </>
  );
}

const BAL_COLOR: Record<string, string> = { fuel: "#5d666c", electricity: "#3dd68c", free: "#5b8def" };

export function HeatPump101({ d }: S) {
  const h = d.heatPump101;
  const max = 3.5;
  return (
    <>
      <Eyebrow lead="Heat pump 101" rest="the question clients ask most" color="var(--heat)" />
      <Rich as="h2" html={h.titleHtml} />
      <p className="lede">{h.lede}</p>
      <Art svg={d.svg.cycle} className="fig scroll cyc" swipe="Swipe to see the whole cycle" />
      <p className="lab" style={{ marginTop: 30 }}>What goes in, what comes out</p>
      <div className="bal">
        {h.balance.map((b) => (
          <div className="brow" key={b.name}>
            <div className="bn">{b.name}</div>
            <div className="bb">
              <div className="bt">{b.in.map(([k, v]) => <span key={k} style={{ width: `${(100 * v) / max}%`, background: BAL_COLOR[k] }} />)}</div>
              <small>in · {b.inLabel}</small>
              <div className="bt"><span style={{ width: `${(100 * b.out) / max}%`, background: "#f2994a" }} /></div>
              <small className="c-heat">out · {b.outLabel}</small>
            </div>
          </div>
        ))}
      </div>
      <p className="note">{h.copNote}</p>
      <p className="lab" style={{ marginTop: 30 }}>Temperature lift sets the COP · indicative</p>
      <div className="lifts">
        {h.lifts.map(([cop, lift]) => <div key={lift}><b>{cop}</b><span className="lab">COP at {lift} K lift</span></div>)}
      </div>
      <p className="note">{h.liftNote}</p>
      <div className="rows">
        {h.faq.map(([q, a]) => <div className="row" key={q}><div className="lab">{q}</div><p>{a}</p></div>)}
      </div>
    </>
  );
}

export function Heat({ d }: S) {
  const h = d.heat;
  const ticks: [string, number, boolean?][] = [["0 °C", 0], ["50", 25], ["100", 50], ["120", 60, true], ["150", 75], ["200 °C", 100]];
  return (
    <>
      <Eyebrow lead="Layer 02" rest="heat" />
      <Rich as="h2" html={h.titleHtml} />
      <p className="lede">{h.lede}</p>
      <div className="ladder">
        {h.loads.map((l) => (
          <div className="lrow" key={l.name}>
            <div className="nm">{l.name}<small>{l.sub}</small></div>
            <div className="track">
              <span className="rg" style={{ left: `${l.min / 2}%`, width: `${Math.max((Math.min(l.max, 200) - l.min) / 2, 1.2)}%`, background: l.heatPump ? "var(--heat)" : "#5d666c" }} />
              <span className="cap" style={{ left: "60%" }} />
            </div>
          </div>
        ))}
      </div>
      <div className="scale">
        <div />
        <div>{ticks.map(([t, x, hot]) => <span key={t} className={hot ? "c-heat" : undefined} style={{ left: `${x}%` }}>{t}</span>)}</div>
      </div>
      <Legend items={[
        { label: "Heat pump range", style: { background: "var(--heat)" } },
        { label: "Stays on existing burners or electrode heat", style: { background: "#5d666c" } },
        { label: "120 °C ceiling", style: { borderLeft: "2px dashed var(--heat)" } },
      ]} />
      <div className="grid3">{h.cards.map((c) => <Card key={c.title} {...c} />)}</div>
    </>
  );
}

const ECON_COLOR = { fuel: "#5d666c", grid: "#f2994a", green: "#3dd68c" } as const;

export function Economics({ d }: S) {
  const e = d.economics;
  const mc = Math.max(...e.rows.map((r) => r.costPerKwhTh));
  const me = Math.max(...e.rows.map((r) => r.co2PerKwhTh));
  return (
    <>
      <Eyebrow lead="The loop in numbers" rest="illustrative" />
      <Rich as="h2" html={e.titleHtml} />
      <p className="lede">{e.lede}</p>
      <div className="econ">
        <div className="ehead"><div className="lab">Source of heat</div><div className="lab">₹ per kWh of useful heat</div><div className="lab" style={{ textAlign: "right" }}>₹/kWh-th</div></div>
        {e.rows.map((r) => (
          <div className="erow" key={r.name}>
            <div className="nm">{r.name}<small>{r.sub}</small></div>
            <div className="ebar"><i style={{ width: `${(100 * r.costPerKwhTh) / mc}%`, background: ECON_COLOR[r.kind] }} /></div>
            <div className="v">{r.costPerKwhTh.toFixed(2)}</div>
          </div>
        ))}
      </div>
      <div className="econ">
        <div className="ehead"><div className="lab">Source of heat</div><div className="lab">kg CO₂ per kWh of useful heat</div><div className="lab" style={{ textAlign: "right" }}>kg/kWh-th</div></div>
        {e.rows.map((r) => (
          <div className="erow" key={r.name}>
            <div className="nm">{r.name}</div>
            <div className="ebar"><i style={{ width: `${Math.max((100 * r.co2PerKwhTh) / me, 0.6)}%`, background: ECON_COLOR[r.kind], opacity: 0.75 }} /></div>
            <div className="v">{r.co2PerKwhTh ? r.co2PerKwhTh.toFixed(2) : "≈ 0"}</div>
          </div>
        ))}
      </div>
      <p className="note">{e.note}</p>
    </>
  );
}

export function Ergos({ d }: S) {
  const g = d.ergos;
  const c = g.cockpit;
  return (
    <>
      <Eyebrow lead="Layer 03" rest="data · ergOS" />
      <Rich as="h2" html={g.titleHtml} />
      <p className="lede">{g.lede}</p>
      <div className="cock">
        <div className="cock-h"><span>ergOS · {c.title}</span><b>● Live</b></div>
        <div className="tiles">
          {c.tiles.map((t) => (
            <div className="tile" key={t.label}>
              <small style={{ color: "var(--mute)" }}>{t.label}</small>
              <b style={{ color: t.valueColor }}>{t.value}</b>
              <small style={{ color: t.subColor }}>{t.sub}</small>
            </div>
          ))}
        </div>
        <div className="ops">
          {c.ops.map((o) => <div className="op" key={o.text}><i style={{ color: o.color }}>{o.icon}</i><span>{o.text}</span></div>)}
        </div>
        <div className="cock-f">Illustrative screen · values indicative</div>
      </div>
      <div className="grid3">{g.cards.map((x) => <Card key={x.title} {...x} />)}</div>
    </>
  );
}

export function Esgos({ d }: S) {
  const e = d.esgos;
  return (
    <>
      <Eyebrow lead="Layer 04" rest="ESG · esgOS" />
      <Rich as="h2" html={e.titleHtml} />
      <p className="lede">{e.lede}</p>
      <div className="grid3">
        {e.modes.map((m) => (
          <div className="card" key={m.title} style={{ borderTop: `3px solid ${swatch(m.color)}` }}>
            <div className="lab" style={{ color: swatch(m.color) }}>{m.kicker}</div>
            <h3>{m.title}</h3>
            <p>{m.text}</p>
          </div>
        ))}
      </div>
      <p className="lab" style={{ marginTop: 30 }}>{e.outputsLabel}</p>
      <ul className="chk">{e.outputs.map((o) => <li key={o}>{o}</li>)}</ul>
      <Rich as="div" className="callout" html={e.calloutHtml} />
    </>
  );
}

export function Models({ d }: S) {
  const m = d.models;
  return (
    <>
      <Eyebrow lead="Working models" rest="how to engage" />
      <Rich as="h2" html={m.titleHtml} />
      <p className="lede">{m.lede}</p>
      <div className="models">
        {m.items.map((x) => (
          <div className="model" key={x.title} style={{ ["--c" as string]: swatch(x.color) }}>
            <div className="k">{x.kicker}</div>
            <h3>{x.title}</h3>
            <p>{x.text}</p>
            <dl>{x.rows.map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}</dl>
          </div>
        ))}
      </div>
      <p className="note">{m.note}</p>
    </>
  );
}

export function Roadmap({ d }: S) {
  const r = d.roadmap;
  return (
    <>
      <Eyebrow lead="The roadmap" rest="indicative" />
      <Rich as="h2" html={r.titleHtml} />
      <Seq steps={r.steps} />
      <p className="note">{r.note}</p>
    </>
  );
}

export function TrackRecord({ d }: S) {
  const t = d.trackRecord;
  return (
    <>
      <Eyebrow lead="Track record" rest="RE-100 assignments" />
      <Rich as="h2" html={t.titleHtml} />
      <p className="lede">{t.lede}</p>
      <table className="tbl">
        <thead><tr><th>Client</th><th>Industry</th><th>RE study scope</th></tr></thead>
        <tbody>{t.clients.map(([a, b, c]) => <tr key={a}><td>{a}</td><td>{b}</td><td className="m">{c}</td></tr>)}</tbody>
      </table>
      <Stats items={t.stats} />
      <p className="note">{t.note}</p>
    </>
  );
}

export function Contact({ d }: S) {
  const c = d.contact;
  return (
    <>
      <Eyebrow lead="Let's talk" rest="start with one plant" />
      <Rich as="h2" html={c.titleHtml} />
      <p className="lede">{c.lede}</p>
      <div className="contact">
        {c.people.map((p) => (
          <div className="row" key={p.email}>
            <div className="lab" style={{ color: swatch(p.color) }}>{p.area}</div>
            <p>
              <b>{p.name}</b><br />
              <a href={`mailto:${p.email}`}>{p.email}</a>
              {p.phone ? <> · <a href={`tel:${p.phone.replace(/\s/g, "")}`}>{p.phone}</a></> : null}
            </p>
          </div>
        ))}
        <div className="row">
          <div className="lab">jouleWise</div>
          <p>{c.company.site}<br /><span style={{ color: "var(--mute)" }}>{c.company.legal}</span></p>
        </div>
      </div>
      <div className="disc"><div className="lab">Disclaimer</div><p>{c.disclaimer}</p></div>
    </>
  );
}
