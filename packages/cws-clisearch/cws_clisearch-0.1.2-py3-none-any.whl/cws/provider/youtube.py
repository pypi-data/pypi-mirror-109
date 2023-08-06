"""Youtube search provider."""
import requests
import json
from cws.provider.searchprovider import SearchProvider
from cws.searchresult import SearchResult
from cws.config import cfg


class Youtube(SearchProvider):
    """Youtube search provider.

    Extends the SearchProvider base class to handle Youtube results.
    """

    name = 'youtube'
    search_url = "https://youtube-search-results.p.rapidapi.com/youtube-search/"
    headers = {
        'x-rapidapi-key': cfg.tokens[name],
        'x-rapidapi-host': "youtube-search-results.p.rapidapi.com"
    }

    def fetch_request(self, search):
        """Make an API request."""
        if cfg.env == 'prod':
            js = json.loads(
                requests.get(
                    self.search_url,
                    headers=self.headers,
                    params={
                        "q": search,
                    }
                ).text
            )
        else:
            with open(cfg.sample_path / f"{self.name}.json", 'r') as file:
                js = json.load(file)

        videos = []
        videocount = 0
        for item in js['items']:
            if videocount >= self.number:
                continue
            if item['type'] == 'video':
                videos.append(item)
                videocount += 1

        return [
            SearchResult(
                search,
                title=i['title'],
                description=i['duration'],
                link=i['url']
            ) for i in videos
        ]
