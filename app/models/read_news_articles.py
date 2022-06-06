import os

class ReadArticles:
    """
    class to read news articles
    """
    def __init__(self, folder):
        self.folder = folder

    def read_articles(self):
        articles = {}
        for path in os.listdir(self.folder):
            filepath = os.path.join(self.folder, path)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding="utf8") as f:
                    lines = f.readlines()
            articles[str(filepath)] = lines
        return articles
