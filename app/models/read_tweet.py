import json


class ReadTweet:
    """
    This class is to read the tweets
    """

    def read_tweet_from_excel(self, filename):
        with open(filename, 'r', encoding="utf8") as f:
            next(f)
            lines = f.readlines()
        return lines

    def read_tweet_from_json(self, filename):
        f = open(filename, "r")
        data = json.load(f)
        return data["data"]