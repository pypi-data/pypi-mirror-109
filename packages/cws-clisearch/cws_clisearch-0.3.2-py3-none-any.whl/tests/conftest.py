"""Fixtures and config for pytest."""
import pytest
import os
from cws.config import cfg

cfg.env = 'dev'


@pytest.fixture(scope='function', params=[i for i in cfg.provider_yamls])
def provider_string(request):
    """Provide string representation of every provider."""
    provider = request.param

    return provider


@pytest.fixture(scope='function')
def home_fixt(tmpdir_factory):
    """Fixture for a home directory and xdg_home directory."""
    home_dir = tmpdir_factory.mktemp('home')
    home_dir.mkdir('.config')

    os.environ['HOME'] = str(home_dir)
    os.environ['XDG_HOME'] = str(home_dir / '.config')

    return home_dir


@pytest.fixture(scope='function')
def token_file(home_fixt):
    """Return a homedir filled with an empty token file."""
    token_file = home_fixt / cfg.token_filename
    token_file.open(mode='w')

    return token_file


@pytest.fixture(scope='function')
def userconf_file(home_fixt):
    """Return a homedir filled with an empty token file."""
    user_file = home_fixt / cfg.userconfig_filename
    user_file.open(mode='w')

    return user_file
