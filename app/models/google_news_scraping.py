import requests
from bs4 import BeautifulSoup
from PIL import Image
from pygooglenews import GoogleNews


class NewsScrapper:
    def __init__(self):
        gn = GoogleNews()  # google news scrapper object
        # search google news articles that contain dima hasao landslide
        self.landslides = gn.search('dima+hasao+landslide')

    def __get_content_metadata(self, article):
        # get the title of the article
        title = article.get('title')
        # get the source url of the article
        link = article.get('link')
        return title, link

    def __save_image(self, article_number, images):
        image_number = 1  # initialize image number to be used for unique image identifier
        alt_map = {}  # to store the image title(alt) for all images
        for image in images:
            image_url, alt = self.__get_image_details(image)  # get image url and alt value
            alt_map[image_number] = alt  # map alt value to image number
            # in case it is not a complete url for image, ignore saving the image,
            # but the image alt is stored
            if not (image_url.startswith("https://") or image_url.startswith("http://")):
                print(f"Invalid image url {image_url}")
                continue
            image_number = self.__format_and_store_image(image_url, image_number, article_number)
        return alt_map

    def __get_image_details(self, image):
        try:
            image_url = image['src']  # src or url of the image
            alt = image.get('alt', "")  # alt attribute of image tag
        except:
            image_url = ""
            alt = ""
        return image_url, alt

    def __format_and_store_image(self, image_url, image_number, article_number):
        try:
            # do a get call to the image url and load the image as an RGB image
            img = Image.open(requests.get(image_url, stream=True).raw).convert('RGB')
            # get size of image
            width, height = img.size
            # if the image is too small, getting useful info from the image is not possible,
            # so the image is ignored
            if width < 100 or height < 100:
                print("image too small")
            else:
                # save image
                img.save('..//data//images//image_' + str(image_number) +
                         '_for_article_' + str(article_number) + '.jpg')
                # increment image number only if image is successfully formatted and saved
                image_number += 1
        except Exception as e:
            print(f"error in parsing or saving image {str(e)}")
        return image_number  # return the next expected image number

    def __save_content(self, article_number, paragraphs, fig_caption, alt, title, link):
        # get all the text contained enclosed in <p></p> tags
        content = '\n'.join([para.string for para in paragraphs])
        content = content.strip()
        if not content:  # if there is no such content
            print(f"Empty file content {content}")
        # get all  figure captions enclosed in <figcaption></figcaption> tag
        figure_contents = '\n'.join([caption.string for caption in fig_caption])
        # save the content to file
        f = open("..//data//news_articles" + str(article_number) + ".txt", "w", encoding="utf8")
        f.write("Title: " + title + "\n")
        f.write("Source: " + link + "\n")
        f.write(content)
        if figure_contents:  # if figure captions exists, save figure caption to file
            f.write(figure_contents)
        if alt:  # if images exist, save the "alt" attribute of images to file
            alt_content = '\n'.join([alt[k] for k in alt])
            f.write("\n Image Captions: \n")
            f.write(alt_content)
        f.close()

    def __get_html(self, link):
        # do a get call to retrieve the bare html content from url
        try:
            html = requests.get(url=link)
        except:
            raise Exception(f"error in get call to url {link}")
        return html

    def __soup_operations(self, html):
        # create a beautiful soup object
        soup = BeautifulSoup(html.content, 'html5lib')
        # get all <p></p> tags
        paragraphs = soup.findAll('p', text=True)
        # get all <figcaption></figcaption> tags
        figcaption = soup.findAll('figcaption')
        # get all <img></img> tags
        images = soup.findAll('img')
        return paragraphs, images, figcaption

    def driver(self):  # driver function for news scraping from google news
        # initialize article number to be used for unique article identifier
        # and unique image identifier
        article_number = 1
        for article in self.landslides['entries']:
            try:
                title, link = self.__get_content_metadata(article)
                html = self.__get_html(link)
                paragraphs, images, fig_caption = self.__soup_operations(html)
                alt_map = {}#self.__save_image(article_number, images)
                self.__save_content(article_number, paragraphs, fig_caption, alt_map, title, link)
                # increment article number only if all processing for the article has
                # been completed successfully
                article_number += 1
            except Exception as e:
                print(f"Error working with {title} \n {link} \n Error Message: {str(e)}")


if __name__ == '__main__':
    obj = NewsScrapper()
    obj.driver()
