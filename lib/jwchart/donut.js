/** jwchart donut/pie — a frameless, translucent ring that sits on the page
 *  rather than inside a panel.  Returns markup as a string; see enhance() in
 *  index.js for the optional hover behaviour. */

import { arcPath, compact, esc, num, pct, polar, series, tag, uid } from "./core.js";

var DEF = {
  size: 720,          // viewBox width
  height: 380,        // viewBox height
  thickness: 0.34,    // ring width as a fraction of the outer radius
  gap: 1.4,           // degrees of breathing room between slices
  radius: 0,          // 0 = derive from the box
  labels: true,       // leader-line labels around the ring
  legend: true,       // value list underneath
  unit: "",
  decimals: 0,
  centerCaption: "",
  centerValue: null,  // defaults to the formatted total
  transparent: true,
  animate: true,      // false for a chart re-rendered often: the entrance would restart each time
  id: "",             // fixes the generated element ids; derived from content when blank
  title: "",
  desc: "",
  className: "",
};

function opt(o, k) { return o && o[k] !== undefined ? o[k] : DEF[k]; }

/** Push labels apart so they never collide on the same side of the ring. */
function spread(items, minGap, lo, hi) {
  items.sort(function (a, b) { return a.y - b.y; });
  for (var i = 1; i < items.length; i++) {
    if (items[i].y - items[i - 1].y < minGap) items[i].y = items[i - 1].y + minGap;
  }
  var over = items.length ? items[items.length - 1].y - hi : 0;
  if (over > 0) for (var j = 0; j < items.length; j++) items[j].y -= over;
  if (items.length && items[0].y < lo) {
    var under = lo - items[0].y;
    for (var k = 0; k < items.length; k++) items[k].y += under;
  }
  return items;
}

/**
 * Render a donut (or a pie, with thickness 1) as an SVG string.
 * @param {{data:Array, size?:number, height?:number, thickness?:number, gap?:number,
 *          labels?:boolean, legend?:boolean, unit?:string, decimals?:number,
 *          centerCaption?:string, centerValue?:string, transparent?:boolean,
 *          title?:string, desc?:string, className?:string}} o
 * @returns {string} SVG markup, safe to inject; every value is escaped.
 */
export function renderDonut(o) {
  var rows = series(o && o.data, o && o.colors);
  var W = opt(o, "size"), H = opt(o, "height");
  var unit = opt(o, "unit"), dp = opt(o, "decimals");
  var total = rows.reduce(function (a, d) { return a + d.value; }, 0);
  if (!rows.length || !total) return tag("figure", { class: "jwc jwc-donut is-empty" }, "");

  var labels = opt(o, "labels");
  var cx = W / 2, cy = H / 2 + 6;
  var outer = opt(o, "radius") || Math.min(H / 2 - 26, labels ? W / 4.4 : W / 2.2);
  var inner = outer * (1 - Math.min(1, Math.max(0.08, opt(o, "thickness"))));
  var gapTurn = Math.max(0, opt(o, "gap")) / 360;
  // one key per chart, so ids are stable across server and client renders
  var key = (o && o.id) || (opt(o, "title") + "|" + rows.map(function (d) {
    return d.label + ":" + d.value;
  }).join(","));
  var glow = uid("jwcglow", key), titleId = uid("jwct", key), descId = uid("jwcd", key);

  // --- slices -------------------------------------------------------------
  var at = 0, slices = [], leaders = [], left = [], right = [];
  rows.forEach(function (d, i) {
    var span = d.value / total;
    var from = at + gapTurn / 2, to = at + span - gapTurn / 2;
    if (to <= from) { from = at; to = at + span; }           // slice thinner than the gap
    var mid = at + span / 2;
    at += span;

    var dir = polar(0, 0, 1, mid);                            // unit vector for the hover lift
    slices.push(tag("g", {
      class: "jwc-slice",
      style: "--jwc-c:" + d.color + ";--jwc-dx:" + num(dir[0] * 7, 2) + "px;--jwc-dy:" + num(dir[1] * 7, 2) + "px",
      "data-label": d.label,
      "data-value": num(d.value, dp),
      "data-display": compact(d.value, 1) + (unit ? " " + unit : ""),
      "data-pct": pct(d.value, total),
      tabindex: "0", role: "listitem",
      "aria-label": d.label + ": " + compact(d.value, 1) + (unit ? " " + unit : "") + ", " + pct(d.value, total),
    }, tag("path", { class: "jwc-arc", d: arcPath(cx, cy, inner, outer, from, to), filter: "url(#" + glow + ")" })
       + tag("title", null, esc(d.label + " — " + compact(d.value, 1) + (unit ? " " + unit : "") + " (" + pct(d.value, total) + ")"))));

    if (labels) {
      var side = Math.cos(mid * Math.PI * 2 - Math.PI / 2) >= 0 ? 1 : -1;   // right or left of the ring
      var anchor = polar(cx, cy, outer + 10, mid);
      (side > 0 ? right : left).push({
        i: i, color: d.color, label: d.label, side: side,
        value: compact(d.value, 1) + (unit ? " " + unit : ""), pct: pct(d.value, total),
        ax: anchor[0], ay: anchor[1], y: anchor[1],
      });
    }
  });

  // --- leader lines and outside labels ------------------------------------
  if (labels) {
    [right, left].forEach(function (group) {
      spread(group, 40, 26, H - 20);
      group.forEach(function (p) {
        var elbowX = cx + p.side * (outer + 26);
        var endX = cx + p.side * (outer + 44);
        leaders.push(tag("g", { class: "jwc-leader", "data-for": p.i, style: "--jwc-c:" + p.color },
          tag("path", { class: "jwc-leader-line", fill: "none",
            d: "M" + num(p.ax, 1) + "," + num(p.ay, 1) + "L" + num(elbowX, 1) + "," + num(p.y, 1) + "H" + num(endX, 1) })
          + tag("circle", { class: "jwc-leader-dot", cx: num(endX, 1), cy: num(p.y, 1), r: 2.2 })
          + tag("text", { class: "jwc-leader-label", x: num(endX + p.side * 8, 1), y: num(p.y - 3, 1),
              "text-anchor": p.side > 0 ? "start" : "end" }, esc(p.label))
          + tag("text", { class: "jwc-leader-value", x: num(endX + p.side * 8, 1), y: num(p.y + 13, 1),
              "text-anchor": p.side > 0 ? "start" : "end" }, esc(p.pct + "  ·  " + p.value))));
      });
    });
  }

  // --- centre readout ------------------------------------------------------
  var centerValue = opt(o, "centerValue");
  if (centerValue === null) centerValue = compact(total, 1) + (unit ? " " + unit : "");
  var centre = tag("g", { class: "jwc-center", "data-total": centerValue,
                          "data-caption": opt(o, "centerCaption") },
    tag("text", { class: "jwc-center-value", x: cx, y: cy + 2, "text-anchor": "middle" }, esc(centerValue))
    + (opt(o, "centerCaption")
        ? tag("text", { class: "jwc-center-caption", x: cx, y: cy + 24, "text-anchor": "middle" },
              esc(opt(o, "centerCaption")))
        : ""));

  // a soft bloom is what keeps a frameless chart from looking flat
  var defs = tag("defs", null, tag("filter", { id: glow, x: "-20%", y: "-20%", width: "140%", height: "140%" },
    tag("feGaussianBlur", { in: "SourceAlpha", stdDeviation: "5", result: "b" })
    + tag("feComponentTransfer", { in: "b", result: "s" }, tag("feFuncA", { type: "linear", slope: "0.5" }))
    + tag("feMerge", null, tag("feMergeNode", { in: "s" }) + tag("feMergeNode", { in: "SourceGraphic" }))));

  var titleText = opt(o, "title") || "Donut chart";
  var descText = opt(o, "desc") || rows.map(function (d) {
    return d.label + " " + pct(d.value, total);
  }).join(", ");

  var svg = tag("svg", {
    viewBox: "0 0 " + W + " " + H, role: "img",
    "aria-labelledby": titleId + " " + descId,
    class: "jwc-svg" + (opt(o, "transparent") ? " is-glass" : " is-solid"),
  }, tag("title", { id: titleId }, esc(titleText))
     + tag("desc", { id: descId }, esc(descText))
     + defs
     + tag("g", { class: "jwc-slices", role: "list" }, slices.join(""))
     + (leaders.length ? tag("g", { class: "jwc-leaders" }, leaders.join("")) : "")
     + centre);

  var legend = "";
  if (opt(o, "legend")) {
    legend = tag("ul", { class: "jwc-legend" }, rows.map(function (d, i) {
      return tag("li", { class: "jwc-legend-item", "data-for": i, style: "--jwc-c:" + d.color },
        tag("i", { class: "jwc-legend-swatch", "aria-hidden": "true" }, "")
        + tag("span", { class: "jwc-legend-label" }, esc(d.label))
        + tag("span", { class: "jwc-legend-value" }, esc(pct(d.value, total) + " · " + compact(d.value, 1) + (unit ? " " + unit : ""))));
    }).join(""));
  }

  var cls = "jwc jwc-donut" + (opt(o, "animate") ? "" : " jwc-static") + " " + opt(o, "className");
  return tag("figure", { class: cls.trim(), "data-jwc": "donut" }, svg + legend);
}
