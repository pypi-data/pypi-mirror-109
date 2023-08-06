"""Google search provider."""
import requests
import json
from cws.provider.searchprovider import SearchProvider
from cws.searchresult import SearchResult
from cws.config import cfg


class Google(SearchProvider):
    """Google search provider.

    Extends the SearchProvider base class to handle Google results.
    """

    search_url = "https://google-search3.p.rapidapi.com/api/v1/search/q={}k&num={}"
    name = 'google'
    headers = {
        'x-rapidapi-key': cfg.tokens[name],
        'x-rapidapi-host': "google-search3.p.rapidapi.com"
    }

    def fetch_request(self, search):
        """Make an API request."""
        if cfg.env == 'prod':
            js = json.loads(
                requests.get(
                    f"{self.search_url.format(search, self.number)}",
                    headers=self.headers,
                ).text
            )
        else:
            with open(cfg.sample_path / f"{self.name}.json", "r") as file:
                js = json.load(file)

        return [SearchResult(search, **i) for i in js['results']]
