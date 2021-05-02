import scrapy

from scrapy import Spider

from wikipedia.enums import LinkTypes
from wikipedia.glob import links
from wikipedia.utils import analyze_link, write_to_file


class WikipediaSpider(Spider):
    name = "wikipedia"

    def __init__(self):
        self.__count = 1

    def start_requests(self):
        yield scrapy.Request('https://fa.wikipedia.org/', callback=self.link_crawler)

    def process_page(self, response):
        for text in response.css('p::text').getall():
            write_to_file(f'data/{self.__count}.txt', text)
        self.__count += 1

    def link_crawler(self, response):
        self.process_page(response)
        for link in response.css('a::attr(href)').getall():
            # add link to database
            if analyze_link(link) == LinkTypes.WIKI and link not in links:
                url = response.urljoin(link)
                links.add(link)
                # write_to_file('./links.txt', link)
                yield scrapy.Request(url, callback=self.link_crawler)
