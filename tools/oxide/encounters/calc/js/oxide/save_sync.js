// Oxide: the calculator's half of the Sync bridge (Ian's save plan, step 3,
// 2026-09-27; VENDORED.md patch 16).
//
// The OxiDex server watches the save file set in its Calc tab and answers
// /api/save with a number that rises each time it reads a newer save. This
// asks every three seconds while the page is in view and, when the number
// rises, presses Sync, which fetches /api/save/packed (the moveset_import.js
// patch). A save made in game reaches the calculator's box within a few
// seconds with no button pressed; Sync still works by hand. Its tooltip says
// what was read last, or why nothing was.
(function () {
  if (window.__oxideSaveSync) {
    return;
  }
  window.__oxideSaveSync = true;
  var lastSeq = 0;

  function tick() {
    if (typeof TITLE === "undefined" || TITLE !== "Platinum Oxide" || document.hidden) {
      return;
    }
    fetch("/api/save", { cache: "no-store" })
      .then(function (r) { return r.json(); })
      .then(function (s) {
        var btn = document.getElementById("sync-lua");
        if (!btn) {
          return;
        }
        $(btn).show();
        btn.title = s.error ? "The OxiDex cannot read the save: " + s.error
          : s.save ? "From " + s.path + ", saved " + new Date(s.mtime * 1000).toLocaleString()
          : "Set the save file in the OxiDex's Calc tab, above the calculator";
        if (s.save && s.seq > lastSeq) {
          lastSeq = s.seq;
          $(btn).click();
        }
      })
      .catch(function () { /* the OxiDex is restarting; the next tick tries again */ });
  }

  setTimeout(tick, 1500);
  setInterval(tick, 3000);
})();
