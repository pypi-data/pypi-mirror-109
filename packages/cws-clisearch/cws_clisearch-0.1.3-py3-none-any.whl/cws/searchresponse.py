"""Search response returned by a provider.

Can contain multiple search results.
"""


class SearchResponse():
    """Represent a search response consisting of multiple results."""

    def __init__(self, results, url_only):
        """Construct the response.

        Args:
            results: The results to build the response from.
        """
        self.results = results
        self.url_only = url_only

    def __repr__(self):
        """Represent as a string."""
        str = ''

        if self.url_only:
            for result in self.results:
                str += f"{result.link}\n"
        else:
            for result in self.results:
                str += f"\n{result}\n-----------------------"

        return str
