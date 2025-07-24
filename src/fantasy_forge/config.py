from dataclasses import dataclass


@dataclass
class Config:
    world = "data/worlds/chaosdorf"
    name = "Player"
    description = "the heroic player"
    logfile = "fantasy_forge.log"
    loglevel = "INFO"
