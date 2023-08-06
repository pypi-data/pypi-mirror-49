import unittest

from scrapping import spider
from scrapping import data_handler
from scrapping.requests import Request

# import logging
# logging.basicConfig(level=logging.DEBUG)

class IMDbTopRatedMoviesSpider(spider.BaseSpider):
    urls = ['https://www.imdb.com/chart/top']
    data_handlers = [data_handler.JsonDataHandler()]

    def parse(self, response, html):
        films_list = html.select('tbody.lister-list')[0]
        # print(archive_list)
        for film in films_list.find_all('tr')[:10]:
            # print('parsing data')
            name = film.select('.titleColumn a')[0].get_text()
            link = "https://imdb.com" + film.select('.titleColumn a')[0].get('href')
            year = film.select('.titleColumn span')[0].get_text()[1:-1]
            rating = film.select('.ratingColumn.imdbRating')[0].get_text()

            yield {
                'name': name,
                'link': link,
                'year': year.encode('utf-8').decode('utf-8'),
                'rating': rating.encode('utf-8').decode('utf-8').strip(),
            }


class MovieFone2019ReleasesSpider(spider.BaseSpider):
    urls = ['https://www.moviefone.com/movies/']
    data_handlers = [data_handler.JsonDataHandler()]

    def parse(self, response, html):
        movies_list = html.select('.movie-list.body-inner')[0]
        for film in movies_list.select('li'):
            # name = film.select('.movie-title')[0].get_text()
            # score = film.select('.tMeterScore')[0].get_text()
            rating = film.select('.rating')[0].get_text()
            link = film.select('.movie-title')[0].get('href')
            release = film.select('.available-text')[0].get_text()

            yield {
                # 'name': name,
                'rating': rating,
                # 'score': score,
                'link': link,
                'release': release,
            }

class ItsFossLastPostCrawler(spider.BaseSpider):
    urls = ['https://itsfoss.com/category/list/']
    data_handlers = [data_handler.JsonDataHandler()]

    def parse(self, response, html):
        posts_list = html.select('#genesis-content article')

        for post in posts_list:
            title = post.select('header h2')[0].get_text()
            link = post.select('header h2 a')[0].get('href')
            tags = dict([(tag.get_text(), tag.get('href')) for tag in post.select('footer .entry-tags a')])

            yield Request(link, parser=self.parse_post)

            yield {
                'type': 'short',
                'title': title,
                'link': link,
                'tags': tags,
            }

    def parse_post(self, response, html):
        title = html.select('header.entry-header h1')[0].get_text()
        url = response._url
        author = html.select('span.entry-author')[0]
        author_link = author.select('a')[0].get('href')
        author_name = author.get_text()
        comments = html.select('.entry-comments-link a')[0].get('href')
        content = html.select('.entry-content')[0].get_text()

        yield {
            'title': title,
            'url': url,
            'author': {
                str(author_name): author_link
            },
            'comments': comments,
            'content': content,
        }


# class BaseSpiderTest(unittest.TestCase):
#     def setUp(self):
#         self.spider = ItsFossLastPostCrawler()
#
#     def test_start(self):
#         self.spider.start()
