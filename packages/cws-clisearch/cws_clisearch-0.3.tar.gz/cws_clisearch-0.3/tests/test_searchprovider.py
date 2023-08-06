"""Test general searchprovider functionality."""
from cws.provider.searchprovider import SearchProvider
from cws.config import cfg


class TestProvider():
    """Test searchproviders."""

    def test_fetch(self, provider_string):
        """Test if fetching requests works."""
        provider = SearchProvider.from_yaml_file(
            cfg.provider_yamls[provider_string]
        )(25)
        result = provider.fetch_request('henk')

        assert isinstance(result, str)
