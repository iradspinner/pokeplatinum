// Oxide patch: upstream's backups/ folder (132 MB of other games' data) was
// not vendored, and this is the one file of it the page loads. No title here
// has a bundled backup, so the page always takes its data from the loader,
// which Oxide points at /api/calc-data.
var backupFiles = {};
