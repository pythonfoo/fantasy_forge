import ctypes
from pathlib import Path
from string import whitespace

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
