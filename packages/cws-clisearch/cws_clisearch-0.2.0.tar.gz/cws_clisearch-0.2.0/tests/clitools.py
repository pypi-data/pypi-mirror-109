"""CLI test helper tools."""
from types import SimpleNamespace


def setup_args(
    provider='google',
    number=25,
    url=False,
    env='dev',
    execute=False,
    search='henk',
):
    """Return an argument namespace."""
    return SimpleNamespace(
        provider=provider,
        number=number,
        url=url,
        env=env,
        execute=execute,
        search=search,
    )
