// M4-C Beispiel: einfacher Event-Hook
// Datei in kubejs/server_scripts/

PlayerEvents.loggedIn(event => {
  event.player.tell('KubeJS Event-Hook aktiv. Willkommen!')
})
