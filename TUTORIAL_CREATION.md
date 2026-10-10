# Tutorial Datadisk Creation Summary

This document summarizes the creation of the **ishtaria-datadisk-tutorial** repository.

## Repository Structure Created

```
ishtaria-datadisk-tutorial/
├── datadisk.yaml           # Datadisk manifest
├── README.md              # Documentation
├── TUTORIAL_CREATION.md   # This file
├── Makefile               # Development commands
├── .gitignore             # Git ignore rules
├── voice/
│   └── voices.yaml        # Voice configuration
├── tools/
│   └── render_voices.py    # Voice rendering script
├── places/
│   └── tutorial_island.yaml # 9 tutorial zones
├── npcs/
│   └── tutors.yaml        # 9 NPCs (7 tutors + merchant + practice animals)
├── dialogues/
│   ├── alara_intro.yaml   # Movement/UI tutor
│   ├── crafton.yaml       # Gathering/crafting tutor
│   ├── valerian.yaml      # Combat tutor
│   ├── hammerin.yaml      # Building tutor
│   ├── merchan.yaml       # Trading tutor
│   ├── arcanis.yaml       # Magic tutor
│   ├── portalus.yaml      # Portal/federation tutor
│   └── tutorial_merchant.yaml # Functional merchant
├── quests/
│   └── tutorial_chain.yaml # 6 progressive tutorial quests
├── i18n/
│   ├── en.yaml            # English translation
│   └── cs.yaml            # Czech translation
└── debian/
    ├── control           # Package control file
    ├── changelog         # Package changelog
    ├── copyright          # License information
    ├── rules             # Build rules
    ├── install           # Installation file
    └── source/
        └── format        # Source format
```

## Features Demonstrated

The tutorial datadisk showcases **all implemented Ishtaria features** through:

### 1. Movement and UI (Alara - Newcomer's Beach)
- Basic WASD movement
- Mouse look controls
- E key interaction
- HUD overview (health, stamina, mana, inventory)
- Minimap navigation
- Stamina system (consumption, regeneration, exhaustion)

### 2. Gathering and Crafting (Crafton - Harvest Grove)
- Tool selection (axe, pickaxe)
- Resource gathering from trees and rocks
- Tool durability system
- Crafting recipes
- Station-based crafting (campfire, anvil)
- Inventory management

### 3. Combat and Hunting (Valerian - Training Grounds)
- Weapon use (sword, shield)
- Attack and block mechanics
- Combat with practice animals (wolf, bear)
- Damage and health system
- Armour and damage reduction
- Weapon types and stats

### 4. Building and Placement (Hammerin - Builder's Yard)
- Object placement from inventory
- Campfire, bench, and other placeable items
- Terrain validation for placement
- Building basics

### 5. Trading and Economy (Merchan - Market Square)
- Merchant buying and selling
- Gold as currency
- Daily merchant limits
- Player-to-player trading introduction
- Tutorial merchant with basic supplies

### 6. Magic System (Arcanis - Mage's Tower)
- Mana system and regeneration
- Spell learning from scrolls
- Spell casting (Refresh, Firebolt, Healing Hands, Ward)
- Mana management

### 7. Federation and Portals (Portalus - Portal Plaza)
- Portal system explanation
- Federation concepts
- World travel mechanics
- Connecting to other servers

## Tutorial Progression

The datadisk includes a **guided quest chain** that takes players through all features:

1. **Tutorial Welcome** (Alara)
   - Meet Alara
   - Learn movement and controls
   - Understand stamina
   - Reward: 100 XP

2. **Tutorial Gathering** (Crafton)
   - Meet Crafton
   - Gather 5 pine logs
   - Craft 10 pine wood planks
   - Reward: 200 XP + 25 gold

3. **Tutorial Combat** (Valerian)
   - Meet Valerian
   - Defeat 1 practice wolf
   - Reward: 300 XP + 30 gold

4. **Tutorial Building** (Hammerin)
   - Meet Hammerin
   - Place 1 campfire
   - Reward: 250 XP

5. **Tutorial Trading** (Merchan)
   - Meet Merchan
   - Buy 1 bread from merchant
   - Reward: 200 XP + 20 gold

6. **Tutorial Magic** (Arcanis)
   - Meet Arcanis
   - Learn Refresh spell
   - Cast first spell
   - Reward: 350 XP

7. **Tutorial Final** (Portalus)
   - Meet Portalus
   - Complete all tutorials
   - Reward: 500 XP + 100 gold

**Total Rewards**: 1900 XP + 175 gold

## Localization

- **English**: Complete translation for all dialogue
- **Czech**: Complete translation for all dialogue
- All text keys follow the pattern: `character.action` or `quest.id.stage`
- Voice synthesis ready with Piper TTS configuration

## Development Commands

```bash
# Validate the datadisk
make test

# Render voice lines (requires Piper and FFmpeg)
make voices

# Stage for local testing
make stage

# Start local server with this datadisk
make server

# Stop the server
make stop

# View server logs
make logs

# Clean build artifacts
make clean

# Build Debian package
dpkg-buildpackage -us -uc -b

# Build without voices (faster)
dpkg-buildpackage -us -uc -b -P novoice
```

## Asset Requirements

To complete the datadisk, you need to create:

### Portraits (media/portraits/)
- alara.jpg (Movement tutor)
- crafton.jpg (Gathering tutor)
- valerian.jpg (Combat tutor)
- hammerin.jpg (Building tutor)
- merchan.jpg (Trading tutor)
- arcanis.jpg (Magic tutor)
- portalus.jpg (Portal tutor)
- merchant.jpg (Tutorial merchant)
- wolf.jpg (Practice wolf)
- bear.jpg (Practice bear)

### Cover Image (media/cover/)
- cover.jpg (1024x768 recommended)

### Background Music (media/music/)
- peaceful.ogg (Newcomer's Beach)
- forest.ogg (Harvest Grove)
- combat.ogg (Training Grounds)
- building.ogg (Builder's Yard)
- market.ogg (Market Square)
- magic.ogg (Mage's Tower)
- mysterious.ogg (Portal Plaza)
- graveyard.ogg (Tutorial Graveyard)

### Voice Lines (media/voice/<lang>/)
- Generated automatically by `make voices` using Piper TTS
- English: en_US-libritts_r-medium model
- Czech: cs_CZ-jirka-medium model

## Integration with Ishtaria

1. **Install the datadisk**:
   ```bash
   dpkg -i ishtaria-datadisk-tutorial_0.1.0_all.deb
   ```

2. **Generate a world with the tutorial**:
   - In `ishtaria-admin`: Select tutorial datadisk when generating map
   - Or use: `ishtaria-server-init <seed> <size> tutorial`

3. **Update AGENTS.md**:
   Add the tutorial datadisk to the repository map:
   ```
   | `ishtaria-datadisk-tutorial` | Tutorial story datadisk demonstrating all features | [README](ishtaria-datadisk-tutorial/README.md), `places/`, `npcs/` |
   ```

## Technical Details

- **Datadisk ID**: tutorial
- **Version**: 0.1.0
- **License**: CC BY-SA 4.0
- **Rating**: everyone
- **Languages**: en, cs
- **Dependencies**: ishtaria-server, piper-tts, ffmpeg (for voice rendering)

## Notes

- The datadisk is designed to be **standalone** - it doesn't require any other datadisks
- All content is **open source** under CC BY-SA 4.0
- Voice synthesis is **optional** - can be built without voices using novoice profile
- The tutorial is **progressive** - players can complete at their own pace
- All tutors are **static NPCs** - they don't move or follow players
- Practice animals are **passive** - they only fight back if attacked
