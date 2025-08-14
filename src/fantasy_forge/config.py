from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Self

import toml
from xdg_base_dirs import xdg_config_home


@dataclass
class Config:
    world = "data/worlds/chaosdorf"
    name = "Player"
    description = "the heroic player"
    logfile = "fantasy_forge.log"
    loglevel = "INFO"

    def user_config() -> dict[str, Any]:
        config_file = xdg_config_home() / "fantasy_forge.toml"

        if not config_file.exists():
            config_file.touch()

        with config_file.open() as file:
            config = toml.load(file)

        return config

    def read() -> Config:
        user_config = Config.user_config()
        config = Config()
        config_options = dir(Config)
        for option in config_options:
            if option in user_config:
                setattr(config, option, user_config[option])

        return config

    def save(self: Self):
        config_file = xdg_config_home() / "fantasy_forge.toml"

        with config_file.open("w") as file:
            toml.dump(self.__dict__, file)

        return
