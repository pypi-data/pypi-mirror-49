import datetime
import importlib
import logging
import os
import random
from contextlib import suppress

logger = logging.getLogger(__name__)


# TODO: design deamon spider

class SpiderInstance(object):
    def __init__(self, module, store_data=True):
        self.module = module
        self.spider = module.Spider
        self.name = module.Spider.name
        self.site = module.Spider.start_urls[0]
        self.sites = module.Spider.start_urls
        self.enabled = True

    def __call__(self):
        return self.spider

    def __repr__(self):
        if len(self.sites) == 1:
            return "<Spider {name} for {site}. {state}>".format(name=self.name, site=self.site, state='Enabled' if self.enabled else 'Disabled')
        else:
            return "<Spider {name} for {sites}. {state}>".format(name=self.name, site=self.sites, state='Enabled' if self.enabled else 'Disabled')


class Spiders:
    def __init__(self, directory, store_data=True, ignore_files=[]):
        self.spiders = []

        dirs = os.walk(os.path.abspath(directory))
        spiders_dir = next(dirs)
        spiders_dir_path = os.path.abspath(spiders_dir[0])

        filenames = spiders_dir[2]

        with suppress(ValueError):
            filenames.remove('__init__.py')
        with suppress(ValueError):
            filenames.remove('pipelines.py')
        for f in ignore_files:
            with suppress(ValueError):
                filenames.remove(f)

        spiders_names = list(map(lambda item: {'module_name': item.split('.')[0], 'module_path': os.path.join(spiders_dir_path, item)}, filenames))

        for spider_name in spiders_names:
            specification = importlib.util.spec_from_file_location(spider_name['module_name'], spider_name['module_path'])
            spider_module = importlib.util.module_from_spec(specification)
            specification.loader.exec_module(spider_module)

            spider = SpiderInstance(spider_module)
            self.spiders.append(spider)


    @property
    def active_spiders(self):
        """
        Returns all active spiders

        Returns:
        iter:Active spiders
        """
        return iter(filter(lambda spider: spider.enabled, self.spiders))


    def crawl(self):
        """
        Start all spiders. Crawl the data from sites.
        Note: This is blocking function!

        Parameters: None
        Returns: None
        """
        # TODO: Use CrawlerRunner instead of CrawlerProcess
        runner = CrawlerRunner({
            'USER_AGENT': random.choice(generate_user_agent()),
            'ITEM_PIPELINES': {'bot.spiders.pipelines.DjangoDBWriterPipeline': 500}
        })
        for spider in self.active_spiders:
            d = runner.crawl(spider())
            d.addBoth(lambda _: reactor.stop())

        reactor.run() # the script will block here until the crawling is finished
