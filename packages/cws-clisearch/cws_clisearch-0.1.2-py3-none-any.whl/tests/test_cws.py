"""Test the cws object."""
import pytest
from cws.cws import Cws
from cws.provider.searchprovider import SearchProvider
from cws.searchresponse import SearchResponse


class TestCws():
    """Test the cws object."""

    @pytest.mark.parametrize("search,expected", [
        ('henk', 'henk'),
        (['henk', 'ding'], 'henk ding'),
    ])
    def test_construction(self, search, expected, provider_string):
        """Test the object construction."""
        cws = Cws(False, provider_string, search, 25)

        assert isinstance(cws.provider, SearchProvider)
        assert cws.searchtext == expected

    def test_search(self, provider_string):
        """Test searching."""
        cws = Cws(False, provider_string, 'henk', 25)

        assert isinstance(cws.start_search(), SearchResponse)
