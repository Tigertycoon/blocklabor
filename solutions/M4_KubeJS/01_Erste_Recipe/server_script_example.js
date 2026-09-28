// M4-B Beispiel: kleine Recipe-Aenderung
// Datei in kubejs/server_scripts/

ServerEvents.recipes(event => {
  // Beispiel: 1 Cobblestone -> 1 Gravel
  event.shapeless('minecraft:gravel', ['minecraft:cobblestone'])
})
