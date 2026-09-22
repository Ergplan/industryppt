/** Deck interactions: hover or tap a chart to read the numbers behind it.
 *
 *  Written once, used twice — the Next.js site imports it, and
 *  tools/generator/build.py inlines this same file into the standalone decks, so
 *  both behave identically.  Keep it framework-free: no imports, no JSX, and the
 *  only contract with either renderer is the data-* attributes read below.
 *
 *  Every figure stays perfectly usable with this file absent; it only adds a readout.
 */

import { renderDonut } from "./jwchart/index.js";

var LAYER_COLOR = { power: "#3dd68c", heat: "#f2994a", data: "#5b8def", esg: "#c9a43a" };
var KIND_COLOR = { fuel: "#5d666c", grid: "#f2994a", green: "#3dd68c" };
/** Where supply comes from, in the order it stacks on the area chart. */
var SUPPLY = [
  ["wind", "Wind \u00b7 ISTS", "#1f7a55"],
  ["solar", "Solar", "#3dd68c"],
  ["bess", "BESS", "#5b8def"],
  ["market", "Green market", "#8fd9b6"],
];

function n(node, key) { var v = parseFloat(node.getAttribute(key)); return isNaN(v) ? 0 : v; }
function attr(node, key) { return node.getAttribute(key) || ""; }
function json(node, key, fallback) {
  try { return JSON.parse(node.getAttribute(key)); } catch (e) { return fallback; }
}
function round(v, dp) { return (Math.round(v * Math.pow(10, dp)) / Math.pow(10, dp)).toFixed(dp); }
function clock(h) {
  var hh = Math.floor(h), mm = Math.round((h - hh) * 60);
  if (mm === 60) { mm = 0; hh += 1; }
  return (hh < 10 ? "0" : "") + (hh % 24) + ":" + (mm < 10 ? "0" : "") + mm;
}

/* ------------------------------------------------------------------ tooltip */

function makeTip(host) {
  var node = document.createElement("div");
  node.className = "jw-tip";
  node.setAttribute("role", "status");
  node.setAttribute("aria-live", "polite");
  node.hidden = true;
  host.appendChild(node);

  var pinned = null;   // the element whose readout is held open
  var shown = null;    // last payload rendered, so a moving cursor does not rebuild it

  function render(d) {
    node.className = "jw-tip" + (d.variant ? " " + d.variant : "");
    node.innerHTML = "";
    if (d.chart) {                                  // a chart stands in for the value rows
      var c = document.createElement("div");
      c.className = "jw-tip-c";
      c.innerHTML = d.chart;
      node.appendChild(c);
    }
    var h = document.createElement("div");
    h.className = "jw-tip-h";
    if (d.accent) h.style.color = d.accent;
    h.textContent = d.title;
    node.appendChild(h);
    if (d.sub) {
      var s = document.createElement("div");
      s.className = "jw-tip-s";
      s.textContent = d.sub;
      node.appendChild(s);
    }
    if (d.rows && d.rows.length) {
      var dl = document.createElement("dl");
      d.rows.forEach(function (r) {
        var dt = document.createElement("dt"); dt.textContent = r[0];
        var dd = document.createElement("dd"); dd.textContent = r[1];
        if (r[2]) dd.style.color = r[2];
        dl.appendChild(dt); dl.appendChild(dd);
      });
      node.appendChild(dl);
    }
    if (d.note) {
      var nt = document.createElement("div");
      nt.className = "jw-tip-n";
      nt.textContent = d.note;
      node.appendChild(nt);
    }
  }

  function place(x, y) {
    var appearing = node.hidden;                  // do not glide in from the last spot
    node.hidden = false;
    var r = node.getBoundingClientRect(), gap = 18, pad = 8;
    var left = x + gap, top = y + gap;
    if (left + r.width > window.innerWidth - pad) left = x - r.width - gap;
    if (left < pad) left = pad;
    if (top + r.height > window.innerHeight - pad) top = y - r.height - gap;
    if (top < pad) top = pad;
    if (appearing) node.style.transition = "none";
    node.style.transform = "translate(" + Math.round(left) + "px," + Math.round(top) + "px)";
    if (appearing) {
      void node.offsetWidth;                      // commit the jump before re-arming the glide
      node.style.transition = "";
    }
  }

  return {
    node: node,
    show: function (owner, d, x, y) {
      if (pinned && pinned !== owner) return;
      if (d !== shown) { render(d); shown = d; }    // same payload: just move it
      place(x, y);
    },
    move: function (owner, x, y) {
      if (pinned && pinned !== owner) return;
      if (!node.hidden) place(x, y);
    },
    hide: function () {
      if (pinned) return;             // a pinned readout stays until dismissed
      node.hidden = true;
    },
    toggle: function (owner, d, x, y) {
      if (pinned === owner) { this.unpin(); return false; }
      shown = null;
      if (pinned) this.unpin();
      pinned = owner;
      shown = d;
      if (owner.classList) owner.classList.add("is-pinned");
      render(d); place(x, y);
      return true;
    },
    unpin: function () {
      // sweep the whole host: a pin can mark a second element too, such as a map
      // marker and the description paired with it
      var marked = host.querySelectorAll(".is-pinned");
      for (var i = 0; i < marked.length; i++) marked[i].classList.remove("is-pinned");
      pinned = null;
      node.hidden = true;
    },
    isPinned: function (owner) { return pinned === owner; },
    pinnedEl: function () { return pinned; },
  };
}

/** Wire one element as a hover/tap readout. Returns a teardown function. */
function bind(elm, tip, build, opts) {
  opts = opts || {};
  var off = [];
  function on(target, type, fn, o) {
    target.addEventListener(type, fn, o);
    off.push(function () { target.removeEventListener(type, fn, o); });
  }
  function xy(e) {
    if (e.clientX != null) return [e.clientX, e.clientY];
    var r = elm.getBoundingClientRect();
    return [r.left + r.width / 2, r.top + r.height / 2];
  }
  on(elm, "pointerenter", function (e) {
    if (e.pointerType === "touch") return;      // touch gets the tap handler instead
    elm.classList.add("is-hot");
    if (opts.enter) opts.enter(e);
    var p = xy(e); tip.show(elm, build(e), p[0], p[1]);
  });
  on(elm, "pointermove", function (e) {
    if (e.pointerType === "touch") return;
    if (opts.move) opts.move(e);
    var p = xy(e);
    if (opts.live) tip.show(elm, build(e), p[0], p[1]); else tip.move(elm, p[0], p[1]);
  });
  on(elm, "pointerleave", function () {
    elm.classList.remove("is-hot");
    if (opts.leave) opts.leave();
    tip.hide(elm);
  });
  on(elm, "click", function (e) {
    var p = xy(e);
    tip.toggle(elm, build(e), p[0], p[1]);
    if (opts.click) opts.click(e);
  });
  on(elm, "keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    e.preventDefault();
    var p = xy(e);
    tip.toggle(elm, build(e), p[0], p[1]);
    if (opts.click) opts.click(e);
  });
  if (!elm.hasAttribute("tabindex")) elm.setAttribute("tabindex", "0");
  on(elm, "focus", function (e) {
    elm.classList.add("is-hot");
    var p = xy(e); tip.show(elm, build(e), p[0], p[1]);
  });
  on(elm, "blur", function () { elm.classList.remove("is-hot"); tip.hide(elm); });
  elm.classList.add("jw-live");
  return function () {
    off.forEach(function (f) { f(); });
    elm.classList.remove("jw-live", "is-hot", "is-pinned");
  };
}

/* -------------------------------------------------------------- economics */

function wireEcon(scope, tip, off) {
  [].slice.call(scope.querySelectorAll('[data-jw="econ"]')).forEach(function (chart) {
    var rows = [].slice.call(chart.querySelectorAll(".erow[data-cost]"));
    if (!rows.length) return;
    // the incumbent every option is judged against: the first fuel-fired row
    var base = null;
    rows.forEach(function (r) { if (!base && attr(r, "data-kind") === "fuel") base = r; });
    var baseCost = base ? n(base, "data-cost") : 0;
    var baseCo2 = base ? n(base, "data-co2") : 0;
    rows.forEach(function (row) {
      off.push(bind(row, tip, function () {
        var cost = n(row, "data-cost"), co2 = n(row, "data-co2");
        var kind = attr(row, "data-kind");
        var out = [
          ["Cost of useful heat", "₹ " + round(cost, 2) + " / kWh-th", KIND_COLOR[kind]],
          ["Carbon", co2 ? round(co2, 3) + " kg CO₂ / kWh-th" : "≈ 0 kg CO₂ / kWh-th",
            co2 ? null : "#3dd68c"],
        ];
        var note = null;
        if (base && row !== base && baseCost) {
          var dc = (1 - cost / baseCost) * 100;
          var de = baseCo2 ? (1 - co2 / baseCo2) * 100 : 0;
          out.push([dc >= 0 ? "Cheaper than baseline" : "Dearer than baseline",
            round(Math.abs(dc), 0) + "%", dc >= 0 ? "#3dd68c" : "#e0604a"]);
          if (baseCo2) out.push(["Less carbon than baseline", round(de, 0) + "%", "#3dd68c"]);
          note = "Baseline: " + attr(base, "data-name");
        } else if (row === base) {
          note = "This row is the baseline the others are compared against.";
        }
        return { title: attr(row, "data-name"), sub: attr(row, "data-sub"),
                 accent: KIND_COLOR[kind], rows: out, note: note };
      }));
    });
  });
}

/* ------------------------------------------------------------ heat ladder */

function wireLoads(scope, tip, off) {
  [].slice.call(scope.querySelectorAll('[data-jw="loads"] .lrow[data-min]')).forEach(function (row) {
    off.push(bind(row, tip, function () {
      var lo = n(row, "data-min"), hi = n(row, "data-max");
      var hp = attr(row, "data-hp") === "1";
      var out = [
        ["Temperature", round(lo, 0) + "–" + round(hi, 0) + " °C", hp ? "#f2994a" : "#8b949a"],
        ["Heat pump range", hp ? "Within reach" : "Above 120 °C", hp ? "#3dd68c" : "#8b949a"],
      ];
      var head = 120 - hi;
      if (hp && head >= 0) out.push(["Headroom to the ceiling", round(head, 0) + " K"]);
      return {
        title: attr(row, "data-name"), sub: attr(row, "data-sub"),
        accent: hp ? "#f2994a" : "#8b949a", rows: out,
        note: hp ? "A heat pump can serve this load today."
                 : "Stays on existing burners or electrode heat.",
      };
    }));
  });
}

/* --------------------------------------------------- heat pump 101 balance */

function wireBalance(scope, tip, off) {
  [].slice.call(scope.querySelectorAll('[data-jw="balance"] .brow[data-out]')).forEach(function (row) {
    off.push(bind(row, tip, function () {
      var ins = json(row, "data-in", []) || [];
      var out = n(row, "data-out");
      var paid = 0, rows = [];
      ins.forEach(function (p) {
        var k = p[0], v = p[1];
        var free = k === "free" || k === "ambient";
        if (!free) paid += v;
        rows.push([free ? "Free ambient heat in" : k.charAt(0).toUpperCase() + k.slice(1) + " in",
          round(v, 2) + " kWh", free ? "#5b8def" : "#3dd68c"]);
      });
      rows.push(["Useful heat out", round(out, 2) + " kWh", "#f2994a"]);
      var ratio = paid ? out / paid : 0;
      if (ratio > 1) rows.push(["COP", round(ratio, 2) + "×", "#3dd68c"]);
      else if (paid) rows.push(["Efficiency", round(ratio * 100, 0) + "%", "#8b949a"]);
      return {
        title: attr(row, "data-name"), accent: ratio > 1 ? "#3dd68c" : "#8b949a", rows: rows,
        note: ratio > 1
          ? "Every paid kWh moves " + round(ratio, 1) + " kWh of heat, because most of it is lifted, not burned."
          : "Burning converts; it cannot multiply.",
      };
    }));
  });
}

/* ---------------------------------------------------------- 24-hour chart */

function wireDay(scope, tip, off) {
  [].slice.call(scope.querySelectorAll('[data-jw="day"]')).forEach(function (fig) {
    var d = json(fig, "data-day", null);
    var svg = fig.querySelector("svg");
    if (!d || !d.load || !svg) return;
    var g = d.geo, last = d.load.length - 1;

    var rule = document.createElement("i");
    rule.className = "jw-day-rule";
    rule.hidden = true;
    fig.appendChild(rule);
    fig.classList.add("jw-day");

    var idx = 0;
    function at(e) {
      var r = svg.getBoundingClientRect();
      if (!r.width) return 0;
      var x = ((e.clientX - r.left) / r.width) * g.w;          // client px -> viewBox units
      var f = (x - g.l) / (g.w - g.l - g.r);                   // -> 0..1 across the plot
      return Math.max(0, Math.min(last, Math.round(f * last)));
    }
    function moveRule() {
      var xv = g.l + (g.w - g.l - g.r) * (idx / last);
      rule.style.left = (100 * xv / g.w) + "%";
      rule.hidden = false;
    }
    var unit = d.unit || "kW";
    var cache = {};                                  // one payload per block, built once
    function readout(i) {
      if (cache[i]) return cache[i];
      var green = d.wind[i] + d.solar[i] + d.bess[i] + d.market[i];
      cache[i] = {
        variant: "is-chart",
        chart: renderDonut({
          id: "jwday",                               // fixed: only the values change
          data: SUPPLY.map(function (s) {
            return { label: s[1], value: d[s[0]][i], color: s[2] };
          }),
          size: 240, height: 240, thickness: 0.42,
          labels: false, legend: true, unit: unit, decimals: 0, animate: false,
          centerValue: round(d.load[i], 0) + " " + unit,
          centerCaption: "plant load",
          title: "Supply mix at " + clock(d.hours[i]),
        }),
        title: clock(d.hours[i]),
        sub: "block " + (i + 1) + " of " + (last + 1) + " \u00b7 " +
             round(Math.min(100, 100 * green / (d.load[i] || 1)), 0) + "% green",
        accent: "#3dd68c",
        note: d.hp[i] >= 1
          ? "Heat pumps are drawing " + round(d.hp[i], 0) + " " + unit + " of this."
          : "Heat pumps are idle in this block.",
      };
      return cache[i];
    }
    off.push(bind(fig, tip, function (e) {
      if (e && e.clientX != null) idx = at(e);
      moveRule();
      return readout(idx);
    }, {
      live: true,                                      // the readout follows the cursor
      move: function (e) { idx = at(e); moveRule(); },
      leave: function () { if (!tip.isPinned(fig)) rule.hidden = true; },
    }));
    off.push(function () { rule.remove(); fig.classList.remove("jw-day"); });
  });
}

/* ------------------------------------------------------- supply-chain map */

function wireScene(scope, tip, off) {
  [].slice.call(scope.querySelectorAll('[data-jw="scene"]')).forEach(function (section) {
    var marks = [].slice.call(section.querySelectorAll(".mk"));
    var points = [].slice.call(section.querySelectorAll(".pts .pt"));
    if (!marks.length || marks.length !== points.length) return;   // only wire a clean 1:1 map

    marks.forEach(function (mk, i) {
      var pt = points[i];
      var title = (pt.querySelector("h4") || {}).textContent || "";
      var tag = (pt.querySelector(".tag") || {}).textContent || "";
      var text = (pt.querySelector("p") || {}).textContent || "";
      var layer = attr(pt, "data-layer");
      var num = (pt.querySelector(".num") || {}).textContent || String(i + 1);

      function readout() {
        return { title: title, sub: tag ? num + " · " + tag : num,
                 accent: LAYER_COLOR[layer], note: text };
      }
      mk.setAttribute("role", "button");
      mk.setAttribute("aria-label", num + ". " + title);

      var pair = function (adding) {
        return function () {
          pt.classList[adding ? "add" : "remove"]("is-hot");
          mk.classList[adding ? "add" : "remove"]("is-hot");
        };
      };
      // the marker and its description light each other up, whichever one you are on
      off.push(bind(mk, tip, readout, {
        enter: pair(true), leave: pair(false),
        click: function () {
          var on = tip.isPinned(mk);
          pt.classList[on ? "add" : "remove"]("is-pinned");
          if (on && pt.getBoundingClientRect().top > window.innerHeight - 80) {
            pt.scrollIntoView({ behavior: "smooth", block: "center" });
          }
        },
      }));
      off.push(bind(pt, tip, readout, { enter: pair(true), leave: pair(false) }));
    });
  });
}

/* -------------------------------------------------------------------- init */

/**
 * Wire every chart inside `root` (default: the whole document).
 * Safe to call more than once — re-initialising replaces the previous wiring.
 * @returns {function} teardown that removes every listener and added node.
 */
export function initDeckInteractive(root) {
  var scope = root || document;
  if (typeof document === "undefined") return function () {};
  var host = scope.querySelector ? (scope.querySelector(".jw-deck") || scope.body || scope) : scope;
  if (!host || !host.appendChild) return function () {};

  var tip = makeTip(host);
  var off = [];
  wireEcon(scope, tip, off);
  wireLoads(scope, tip, off);
  wireBalance(scope, tip, off);
  wireDay(scope, tip, off);
  wireScene(scope, tip, off);

  function onKey(e) { if (e.key === "Escape") tip.unpin(); }
  function onDown(e) {
    var p = tip.pinnedEl();
    if (p && !p.contains(e.target) && !tip.node.contains(e.target)) tip.unpin();
  }
  document.addEventListener("keydown", onKey);
  document.addEventListener("pointerdown", onDown, true);

  return function destroy() {
    off.forEach(function (f) { f(); });
    document.removeEventListener("keydown", onKey);
    document.removeEventListener("pointerdown", onDown, true);
    tip.unpin();
    if (tip.node.parentNode) tip.node.parentNode.removeChild(tip.node);
  };
}
