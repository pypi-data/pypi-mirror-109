"""Base search provider."""
from abc import ABC, abstractmethod
from cws.searchresponse import SearchResponse
from cws.searchresult import SearchResult
from cws.config import cfg


class SearchProvider(ABC):
    """Abstract base for searchproviders."""

    search_url = ''
    headers = {}
    params = {}
    name = ''

    def __init__(self, number, *args, **kwargs):
        """Construct the searchprovider."""
        self.number = number
        try:
            self.default_action = cfg.userconfig['provider'][self.name]['default_action']
        except KeyError:
            pass

    @abstractmethod
    def fetch_request(self, search):
        """Abstract method to fetch requests from an api.

        Should return a list of search results.
        """
        return [SearchResult]

    def search(self, search, url_only):
        """Get results from the provider.

        Calls the internal scrape() to generate a response.

        Args:
            search: The search query to perform.
            url_only: Bool indicating to return urls only.

        Returns:
            SearchResponse: A SearchResponse object with results.
        """
        result_list = self.fetch_request(search)

        return SearchResponse(result_list, url_only)
