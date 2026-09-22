import type { DeckData } from "@/lib/types";
import { DeckBar } from "./DeckBar";
import { Page } from "./ui";
import * as S from "./sections";

/** Page order, header labels and section components. Edit here to reorder or drop pages. */
const PAGES: [string, string, (p: { d: DeckData }) => React.ReactNode][] = [
  ["Executive summary", "For leadership", S.ExecSummary],
  ["Why now", "Pressures on the plant", S.WhyNow],
  ["The stack", "Power → heat → data → ESG", S.Stack],
  ["Supply chain", "Intervention map", S.SupplyChain],
  ["Power", "Plan · implement · meter · orchestrate", S.Power],
  ["Heat pump 101", "What is a heat pump", S.HeatPump101],
  ["Heat", "Industrial heat pumps", S.Heat],
  ["Economics", "Cost and carbon per unit of heat", S.Economics],
  ["ergOS", "Orchestration", S.Ergos],
  ["esgOS", "Disclosure", S.Esgos],
  ["Models", "Advisory · SaaS · Heat", S.Models],
  ["Roadmap", "From baseline to proof", S.Roadmap],
  ["Track record", "Clients", S.TrackRecord],
  ["Contact", "Let's talk", S.Contact],
];

export function Deck({ deck, showBar = true }: { deck: DeckData; showBar?: boolean }) {
  const total = PAGES.length;
  return (
    <div className="jw-deck">
      {showBar ? <DeckBar short={deck.short} total={total} /> : null}
      <main>
        <section className="pg cover" id="p00" aria-label="Cover">
          <S.Cover d={deck} />
          <div className="ft"><span>joulewise.com</span><span>For discussion purposes only</span></div>
        </section>
        {PAGES.map(([left, right, Section], i) => (
          <Page key={left} n={i + 1} total={total} left={left} right={right} short={deck.short}>
            <Section d={deck} />
          </Page>
        ))}
      </main>
    </div>
  );
}
