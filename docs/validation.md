# Validation and scope

Validated for this publication:

- Four chapters, 18 quests, 83 unique quest/task/reward/chapter identifiers and an acyclic prerequisite graph.
- Cross-module entry gates match the current course sequence.
- All 21 handbook entries reference an existing category.
- All 133 pinned mod downloads were fetched from the recorded public URLs and matched the original installed files by SHA-256.
- The world export excludes saved player data, inventories, personal statistics, quest/team/claim progress, logs and connection settings.
- CI validates the sources and builds the distributable `.mrpack` without bundling dependency JARs.

Not established by these checks: a fresh launcher import, full client startup with the complete pack, the entire quest path, multiplayer behavior, classroom usability or learning outcomes. Existing screenshots show the local prototype, not a newly recorded acceptance test.

The full dependency profile intentionally preserves the source instance, including optional building and convenience mods. A smaller classroom-specific profile can be prepared after a pilot. Disabled mods and local debugging/decompilation artifacts are not included.
