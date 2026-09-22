/** jwchart core — SVG string building, arc geometry and number formatting.
 *
 *  No dependencies, no framework, no DOM required: every render* function returns
 *  a string, so charts can be produced on a server, at build time, or in a browser.
 *  Nothing in this folder knows anything about the project using it.
 */

/* ------------------------------------------------------------------ escaping */

var ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };

/** Escape text destined for SVG/HTML markup. */
export function esc(v) {
  return String(v == null ? "" : v).replace(/[&<>"']/g, function (c) { return ESC[c]; });
}

/** Build an element string from a tag, an attribute map and optional children. */
export function tag(name, attrs, children) {
  var out = "<" + name;
  for (var k in attrs) {
    if (!Object.prototype.hasOwnProperty.call(attrs, k)) continue;
    var v = attrs[k];
    if (v === null || v === undefined || v === false) continue;
    out += " " + k + '="' + esc(v) + '"';
  }
  // Always an explicit closing tag: `<i/>` is XML, and an HTML parser reads it as an
  // *open* <i> that swallows everything after it. Valid in SVG too, so one rule serves both.
  return out + ">" + (children == null ? "" : children) + "</" + name + ">";
}

/* ------------------------------------------------------------------ numbers */

/** Round to `dp` decimals and drop trailing zeros: 3.50 -> "3.5", 3.00 -> "3". */
export function num(v, dp) {
  if (!isFinite(v)) return "0";
  var s = Number(v).toFixed(dp === undefined ? 1 : dp);
  return s.indexOf(".") < 0 ? s : s.replace(/\.?0+$/, "");
}

/** Short human form for axis and label use: 1234 -> "1.2k", 2400000 -> "2.4M". */
export function compact(v, dp) {
  var a = Math.abs(v);
  if (a >= 1e9) return num(v / 1e9, dp === undefined ? 1 : dp) + "B";
  if (a >= 1e6) return num(v / 1e6, dp === undefined ? 1 : dp) + "M";
  if (a >= 1e3) return num(v / 1e3, dp === undefined ? 1 : dp) + "k";
  return num(v, a < 10 ? 1 : 0);
}

/** Percentage of a total, guarded against a zero total. */
export function pct(v, total, dp) {
  return total ? num((100 * v) / total, dp === undefined ? 0 : dp) + "%" : "0%";
}

/* ----------------------------------------------------------------- geometry */

var TAU = Math.PI * 2;

/** Point on a circle. Angles are turns clockwise from 12 o'clock, so 0.25 is 3 o'clock. */
export function polar(cx, cy, r, turn) {
  var a = turn * TAU - Math.PI / 2;
  return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
}

function fmt(n) { return Math.round(n * 1000) / 1000; }

/**
 * Path for an annular sector (a donut slice); pass innerR 0 for a solid pie slice.
 * A full ring is drawn as two arcs because SVG cannot close a 360° arc in one.
 */
export function arcPath(cx, cy, innerR, outerR, from, to) {
  var span = to - from;
  if (span <= 0) return "";
  if (span >= 1) {                                   // full circle: two half arcs
    var o = outerR, i = innerR;
    var p = "M" + fmt(cx - o) + "," + fmt(cy) +
            "A" + o + "," + o + " 0 1 1 " + fmt(cx + o) + "," + fmt(cy) +
            "A" + o + "," + o + " 0 1 1 " + fmt(cx - o) + "," + fmt(cy) + "Z";
    if (!i) return p;
    return p + "M" + fmt(cx - i) + "," + fmt(cy) +
           "A" + i + "," + i + " 0 1 0 " + fmt(cx + i) + "," + fmt(cy) +
           "A" + i + "," + i + " 0 1 0 " + fmt(cx - i) + "," + fmt(cy) + "Z";
  }
  var large = span > 0.5 ? 1 : 0;
  var a = polar(cx, cy, outerR, from), b = polar(cx, cy, outerR, to);
  var d = "M" + fmt(a[0]) + "," + fmt(a[1]) +
          "A" + outerR + "," + outerR + " 0 " + large + " 1 " + fmt(b[0]) + "," + fmt(b[1]);
  if (!innerR) return d + "L" + fmt(cx) + "," + fmt(cy) + "Z";
  var c = polar(cx, cy, innerR, to), e = polar(cx, cy, innerR, from);
  return d + "L" + fmt(c[0]) + "," + fmt(c[1]) +
         "A" + innerR + "," + innerR + " 0 " + large + " 0 " + fmt(e[0]) + "," + fmt(e[1]) + "Z";
}

/* ------------------------------------------------------------------ palette */

/** Default categorical palette — distinguishable on dark and light backgrounds.
 *  Override per chart with `colors`, or per slice with `color` on the datum. */
export var PALETTE = ["#3dd68c", "#5b8def", "#f2994a", "#c9a43a", "#a78bfa", "#e0604a", "#4bc6c0", "#8b949a"];

/** Normalise input rows to {label, value, color, meta} and drop anything unusable. */
export function series(data, colors) {
  var pal = colors && colors.length ? colors : PALETTE;
  return (data || [])
    .map(function (d, i) {
      var v = typeof d === "number" ? d : Number(d.value);
      return {
        label: typeof d === "number" ? "Series " + (i + 1) : String(d.label == null ? "" : d.label),
        value: isFinite(v) ? v : 0,
        color: (d && d.color) || pal[i % pal.length],
        note: (d && d.note) || null,
      };
    })
    .filter(function (d) { return d.value > 0; });
}

/**
 * A stable id for filter/label references, derived from `key` rather than from a
 * counter or a random number. Two renders of the same chart produce the same ids,
 * which is what lets a server-rendered chart hydrate on the client without a mismatch.
 */
export function uid(prefix, key) {
  var h = 2166136261;                       // FNV-1a over the key
  var str = String(key == null ? "" : key);
  for (var i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
  }
  return (prefix || "jwc") + "-" + h.toString(36);
}
