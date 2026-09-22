# jouleWise — industry decarbonisation decks (Next.js section)

Five industry decks — **automotive, pharma, textile, hotels, beverages** — built as one reusable
Next.js section. Same 15-page structure for every industry; the content, plant illustration,
heat-load ladder, cockpit screen and disclosures change per industry.

| Route | What it is |
|---|---|
| `/industries` | Index of the five decks |
| `/industries/[slug]` | One deck, statically generated (`automotive`, `pharma`, `textile`, `hotels`, `beverages`) |
| `/standalone/joulewise-<slug>.html` | Self-contained HTML versions (share as a file or link) |

## Run

```bash
npm install
npm run dev        # http://localhost:3000/industries
npm run build      # all five pages are pre-rendered (generateStaticParams)
```

Next.js 15 (App Router) · React 19 · TypeScript. No other runtime dependencies.

## Structure

```
app/
  layout.tsx                 fonts (Inter Tight, IBM Plex Mono via next/font) + CSS import
  industries/page.tsx        index
  industries/[slug]/page.tsx deck page + metadata
components/deck/
  Deck.tsx                   page order, header labels — reorder or drop pages here
  sections.tsx               one component per page (Cover, ExecSummary … Contact)
  ui.tsx                     shared primitives (Page frame, Rich text, inline Art, icons)
  DeckBar.tsx                sticky bar with scroll progress (client component, optional)
content/decks/<slug>.json    ALL copy, numbers and SVG artwork for each industry
lib/types.ts                 schema of the JSON
lib/decks.ts                 loader: decks, deckSlugs, getDeck()
styles/jw-deck.css           all styles, scoped under .jw-deck (won't leak into the site)
tools/generator/             Python that draws the isometric plants/charts and exports the JSON
public/standalone/           standalone HTML decks
```

## Merging into the main website

1. Copy `components/deck`, `lib`, `content/decks`, `styles/jw-deck.css` and `app/industries`.
2. In the site's root layout, import `@/styles/jw-deck.css` and add the two font variables
   (`--font-inter-tight`, `--font-plex-mono`) as in `app/layout.tsx`. Without them the deck falls back to
   Helvetica/Arial and system mono.
3. If the site has its own sticky header, either render `<Deck deck={d} showBar={false} />` or keep the
   bar and set `--jw-top-offset` on `.jw-deck` to your header height so the bar sits below it.
4. Requires the `@/*` path alias (see `tsconfig.json`).

## Editing content

- **Copy / numbers:** edit `content/decks/<slug>.json` directly. Fields ending in `Html` accept only
  `<b>`, `<br>` and `<span class="g">` (green) / `<span class="h">` (heat orange).
- **Contacts:** `contact.people` in each JSON (electricity: Praveen Sharma; heat: Gautam Prasad).
- **Illustrations and charts** (`svg.*` in the JSON) are generated. To change a plant drawing, edit
  `tools/generator/scenes.py`, then regenerate:

```bash
npm run decks:export       # python3 — rewrites content/decks/*.json (overwrites manual JSON edits)
npm run decks:standalone   # rewrites public/standalone/*.html
```

  The generator's copy lives in `tools/generator/industries.py` and `export.py`. If you edit copy in
  the JSON by hand, make the same edit in the generator before re-exporting, or it will be overwritten.

## Notes

- Heat-cost figures, cockpit screens and plant drawings are illustrative and labelled as such in the pages.
- Animations (energy flows, turbine rotors) respect `prefers-reduced-motion`.
- Mobile: wide diagrams scroll sideways inside their own container; the page never scrolls sideways.
