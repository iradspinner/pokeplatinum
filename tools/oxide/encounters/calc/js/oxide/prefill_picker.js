// Oxide patch: opening a species picker starts its search at the species
// already picked, selected, so the other sets of that species (every trainer
// with an Electivire) are one click away, and typing replaces the name.
// Upstream opens it empty. Loaded last, so it needs no change to upstream's
// own scripts; select2 3.4 fires "select2-open" on the picker's input and
// then clears its search box, hence the deferral.
$(document).on("select2-open", ".set-selector", function () {
  var value = String($(this).val() || "");
  var cut = value.indexOf(" (");
  var species = cut > 0 ? value.slice(0, cut) : value;
  if (!species) return;
  setTimeout(function () {
    var input = $(".select2-drop-active .select2-input");
    if (!input.length) return;
    input.val(species).trigger("keyup-change");
    input[0].select();
  }, 0);
});
