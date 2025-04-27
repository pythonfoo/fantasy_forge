"""
Make fantasy_forge runnable in a web browser.

This file can't be run with a normal Python interpreter, it needs Brython.
"""

from browser import document, window

from fantasy_forge.main import main

# TODO: perhaps move the initialization to JS,
# so that users see something while Python loads
term = window.Terminal()
term.open(document.getElementById("terminal"))
main()
term.write("main run")
