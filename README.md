# ishtaria-datadisk-tutorial

Tutorial story datadisk for [Ishtaria](https://git.vitexsoftware.com/Ishtaria/ishtaria-docs).
**Open source tutorial content** - CC BY-SA 4.0 license. This datadisk demonstrates all
implemented game features in a guided tutorial experience.

A datadisk is data, not code: places, characters, dialogue trees and scenarios that the Ishtaria
server evaluates. Several datadisks can be combined into one world.

```
datadisk.yaml      manifest (id, version, requires/conflicts, license, rating)
places/            places the world generator finds a site for (tutorial island areas)
npcs/              characters standing at places (tutors, merchants, creatures)
dialogues/         decision trees: tutorials, explanations, feature demonstrations
quests/            tutorial scenarios as stage machines
lore/              tutorial entries (not spawned, for codex)
music/ + media/    background tracks and tutor portraits shown during tutorials
i18n/en.yaml cs.yaml
voice/voices.yaml  voice of each character per language
tools/             helper scripts for asset preparation
```

Format: `ishtaria-protocol/schemas/datadisk.schema.json`. Check the disk (schema, references, media):

```sh
python3 ../ishtaria-protocol/tests/validate_datadisk.py .
```

Install (`dpkg-buildpackage -us -uc -b`, then `dpkg -i`) to `/usr/share/ishtaria/datadisks/tutorial/`.
In `ishtaria-admin`, *World maps → Generate map* then shows a checkbox for this disk; or
`ishtaria-server-init <seed> <size> tutorial`.

## Tutorial Content Overview

The Tutorial World is designed as a single island with multiple zones, each teaching different features:

### Zone 1: Basic Movement and UI
- **Newcomer's Beach**: Spawn point where players learn basic movement and HUD
- **Tutor Alara**: Introduces controls, stamina system, and UI navigation

### Zone 2: Gathering and Crafting
- **Harvest Grove**: Trees, rocks, and plants to gather from
- **Tutor Crafton**: Teaches gathering tools, resource collection, and crafting basics
- **Workbench Area**: Crafting stations for practice

### Zone 3: Combat and Hunting
- **Training Grounds**: Safe area with target dummies
- **Hunting Forest**: Passive animals to practice combat on
- **Tutor Valerian**: Combat instructor

### Zone 4: Building and Placement
- **Builder's Yard**: Area for placing objects
- **Tutor Hammerin**: Building and placement tutor

### Zone 5: Trading and Economy
- **Market Square**: Merchant stalls
- **Tutor Merchan**: Trading and economy tutor
- **Shopkeeper**: Functional merchant for practice

### Zone 6: Magic System
- **Mage's Tower**: Magic training area
- **Tutor Arcanis**: Magic system tutor

### Zone 7: Advanced Features
- **Portal Plaza**: Federation portal demonstration
- **Tutor Portalus**: Portal and federation explainations

### Zone 8: Story-disk placement
- **Surveyor's Rise**: measured from the village (`locate`), with a landscape patch and a wildlife overlay
- **Survey Cairn**: a surveyed point (`tolerance_m: 0`) and a walkable structure shipped with the disk
- **Surveyor**: patrols a square, stands taller than the model (`size`), and explains the lesson
- **Apprentice, elder and child**: wander; the three share one short greeting. The child is fast enough that the client plays Run
- The cover jingle and the music away from every place are the disk's `cover_music` and `ambient_music`

The tutorial does not ship a real planet and does not fix the player's body. A disk that does (`world.terrain`, `geo`, `player_character`, `player_model`, `player_body`) cannot be combined with another planet disk, and it takes the character choice away. Surveyor explains those, and this disk stays combinable with one.

## Features Demonstrated

- Movement: walking, running, stamina consumption
- Gathering: trees, rocks, plants with appropriate tools
- Crafting: recipes, stations, inventory management
- Combat: hunting, damage, armour, weapons
- Building: placing objects, structure construction
- Trading: merchant buying/selling, player-to-player
- Magic: mana, spells, scrolls
- Social: friends, events, nearby players
- Survival: health, stamina, water, food
- Drinking: fountains and water sources
- Equipment: tools, weapons, armour slots
- Durability: tool degradation
- Quests: tutorial quest chains
- Chat: communication with other players
- Graveyards: permanent memorials
- Hall of Fame: achievements and scores
- Story placement: a site measured from another place, a surveyed point, a landscape patch, a structure, a wildlife overlay
- Walking characters: a patrol, wanderers who share one dialogue, and a taller body
- Disk music: a cover jingle and the ambient track heard outside every place

## Spoken Lines

`dpkg-buildpackage` runs `tools/render_voices.py`: every NPC line is synthesized with Piper
and encoded to OGG Vorbis in `media/voice/<language>/<text_key>.ogg`. Build-Depends include
`piper-voice-cs-cz-jirka-medium` and `piper-voice-en-us-libritts-r-medium`
(`/usr/share/piper/voices/`).

`dpkg-buildpackage -P pkg.ishtaria-datadisk-tutorial.novoice` skips the rendering.

## Music

Tutorial zones use CC0 background music tracks appropriate to each area.

## Asset Requirements

Character portraits for tutors should be created and placed in `media/portraits/`.
A cover image should be created for `media/cover/cover.jpg` (1024x768 recommended).

## Development

```sh
make test     # validate the datadisk
make stage    # stage for local testing
make server   # start local server with this datadisk
make stop     # stop the server
make clean    # clean build artifacts
```

## License

CC BY-SA 4.0. All content is open source and can be modified and shared under the
same license terms.
