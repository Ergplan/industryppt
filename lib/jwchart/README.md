# jwchart

Small, dependency-free SVG charts that render to a **string**.

Built for decks and documents where a chart should sit *on* the page rather than
inside a boxed widget: no frame, no background, translucent fills, labels on
leader lines. It has no build step, no runtime dependency and no framework
opinion — copy the folder into any project.

## Why a string?

`renderDonut(options)` is a pure function returning SVG markup. That means:

- it runs in Node, in a build script, in a server component, or in the browser
- the page is complete before any JavaScript loads — charts survive JS being off,
  print, and email clients
- interaction is layered on afterwards with `enhance()`, and is entirely optional

## Use

### Anywhere (string)

```js
import { renderDonut } from "./lib/jwchart/index.js";

const svg = renderDonut({
  data: [
    { label: "Wind", value: 632, color: "#1f7a55" },
    { label: "Solar", value: 735, color: "#3dd68c" },
    { label: "Storage", value: 104, color: "#5b8def" },
  ],
  unit: "kWh",
  centerCaption: "green supply in a day",
});
```

Include `jwchart.css` once, then drop `svg` into your template.

### React (server or client)

```jsx
import { renderDonut } from "@/lib/jwchart";
<div dangerouslySetInnerHTML={{ __html: renderDonut({ data }) }} />
```

Call `enhance(el)` from a `useEffect` in a client component to add hover.

### Plain DOM, one step

```js
import { mountDonut } from "./lib/jwchart/index.js";
const teardown = mountDonut("#mix", { data, unit: "kWh" });
```

### From another language

Because rendering is pure, a non-JS generator can shell out once per build:

```bash
echo '{"data":[{"label":"Wind","value":632}]}' | node render-donut.mjs
```

That is how this repo's Python deck generator draws the same chart as the site —
one implementation, two renderers. See `tools/generator/render-chart.mjs`.

## Interaction

`enhance(root)` wires every `[data-jwc]` figure inside `root` and returns a
teardown function. Hovering or focusing a slice lifts it, dims the others and
turns the middle of the ring into the readout. Slices, legend entries and leader
labels are all live and all point at the same slice.

Keyboard: `Tab` to a slice, arrows to move between slices, `Enter`/`Space` to
pin, `Escape` to release.

If you re-render a chart as its data changes — following a cursor, say — pass
`animate: false`, or the entrance animation restarts on every render and the
chart never becomes fully opaque.

## Theming

Everything is a `--jwc-*` custom property with a working default. Override on the
figure or any ancestor:

```css
.jwc {
  --jwc-ink: #111;
  --jwc-muted: #667;
  --jwc-font: "Söhne", sans-serif;
  --jwc-fill: .2;        /* slice fill opacity at rest */
  --jwc-lift: 0;         /* disable the hover lift */
}
```

Per-slice colour comes from `color` on the datum, or the `colors` array, or the
built-in `PALETTE`.

## Accessibility

- the chart is one `role="img"` with a `<title>` and a `<desc>` listing every share
- each slice is a focusable `listitem` with its own label, value and percentage
- a `<title>` per slice gives the native tooltip when JavaScript is absent
- `prefers-reduced-motion` removes the entrance animation and the hover lift

## API

| Export | Purpose |
| --- | --- |
| `renderDonut(options)` | donut or pie (`thickness: 1`) as an SVG string |
| `enhance(root?)` | add interaction to rendered charts; returns teardown |
| `mountDonut(target, options)` | render + enhance into an element |
| `series`, `arcPath`, `polar`, `compact`, `pct`, `num`, `tag`, `esc`, `uid`, `PALETTE` | building blocks for new chart types |

Options are documented in `index.d.ts`.

## Adding a chart type

1. Write `renderX(options)` in `x.js` returning a string; use `tag()` and the
   geometry helpers from `core.js`.
2. Mark the wrapper `data-jwc="x"`.
3. Register a `wireX(fig, off)` in the `TYPES` map in `index.js` if it needs
   interaction.
4. Add its styles to `jwchart.css` using the existing tokens.
