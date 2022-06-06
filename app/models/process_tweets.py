import datetime

from app.models.read_tweet import ReadTweet


class ProcessTweet:
    """
    This class is for pre-processing and processing of tweets
    """
    def __init__(self, filename):
        """
        constructor
        """
        self.read_tweet = ReadTweet()
        self.filename = filename

    def map_tweets_from_excel(self):
        data = self.read_tweet.read_tweet_from_excel(filename=self.filename)
        tweet_map = []
        for line in data:
            elements = line.split(",")
            tweet_id, tweet_text, tweet_date = elements[0], elements[1:-4], elements[-2]
            tweet_text = " ".join(tweet_text)
            if tweet_text.startswith('"'):
                tweet_text = tweet_text[1:]
            if tweet_text.endswith('"'):
                tweet_text = tweet_text[:-1]
            tweet_map.append({"id": tweet_id, "text": tweet_text.lower(), "date": tweet_date})
        return tweet_map

    def map_tweets_from_json(self):
        data = self.read_tweet.read_tweet_from_json(filename=self.filename)
        tweet_map = []
        for tweet in data:
            tweet_id, tweet_text = tweet["id"], tweet["text"]
            tweet_date = datetime.datetime.strftime(datetime.datetime.strptime(tweet["created_at"][:10], "%Y-%m-%d"),
                                              "%d/%m/%Y")
            attachments = tweet.get("attachments", None)
            has_media = "Yes" if attachments else "No"
            tweet_map.append({"id": tweet_id, "text": tweet_text.lower(), "date": tweet_date, "has_media": has_media})
        return tweet_map




    def filter_tweets(self, tweet_map, text=None, date=None):
        filtered_tweets = []
        if text:
            text = text.lower()
            text = text.split(",")
            for tweet in tweet_map:
                for t in text:
                    if t in tweet["text"]:
                        filtered_tweets.append(tweet)
                        break
        if filtered_tweets:
            tweet_map = filtered_tweets
        if date:
            filtered_tweets = []
            date = date.lower()
            for tweet in tweet_map:
                if date in tweet["date"].lower():
                    filtered_tweets.append(tweet)
        return filtered_tweets


if __name__ == '__main__':
    filename = "C:\\Users\\HP\\Desktop\\landslide\\landslide\\landslide.csv"
    obj = ProcessTweet(filename=filename)
    print(obj.map_tweets_from_excel())