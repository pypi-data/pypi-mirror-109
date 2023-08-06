"""CLI web search."""
from cws.provider.google import Google
from cws.provider.youtube import Youtube


class Cws():
    """Main object.

    High-level interface to interact with CLI web search.
    """

    providers = {
        'google': Google,
        'youtube': Youtube,
    }

    def __init__(self, url_only, provider, search, number):
        """Construct the CLI web search object.

        Args:
            url_only: Output setting
            provider: String identifier of search provider
            search: Search query as a list of strings
            number: Number of search results to return
        """
        self.url_only = url_only
        self.provider = self.providers[provider](number)
        self.search = search
        self.number = number
        if isinstance(search, str):
            self.searchtext = search
        else:
            self.searchtext = ' '.join(self.search)

    def start_search(self):
        """Use a given searchprovider to search.

        Returns:
            SearchResponse: A search response returned by the searchprovider
        """
        return self.provider.search(self.searchtext, self.url_only)
