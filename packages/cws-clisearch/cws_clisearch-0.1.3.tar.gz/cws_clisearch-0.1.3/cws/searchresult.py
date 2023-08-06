"""Represents a search result."""


class SearchResult():
    """Represent an individual searchresult that cws can handle."""

    def __init__(self, search, **kwargs):
        """Construct an individual searchresult.

        Args:
            search: Searchquery used to get this result
            kwargs: Dictionary of result data
        """
        self.search = search
        self.title = kwargs['title']
        self.description = kwargs['description']
        self.link = kwargs['link']

    def __repr__(self):
        """Represent the result as a string."""
        return f"{self.title} - {self.link}\n-\n{self.description}"
