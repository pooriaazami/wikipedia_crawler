import scrapy

from scrapy import Spider

from wikipedia.enums import LinkTypes
from wikipedia.utils import analyze_link, write_to_file

from utils.redis_interface import RedisInterface


class WikipediaSpider(Spider):
    name = "wikipedia"

    def __init__(self):
        self.__redis_interface = RedisInterface()
        self.__count = 1

    def start_requests(self):
        yield scrapy.Request('https://fa.wikipedia.org/', callback=self.link_crawler)

    def process_page(self, response):
        text = ""
        for tag in response.css('p'):
            for data in tag.css('::text').getall():
                text += data
        if len(text) > 0:
            with open(f'data/{self.__count}.txt', 'w', encoding='utf-8') as file:
                file.write(text)

            self.__count += 1

    def link_crawler(self, response):
        self.process_page(response)
        for link in response.css('a::attr(href)').getall():
            # add link to database
            if analyze_link(link) == LinkTypes.WIKI and self.__redis_interface.add_item(link):
                url = response.urljoin(link)
                # write_to_file('./links.txt', link)
                yield scrapy.Request(url, callback=self.link_crawler)
