"""Test cws configuration."""
from cws.config import Cfg


class TestConfig():
    """Test the cws config."""

    def test_tokenfile(self, token_file):
        """Test token file scenario's."""
        cfg = Cfg()

        assert cfg.token_file == token_file

    def test_userconffile(self, userconf_file):
        """Test userconfig scenario's."""
        cfg = Cfg()

        assert cfg.userconfig_file == userconf_file
