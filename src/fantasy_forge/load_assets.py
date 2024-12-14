from pathlib import Path
from typing import Any

from fantasy_forge.area import Area
from fantasy_forge.armour import Armour
from fantasy_forge.character import Character
from fantasy_forge.container import Container
from fantasy_forge.enemy import Enemy
from fantasy_forge.entity import Entity
from fantasy_forge.gateway import Gateway
from fantasy_forge.inventory import Inventory
from fantasy_forge.item import Item
from fantasy_forge.key import Key
from fantasy_forge.player import Player
from fantasy_forge.weapon import Weapon
from fantasy_forge.world import World

CONSTRUCTORS: dict[str, Any] = {
    "areas": Area,
    "armour":Armour,
    "characters":Character,
    "container":Container,
    "enemies":Enemy,
    "entities":Entity,
    "gateways":Gateway,
    "inventories":Inventory,
    "items":Item,
    "keys":Key,
    "player":Player,
    "weapons":Weapon,
    "world":World,
}

name = "chaosdorf"
world_folder: Path = Path("data/worlds")
world_path = world_folder / name

# load world.toml
world: World = World.load(name)

# load assets
path : Path
for path in world_path.glob("**/*.toml"):
    constructor = CONSTRUCTORS.get(path.parent.name)
    if constructor is None:
        constructor = CONSTRUCTORS.get(path.stem)
    print(f"{constructor} {path.name}")