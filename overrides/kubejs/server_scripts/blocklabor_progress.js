const M1_UNLOCK_STAGE = 'm1_stone_unlock'

function syncProgressiveStage(player, server) {
  if (!Platform.isLoaded('progressivestages')) return
  if (!player.stages.has(M1_UNLOCK_STAGE)) return

  // Keeps KubeJS stage progress and ProgressiveStages in sync.
  server.runCommandSilent(`stage grant ${player.username} ${M1_UNLOCK_STAGE}`)
}

PlayerEvents.loggedIn(event => {
  syncProgressiveStage(event.player, event.server)
})
