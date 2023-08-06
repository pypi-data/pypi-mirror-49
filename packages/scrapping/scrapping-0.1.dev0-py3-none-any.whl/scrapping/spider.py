import types

from bs4 import BeautifulSoup

from multiprocessing.dummy import Pool as ThreadPool

from .requests import Request
from .requests import Method



import logging
logger = logging.getLogger(__name__)
FORMAT = '[%(levelname)s] %(asctime)s / %(name)s:%(funcName)s|%(process)d - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

class BaseSpider:
    """
    Basic simple spider

    Right in class you can specify such arguments:
        urls - list of str urls.

        data_handlers - list of data handlers. The data from parsing function goes right there.

        workers - number of workers in the Pool.

    You can overload such functions:
        parse(self, request, html) - parse data here. This method accepts scrapping.requests.Request and bs4.BeautifulSoup arguments.

        get_requests(self) - if you don't have prepared urls to parse find them here and return as scrapping.requests.Request object. Other data types would be ignored.
    """
    workers = 5
    urls = []
    data_handlers = []
    name = None

    def __init__(self, urls=None, name=None, workers=None, data_handlers=None):
        self.urls = urls if urls else self.urls
        self.workers = workers if workers else self.workers
        self.data_handlers = data_handlers if data_handlers else self.data_handlers
        self._stored_requests = []

        self.name = name if name else self.name
        if not self.name:
            self.name = self.__class__.__name__

        # self.logger = logging.getLogger('spider.BaseSpider')
        self.logger = logging.getLogger(self.name)

        # if

    def get_requests(self):
        """
        Use this method to navigate through requests/links

        return/yield:
            scrapping.requests.Request object

        Note: if parsing function is not specified the default one will be used
        """
        return list(map(lambda url: Request(url), self.urls))

    def parse(self, request, html):
        """
        Default parsing function

        return/yield:
            dict with parsed data
            scrapping.requests.Request object
        """
        self.logger.warning("{} for {} parse method empty! Returning None.".format(self.name, request._url))

    def start(self):
        "Starts crawling"
        self.logger.info("{} started!".format(self.name))
        # for storing the data open data handlers
        self.open_data_handlers()

        for request in self.get_requests():
            # check if they are real Request obj and have parser
            if isinstance(request, Request):
                if not request.parser:
                    request.parser = self.parse
                self._stored_requests.append(request)

        self.pool = ThreadPool(self.workers)
        # all requests are parsed paralelly
        ret_items = self.pool.map(self._handle_request, self._stored_requests)
        # print(ret_items)
        # self.logger.debug('here 1 {}'.format(ret_items))
        # wait untill all first done
        self.pool.close()
        self.pool.join()
        # unpack returned packed objects from pool
        ret_items = self._unpack_packed(ret_items)
        self._save_ret_items_data(ret_items)

        # self.logger.debug('here 2 {}'.format(ret_items))
        # if any other return Request obj handle that
        while any(ret_items):
            # clean the list, only Requests left
            ret_requests = list(filter(lambda item: isinstance(item, Request), ret_items))

            for request in ret_requests:
                if not request.parser:
                    request.parser = self.parse
            self.pool = ThreadPool(self.workers)
            # all requests are parsed paralelly
            ret_items = list(self.pool.map(self._handle_request, ret_requests))
            # unpack returned packed objects from pool
            ret_items = self._unpack_packed(ret_items)
            self._save_ret_items_data(ret_items)
            # wait untill all first done
            self.pool.close()
            self.pool.join()

        self.close_data_handlers()

    def _unpack_packed(self, i):
        "Unpacks all packed urls (lists) in given iterable object"
        for obj in i:
            if isinstance(obj, list):
                i.extend(obj)
                i.remove(obj)
        return i

    def _handle_request(self, request):
        # prepare data to parse and call the parser
        request.join()
        bs_obj = BeautifulSoup(request.text, 'lxml')
        ret = request.parser(request, bs_obj)
        # handle data returned by yield
        if isinstance(ret, types.GeneratorType):
            items = list(filter(lambda item: isinstance(item, dict) or isinstance(item, Request), ret))
            return items
        else:
            return ret if isinstance(ret, dict) or isinstance(ret, Request) else None

    def _save_ret_items_data(self, items):
        "Handle every parsed data in returned sequence"
        for item in items:
            if isinstance(item, dict):
                self.handle_data(item)

    def handle_data(self, data):
        "Gives data to data_handlers"
        self.logger.debug("DATA: {}".format(data))
        for handler in self.data_handlers:
            handler.process(data)

    def open_data_handlers(self):
        for handler in self.data_handlers:
            handler.setUp(self)
            self.logger.debug("Data handler {} set up.".format(handler.__class__.__name__))

    def close_data_handlers(self):
        for handler in self.data_handlers:
            handler.tearDown()
            self.logger.debug("{} closed.".format(handler.__class__.__name__))
