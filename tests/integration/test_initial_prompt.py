from icommandlib import ICommand
from commandlib import python_bin
from pathlib import Path

p = Path("src/fantasy_forge/__main__.py")

process = ICommand(python_bin.python(p.absolute())).run()
process.wait_until_output_contains("Please name your character:")
process.send_keys("moverm eyer\n")
process.wait_until_on_screen("> ")
Path("stripshot.txt").write_text(process.stripshot())