# Fantasy Forge (working title)

## Let's Go!

Clone the repo, change into the directory, and run `uv run -m fantasy_forge` to start the game. `uv` will create a fitting virtualenv for you. You can install [uv](https://astral.sh/blog/uv) using [pipx](https://github.com/pypa/pipx).

So initially, if you don't have it:

```bash
pipx install uv
git clone https://github.com/pythonfoo/fantasy_forge
```

And to start:

```bash
cd fantasy_forge
# call the module
uv run -m fantasy_forge
# or run the command
uv run fantasy-forge
```

You can also set a debug level to write debugging output to `./fantasy_forge.log`.


## Development


### pre-commit

See [pre-commit docs](https://pre-commit.com/) and the [ruff-hook](https://github.com/astral-sh/ruff-pre-commit)

```bash
# Install `pre-commit` with e.g.
pipx install pre-commit
# install the pre-commit file (.pre-commit-config.yaml) with
pre-commit install
# run it (perhaps multiple times), to see if everything works
pre-commit run --all-files
```


### Tests (TBD :D)

Unittests via [pytest](https://docs.pytest.org/) live in `./tests/unittests`

Integration tests via [hitchstory](https://hitchdev.com/) and pytest are in `./tests/integration`
