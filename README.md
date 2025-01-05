# Fantasy Forge (working title)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Fantasy Forge is a framework for creating and playing text adventure games. The game data is stored in toml files. It is planned that the framework will work separately from the game and the content can be exchanged. It is currently still in an early stage of development, if you want to try it out follow the installation instructions.

## Let's Go

If you don't have it, install [uv](https://astral.sh/blog/uv) using [the installer](https://docs.astral.sh/uv/getting-started/installation/) or, if you have it, [pipx](https://github.com/pypa/pipx).

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pipx install uv
```

Clone the repo, change into the directory, and run `uv fantasy-forge` to start the game. `uv` will create a fitting virtualenv for you.

```bash
# clone the repo
git clone https://github.com/pythonfoo/fantasy_forge
cd fantasy_forge
# run the command
uv run fantasy-forge
# or call the module
uv run -m fantasy_forge
```

You can set a debug level to write debugging output to `./fantasy_forge.log`.

## Development

Contributions are very welcome <3. Please commit one thing at a time to keep things simple and neat. We'll probably have a look at them during pythonfoo, if you don't mind.

### pre-commit

If you installed `uv`, you can use [uvx](https://docs.astral.sh/uv/guides/tools/#running-tools) to install [pre-commit](https://pre-commit.com/).
Pre-commit checks, among other things, that the code doesn't contain syntax errors and is [well formatted](https://github.com/astral-sh/ruff-pre-commit).

```bash
# install `pre-commit`
uvx install pre-commit
# install the pre-commit file (.pre-commit-config.yaml) with
pre-commit install
# run it (perhaps multiple times), to see if everything works
pre-commit run --all-files
```

### Tests (TBD :D)

Unittests via [pytest](https://docs.pytest.org/) live in `./tests/unittests`

Integration tests via [hitchstory](https://hitchdev.com/) and pytest are in `./tests/integration`
