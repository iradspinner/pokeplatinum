// Which colour scheme the encounter tool draws in, light or dark.
//
// Loaded as an ordinary blocking script in <head>, straight after theme.css,
// so it runs before the first paint and a pinned scheme never flashes the
// other one first. It is not a module and not deferred, for the same reason.
//
// The page follows Windows by default. One button in the header offers the
// opposite of whatever the system is showing right now, and pressing it pins
// that exact scheme, so if Windows later switches to match, the page stays
// where Ian put it. Once something is pinned the same button offers "System",
// which releases the pin. The label always names what pressing it will do.
//
// The preference is per browser, so it lives in localStorage rather than going
// through the server the way the caught list does. Every storage access is
// wrapped: a private window or blocked storage throws, and an empty or
// throwing store simply means "follow the system".
//
// The damage calculator (M8 D5) will load this same file, so any button marked
// data-theme-toggle is wired automatically and the two pages share one setting.
(function () {
  "use strict";

  var KEY = "oxide-color-scheme";
  var media = window.matchMedia("(prefers-color-scheme: dark)");
  var listeners = [];

  function pinned() {
    try {
      var value = window.localStorage.getItem(KEY);
      return value === "light" || value === "dark" ? value : null;
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
  // pins it. The meta is kept in step so the two never disagree.
  function apply(value) {
    var meta = document.querySelector('meta[name="color-scheme"]');
    if (meta) meta.setAttribute("content", value || "light dark");
    document.documentElement.style.colorScheme = value || "";
  }

  function system() {
    return media.matches ? "dark" : "light";
  }

  // What pressing the button will do: release a pin, or pin the opposite of
  // what the system is showing.
  function label() {
    if (pinned()) return "System";
    return system() === "dark" ? "Light" : "Dark";
  }

  function notify() {
    listeners.forEach(function (fn) {
      try { fn(); } catch (e) { /* one listener must not stop the rest */ }
    });
  }

  function toggle() {
    var next = pinned() ? null : (system() === "dark" ? "light" : "dark");
    remember(next);
    apply(next);
    notify();
    return label();
  }

  apply(pinned());

  // Windows switching scheme changes what the button should offer, and the
  // page redraws anything whose colour it had to work out in script.
  var onSystem = function () { notify(); };
  if (media.addEventListener) media.addEventListener("change", onSystem);
  else if (media.addListener) media.addListener(onSystem);

  function wire(button) {
    button.textContent = label();
    button.title = "Colour scheme: follow Windows, or pin the other one";
    button.addEventListener("click", function () { toggle(); });
  }

  // Keep every toggle's label current, however the change came about.
  listeners.push(function () {
    var buttons = document.querySelectorAll("[data-theme-toggle]");
    for (var i = 0; i < buttons.length; i++) buttons[i].textContent = label();
  });

  document.addEventListener("DOMContentLoaded", function () {
    var buttons = document.querySelectorAll("[data-theme-toggle]");
    for (var i = 0; i < buttons.length; i++) wire(buttons[i]);
  });

  window.oxideTheme = {
    label: label,
    toggle: toggle,
    pinned: pinned,
    onChange: function (fn) { listeners.push(fn); }
  };
})();
