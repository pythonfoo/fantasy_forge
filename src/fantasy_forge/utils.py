from __future__ import annotations

import ctypes
from pathlib import Path
from string import whitespace
from typing import TYPE_CHECKING, Any

from fantasy_forge.entity import Entity
from fantasy_forge.messages import Messages

SOURCE_FOLDER: Path = Path(__file__).parent.resolve()  # fantasy_forge/src/fantasy_forge
ROOT_FOLDER: Path = SOURCE_FOLDER.parent.parent.resolve()  # fantasy_forge

DATA_FOLDER: Path = ROOT_FOLDER / "data"  # fantasy_forge/data
WORLDS_FOLDER: Path = DATA_FOLDER / "worlds"  # fantasy_forge/data/worlds


# taken from https://stackoverflow.com/a/5948050/2192464
class UniqueDict[K, V](dict[K, V]):
    def __setitem__(self, key: K, value: V):
        if key not in self:
            dict.__setitem__(self, key, value)
        else:
            raise KeyError("Key already exists")


def inflate_contents(
    messages: Messages, contents: list[dict[str, Any]], target: Area | Container
):
    contents_list: list[Entity] = []
    for entity_dict in contents:
        match entity_dict.get("kind", "entity"):
            case "item":
                from fantasy_forge.item import Item

                contents_list.append(Item(messages, entity_dict))
            case "gateway":
                from fantasy_forge.gateway import Gateway

                contents_list.append(Gateway(messages, entity_dict))
            case "key":
                from fantasy_forge.key import Key

                contents_list.append(Key(messages, entity_dict))
            case "enemy":
                from fantasy_forge.enemy import Enemy

                contents_list.append(Enemy(messages, entity_dict))
            case "weapon":
                from fantasy_forge.weapon import Weapon

                contents_list.append(Weapon(messages, entity_dict))
            case "armour":
                from fantasy_forge.armour import Armour

                contents_list.append(Armour(messages, entity_dict))

            case "container":
                from fantasy_forge.container import Container

                contents_list.append(Container(messages, entity_dict))

            case _:
                contents_list.append(Entity(messages, entity_dict))
    for entity in contents_list:
        target.contents[entity.name] = entity


# taken from https://stackoverflow.com/a/15274929/2192464
def terminate_thread(thread):
    """Terminates a python thread from another thread.

    :param thread: a threading.Thread instance
    """
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def clean_filename(filename: str) -> str:
    result = []
    for char in filename.casefold():
        if char.isalnum():
            result.append(char)
        elif char in whitespace:
            result.append("_")
        else:
            continue
    return "".join(result)


if TYPE_CHECKING:
    from fantasy_forge.area import Area
    from fantasy_forge.container import Container
