# Fantasy Forge (working title)

## Let's Go!

Clone the repo, change into the directory, and run `uv run -m fantasy_forge` to start the game. `uv` will create a fitting virtualenv for you. You can install [uv](https://astral.sh/blog/uv) using [pipx](https://github.com/pypa/pipx).

So initially, if you don't have it:

```
pipx install uv
git clone https://github.com/pythonfoo/fantasy_forge
```

And to start:

```
cd fantasy_forge
uv run -m fantasy_forge
```

You can also set a debug level to write debugging output to `./fantasy_forge.log`.


## Tests

Unittests via pytest live in `./tests/unittests`.


Integration tests via hitchstory are in `./tests/integration`
