/** jwchart — small, dependency-free SVG charts that render to a string.
 *
 *  Two halves, deliberately separable:
 *    render*(options) -> SVG string, pure, runs anywhere (server, build step, browser)
 *    enhance(root)    -> optional browser-only hover/focus behaviour over that markup
 *
 *  So a page works fully rendered with JavaScript disabled, and gets interaction
 *  when it is available.  See README.md.
 */

export { renderDonut } from "./donut.js";
export { arcPath, compact, esc, num, pct, polar, series, tag, uid, PALETTE } from "./core.js";

import { renderDonut } from "./donut.js";

/** Chart types enhance() knows how to wire, keyed by the data-jwc attribute. */
var TYPES = { donut: wireDonut };

function all(root, sel) { return [].slice.call(root.querySelectorAll(sel)); }

function wireDonut(fig, off) {
  var slices = all(fig, ".jwc-slice");
  var legend = all(fig, ".jwc-legend-item");
  var leaders = all(fig, ".jwc-leader");
  var centre = fig.querySelector(".jwc-center");
  var valueText = fig.querySelector(".jwc-center-value");
  var capText = fig.querySelector(".jwc-center-caption");
  if (!slices.length) return;

  var restore = centre ? { value: centre.getAttribute("data-total"), cap: centre.getAttribute("data-caption") || "" } : null;
  var pinned = -1;

  function paint(i) {
    fig.classList.toggle("is-focused", i >= 0);
    slices.forEach(function (s, k) { s.classList.toggle("is-active", k === i); });
    legend.forEach(function (s, k) { s.classList.toggle("is-active", k === i); });
    leaders.forEach(function (s) {
      s.classList.toggle("is-active", Number(s.getAttribute("data-for")) === i);
    });
    if (!restore) return;
    // the middle of the ring doubles as the readout, so no tooltip is needed
    if (i < 0) {
      if (valueText) valueText.textContent = restore.value;
      if (capText) capText.textContent = restore.cap;
    } else {
      var s = slices[i];
      if (valueText) valueText.textContent = s.getAttribute("data-pct");
      if (capText) capText.textContent = s.getAttribute("data-label") + " · " + s.getAttribute("data-display");
    }
  }

  function bindTo(nodes, index) {
    nodes.forEach(function (node, k) {
      var i = index === undefined ? k : Number(node.getAttribute("data-for"));
      function enter() { if (pinned < 0) paint(i); }
      function leave() { if (pinned < 0) paint(-1); }
      function toggle(e) {
        if (e && e.preventDefault) e.preventDefault();
        pinned = pinned === i ? -1 : i;
        fig.classList.toggle("is-pinned", pinned >= 0);
        paint(pinned < 0 ? -1 : pinned);
      }
      function key(e) {
        if (e.key === "Enter" || e.key === " ") return toggle(e);
        if (e.key === "Escape" && pinned >= 0) { pinned = -1; fig.classList.remove("is-pinned"); paint(-1); return; }
        var step = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1
                 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
        if (!step) return;
        e.preventDefault();
        var next = (i + step + slices.length) % slices.length;
        slices[next].focus();
      }
      node.addEventListener("pointerenter", enter);
      node.addEventListener("pointerleave", leave);
      node.addEventListener("focus", enter);
      node.addEventListener("blur", leave);
      node.addEventListener("click", toggle);
      node.addEventListener("keydown", key);
      off.push(function () {
        node.removeEventListener("pointerenter", enter);
        node.removeEventListener("pointerleave", leave);
        node.removeEventListener("focus", enter);
        node.removeEventListener("blur", leave);
        node.removeEventListener("click", toggle);
        node.removeEventListener("keydown", key);
      });
    });
  }

  bindTo(slices);
  bindTo(legend);
  bindTo(leaders, "data-for");
  off.push(function () {
    paint(-1);
    fig.classList.remove("is-focused", "is-pinned");
  });
}

/**
 * Attach interaction to charts already present in the DOM.
 * Safe to call repeatedly; call the returned function to detach.
 * @param {ParentNode} [root=document]
 * @returns {function(): void} teardown
 */
export function enhance(root) {
  if (typeof document === "undefined") return function () {};
  var scope = root || document;
  var off = [];
  all(scope, "[data-jwc]").forEach(function (fig) {
    if (fig.getAttribute("data-jwc-ready") === "1") return;
    var wire = TYPES[fig.getAttribute("data-jwc")];
    if (!wire) return;
    fig.setAttribute("data-jwc-ready", "1");
    off.push(function () { fig.removeAttribute("data-jwc-ready"); });
    wire(fig, off);
  });
  return function () { off.forEach(function (f) { f(); }); };
}

/** Render into an element in one step, for plain-DOM use without a framework. */
export function mountDonut(target, options) {
  var el = typeof target === "string" ? document.querySelector(target) : target;
  if (!el) return function () {};
  el.innerHTML = renderDonut(options);
  return enhance(el);
}
