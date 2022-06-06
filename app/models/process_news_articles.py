from app.models.read_news_articles import ReadArticles


class ProcessArticles:
    """
    this class is to process news articles
    """
    def __init__(self, folder):
        self.read_obj = ReadArticles(folder)

    def process_articles(self):
        articles = self.read_obj.read_articles()
        article_map = []
        for _, article in articles.items():
            title, source, body = article[0].strip(), article[1].strip(), "\\n".join(article[2:])
            title = title[6:].strip()
            source = source[7:].strip()
            body = body.replace("\n", "\\n")
            article_map.append({"Title": title, "Source": source, "Content": body})
        return article_map