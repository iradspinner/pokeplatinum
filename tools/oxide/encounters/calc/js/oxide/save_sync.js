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
//
// The save also says which level-cap split the player is in, so the
// calculator's level cap (the Box's cap and its "set to cap") follows it:
// set when a save's cap differs from the last one set here, so a cap typed
// by hand stays until the game's own cap changes (step 4).
//
// The same save carries the game's battle log, its last 60 trainer battles
// (request 4, docs/oxide/battle-log.md). On each new save this fetches
// /api/save/battlelog, which the OxiDex has already turned into the Battle
// Log's own payload with every name filled in, and hands it to the Battle
// Log's save-file source (VENDORED.md patch 18). The Battle Log's split tabs
// are Oxide's level-cap splits, which the payload lists.
(function () {
  if (window.__oxideSaveSync) {
    return;
  }
  window.__oxideSaveSync = true;
  var lastSeq = 0, lastCap = null;

  function applyCap(save) {
    var split = save && save.progress && save.progress.split;
    if (!split || !split.cap || split.cap === lastCap) {
      return;
    }
    lastCap = split.cap;
    try { localStorage.lvlCap = String(split.cap); } catch (e) { /* private window */ }
    $('#lvl-cap').val(split.cap).trigger('change');
  }

  // The Battle Log's split tabs, by the split index each battle records. Not
  // splitData: the Fragsheet reads that too and has room for nine splits,
  // where Oxide has thirteen.
  function applySplits(splits) {
    if (!Array.isArray(splits) || !splits.length) {
      return;
    }
    var titles = [];
    splits.forEach(function (s) { titles[s.index] = s.name; });
    window.oxideBattleLogSplitTitles = titles;
  }

  function syncBattleLog() {
    if (typeof window.updateSaveFileBattleLog !== "function") {
      return;
    }
    fetch("/api/save/battlelog", { cache: "no-store" })
      .then(function (r) { return r.json(); })
      .then(function (out) {
        if (!out || !out.calc) {
          return;
        }
        applySplits(out.calc.splits);
        var records = (out.log && out.log.records) || [];
        // The Battle Log wants {valid, hasLogs, records}; the records are
        // only counted, since the payload is already built.
        window.updateSaveFileBattleLog(
          { valid: true, hasLogs: records.length > 0, records: records, payload: out.calc },
          [], "the OxiDex's save", { activate: true });
      })
      .catch(function (e) { console.warn("Oxide: the battle log could not be read", e); });
  }

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
          applyCap(s.save);
          $(btn).click();
          syncBattleLog();
        }
      })
      .catch(function () { /* the OxiDex is restarting; the next tick tries again */ });
  }

  setTimeout(tick, 1500);
  setInterval(tick, 3000);
})();
