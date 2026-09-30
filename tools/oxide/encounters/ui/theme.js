// Which colour scheme the encounter tool draws in: light, dark, or dim, the
// dark scheme on a cyan ground (Ian, 2026-09-28).
//
// Loaded as an ordinary blocking script in <head>, straight after theme.css,
// so it runs before the first paint and a pinned scheme never flashes the
// other one first. It is not a module and not deferred, for the same reason.
//
// The page follows Windows by default. The header has four buttons (Ian,
// 2026-09-29, the redesign): Dark, Dim and Light pin that look, and Auto
// follows Windows again; the one in force is marked. A pin stays where Ian
// put it if Windows later switches. Any button marked data-theme-set="dark",
// "dim", "light" or "auto" is wired. The older single button that steps
// through the looks (data-theme-toggle) still works on any page that has it,
// skipping the pin that would look the same as what Windows shows, so every
// press changes something; its label names what pressing it will do.
//
// The preference is per browser, so it lives in localStorage rather than going
// through the server the way the caught list does. Every storage access is
// wrapped: a private window or blocked storage throws, and an empty or
// throwing store simply means "follow the system".
//
// The damage calculator (M8 D5) loads this same file, so any button marked
// data-theme-toggle is wired automatically and the two pages share one setting.
(function () {
  "use strict";

  var KEY = "oxide-color-scheme";
  var media = window.matchMedia("(prefers-color-scheme: dark)");
  var listeners = [];

  function pinned() {
    try {
      var value = window.localStorage.getItem(KEY);
      return value === "light" || value === "dark" || value === "dim" ? value : null;
    } catch (e) {
      return null;
    }
  }

  function remember(value) {
    try {
      if (value) window.localStorage.setItem(KEY, value);
      else window.localStorage.removeItem(KEY);
    } catch (e) {
      // The pin still applies to this tab; it just will not outlive it.
    }
  }

  // Pin a scheme, or release one with null. Writing the meta tag alone does
  // not pin anything: a color-scheme meta only takes effect while the root
  // element's own color-scheme is `normal`, and theme.css sets it to
  // `light dark` so the page follows the system even with scripts off. An
  // inline style on <html> outranks the stylesheet, so that is what actually
  // pins it. The meta is kept in step so the two never disagree. Dim is the
  // dark scheme with theme.css's data-theme="dim" overrides on top.
  function apply(value) {
    var scheme = value === "dim" ? "dark" : value;
    var meta = document.querySelector('meta[name="color-scheme"]');
    if (meta) meta.setAttribute("content", scheme || "light dark");
    document.documentElement.style.colorScheme = scheme || "";
    if (value === "dim") document.documentElement.setAttribute("data-theme", "dim");
    else document.documentElement.removeAttribute("data-theme");
  }

  function system() {
    return media.matches ? "dark" : "light";
  }

  // The next look in the cycle, null for following Windows: from the
  // system's look, the dimmer-or-brighter neighbours in order, then back.
  function next() {
    var order = system() === "dark" ? ["dim", "light", null] : ["dark", "dim", null];
    var now = pinned();
    if (!now) return order[0];
    var i = order.indexOf(now);
    // A pin the order does not hold (Dark on a dark desktop, Light on a
    // light one, left from before Windows switched) releases on the next press.
    return i < 0 ? null : order[i + 1];
  }

  var NAMES = { dark: "Dark", dim: "Dim", light: "Light" };

  // What pressing the button will do.
  function label() {
    var n = next();
    return n ? NAMES[n] : "System";
  }

  function notify() {
    listeners.forEach(function (fn) {
      try { fn(); } catch (e) { /* one listener must not stop the rest */ }
    });
  }

  function toggle() {
    var value = next();
    remember(value);
    apply(value);
    notify();
    return label();
  }

  // Pin one look, or follow Windows with "auto" (or null).
  function set(value) {
    value = value === "dark" || value === "dim" || value === "light" ? value : null;
    remember(value);
    apply(value);
    notify();
  }

  // Mark the button of the look in force: the pinned one, or Auto.
  function mark() {
    var now = pinned() || "auto";
    var buttons = document.querySelectorAll("[data-theme-set]");
    for (var i = 0; i < buttons.length; i++) {
      var on = buttons[i].getAttribute("data-theme-set") === now;
      buttons[i].classList.toggle("on", on);
      buttons[i].setAttribute("aria-pressed", on ? "true" : "false");
    }
  }

  apply(pinned());

  // Windows switching scheme changes what the button should offer, and the
  // page redraws anything whose colour it had to work out in script.
  var onSystem = function () { notify(); };
  if (media.addEventListener) media.addEventListener("change", onSystem);
  else if (media.addListener) media.addListener(onSystem);

  function wire(button) {
    button.textContent = label();
    button.title = "Colour scheme: Dark, Dim (a soft grey) or Light, or follow Windows";
    button.addEventListener("click", function () { toggle(); });
  }

  // Another page of the tool changed the setting: the calculator in its
  // frame, or a second tab. The storage event reaches every other document on
  // this origin, so each follows without a reload.
  window.addEventListener("storage", function (event) {
    if (event.key !== KEY && event.key !== null) return;
    apply(pinned());
    notify();
  });

  // Keep every toggle's label current, however the change came about.
  listeners.push(function () {
    var buttons = document.querySelectorAll("[data-theme-toggle]");
    for (var i = 0; i < buttons.length; i++) buttons[i].textContent = label();
  });

  listeners.push(mark);

  document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll("[data-theme-toggle]");
    for (var i = 0; i < buttons.length; i++) wire(buttons[i]);
    var sets = document.querySelectorAll("[data-theme-set]");
    for (var j = 0; j < sets.length; j++) {
      sets[j].addEventListener("click", function () { set(this.getAttribute("data-theme-set")); });
    }
    mark();
  });

  // The favicon: a 16 by 16 pixel mark, a teal diamond with a pink core. It is
  // an SVG drawn from the page's own tokens rather than from colour literals,
  // so it follows the theme like everything else and this file stays free of
  // hex. A favicon is its own document and cannot read CSS variables, so the
  // resolved colours are read back from the page and written into it.
  function tokenColour(name) {
    var probe = document.createElement("span");
    probe.style.color = "var(" + name + ")";
    document.body.appendChild(probe);
    var colour = getComputedStyle(probe).color;
    document.body.removeChild(probe);
    return colour;
  }

  function pixelDiamond(widths, top, fill) {
    // One rect per row, centred, so the edges step like a sprite's do.
    var out = "";
    for (var i = 0; i < widths.length; i++) {
      var w = widths[i];
      out += '<rect x="' + (8 - w / 2) + '" y="' + (top + i) + '" width="' + w +
             '" height="1" fill="' + fill + '"/>';
    }
    return out;
  }

  function drawFavicon() {
    if (!document.body) return;
    var outer = [2, 4, 6, 8, 10, 12, 14, 16, 16, 14, 12, 10, 8, 6, 4, 2];
    var core = [2, 4, 6, 6, 4, 2];
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" ' +
              'shape-rendering="crispEdges">' +
              pixelDiamond(outer, 0, tokenColour("--mass")) +
              pixelDiamond(core, 5, tokenColour("--place-ink")) + "</svg>";
    var link = document.querySelector('link[rel="icon"]');
    if (!link) {
      link = document.createElement("link");
      link.rel = "icon";
      document.head.appendChild(link);
    }
    link.href = "data:image/svg+xml," + encodeURIComponent(svg);
  }

  listeners.push(drawFavicon);
  document.addEventListener("DOMContentLoaded", drawFavicon);

  window.oxideTheme = {
    label: label,
    toggle: toggle,
    set: set,
    pinned: pinned,
    onChange: function (fn) { listeners.push(fn); }
  };
})();
