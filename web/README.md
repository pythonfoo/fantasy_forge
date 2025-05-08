# fantasy forge, but for the web

## install

```
yarnpkg install
uv run brython-cli add_package fantasy_forge --dest-dir .
# TODO: shouldn't this also add the transitive dependencies?
uv run brython-cli add_package toml --dest-dir .
uv run brython-cli add_package xdg_base_dirs --dest-dir .
uv run brython-cli add_package huepy --dest-dir .
touch ../.venv/lib/python3.13/site-packages/fluent/__init__.py
uv run brython-cli add_package fluent --dest-dir .
uv run brython-cli add_package typing_extensions --dest-dir .
uv run brython-cli add_package babel --dest-dir .
uv run brython-cli add_package attr --dest-dir .
```
