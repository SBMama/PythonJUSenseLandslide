import json

import requests

class TweetScrapper:
    def __init__(self):
        self.header = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAHtZOgEAAAAAguUG5u%2BzYCHNyqbpgwS70a1dMYY%3D0T2OuZB2JES1ZtDzRFVvpNNiMNO2D3khoJfsGTOcXYSCdOrdms"}
        self.url = "https://api.twitter.com/2/tweets/search/all"

    def search(self):
        START_TIME = "2022-05-12T00:00:00Z"
        END_TIME = "2022-05-18T23:59:59Z"
        TWEET_PARAMS = {
            "max_results": 100,
            "start_time": START_TIME,
            "end_time": END_TIME,
            "query": "dima hasao landslide",
            "expansions": "author_id,geo.place_id,attachments.media_keys",
            "tweet.fields": "created_at,geo"
        }
        res = requests.get(url=self.url, params=TWEET_PARAMS, headers=self.header)
        f = open('tweets.json', 'w')
        json.dump(res.json(), f)


if __name__ == '__main__':
    obj = TweetScrapper()
    obj.search()