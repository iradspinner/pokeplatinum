// Oxide patch 22 (the line tester, docs/oxide/line-tester.md): a Fight button
// under the party. It sends the six species of currentParty, each with its
// "My Box" set (level, nature, ability, item, moves, IVs and EVs), and the
// trainer on the right side, by the trainer id its set carries, to the
// OxiDex's /api/battle, which starts a battle of that party against that
// trainer; the OxiDex then shows it in its Battle tab. Loaded last, so it
// needs no change to upstream's own scripts. The button shows whenever
// upstream shows the party's Clear button, and takes that button's look.
(function () {
  "use strict";
  var LOOK = ["color", "borderTopColor", "borderRightColor", "borderBottomColor", "borderLeftColor",
              "borderTopStyle", "borderRightStyle", "borderBottomStyle", "borderLeftStyle",
              "borderTopWidth", "borderRightWidth", "borderBottomWidth", "borderLeftWidth",
              "borderRadius", "lineHeight", "fontFamily", "fontSize", "paddingTop", "paddingRight",
              "paddingBottom", "paddingLeft", "marginTop", "marginBottom", "marginLeft", "marginRight",
              "textAlign", "width", "backgroundColor"];

  // A party member's own set: the box's, as the calculator's party draws it.
  function boxSet(species) {
    var mine = typeof customSets !== "undefined" && customSets ? customSets : {};
    var sets = typeof setdex !== "undefined" && setdex ? setdex : {};
    return (mine[species] && mine[species]["My Box"]) || (sets[species] && sets[species]["My Box"]) || null;
  }

  function partySets() {
    var party = typeof currentParty !== "undefined" && Array.isArray(currentParty) ? currentParty : [];
    var out = [];
    for (var i = 0; i < party.length && out.length < 6; i++) {
      var s = boxSet(party[i]);
      if (!s || s.isEgg) continue;
      out.push({ species: party[i], level: s.level, nature: s.nature, ability: s.ability, item: s.item,
                 moves: s.moves, ivs: s.ivs, evs: s.evs });
    }
    return out;
  }

  // The right side's set names its trainer: "Species (Lvl N Class Name)",
  // and the set itself carries the trainer's id (calc_trainers.py).
  function rightTrainer() {
    var v = String($("#p2 .set-selector").val() || "");
    var cut = v.indexOf(" (");
    if (cut < 0) return null;
    var species = v.slice(0, cut), name = v.slice(cut + 2, -1);
    var sets = typeof setdex !== "undefined" && setdex ? setdex : {};
    var set = sets[species] && sets[species][name];
    if (!set || set.tr_id === undefined || set.tr_id === null) return null;
    return { tr_id: set.tr_id, set: v, species: species };
  }

  function button() {
    var b = document.getElementById("oxide-fight");
    if (b) return b;
    var after = document.getElementById("edge") || document.getElementById("clear-party");
    if (!after) return null;
    b = document.createElement("div");
    b.id = "oxide-fight";
    b.textContent = "Fight";
    b.title = "Play this party against the trainer on the right, turn by turn, in the OxiDex's Battle tab";
    b.style.cursor = "pointer";
    b.style.display = "none";
    after.parentNode.insertBefore(b, after.nextSibling);
    return b;
  }

  function refresh() {
    var b = button(), clear = document.getElementById("clear-party");
    if (!b || !clear) return;
    var look = getComputedStyle(clear);
    LOOK.forEach(function (k) { b.style[k] = look[k]; });
    b.style.display = look.display === "none" ? "none" : "inline-block";
  }

  $(document).on("click", "#oxide-fight", function () {
    var b = this;
    var party = partySets(), trainer = rightTrainer();
    if (!party.length) { alert("The party is empty."); return; }
    if (!trainer) { alert("Pick a trainer's Pokemon on the right side first."); return; }
    if (b.dataset.busy) return;
    b.dataset.busy = "1";
    b.textContent = "Starting";
    fetch("/api/battle", { method: "POST", headers: { "Content-Type": "application/json" },
                           body: JSON.stringify({ op: "new", source: "calc", party: party, trainer: trainer }) })
      .then(function (r) { return r.json(); })
      .then(function (out) {
        if (out.error) { alert(out.error); return; }
        if (window.parent !== window && typeof window.parent.openBattle === "function") {
          window.parent.openBattle(out.line, 0, out.view);
        } else {
          window.open("/#battle/" + encodeURIComponent(out.line) + "/0", "_blank");
        }
      })
      .catch(function (e) { alert("The OxiDex did not answer: " + e); })
      .then(function () { delete b.dataset.busy; b.textContent = "Fight"; });
  });

  $(function () {
    refresh();
    var clear = document.getElementById("clear-party");
    var party = document.querySelector(".player-party");
    if (window.MutationObserver) {
      if (clear) new MutationObserver(refresh).observe(clear, { attributes: true, attributeFilter: ["style"] });
      if (party) new MutationObserver(refresh).observe(party, { childList: true });
    }
  });
})();
