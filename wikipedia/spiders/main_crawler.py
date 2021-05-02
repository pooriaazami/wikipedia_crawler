import scrapy

from scrapy import Spider

from wikipedia.enums import LinkTypes
from wikipedia.utils import analyze_link


class WikipediaSpider(Spider):
    name = "wikipedia"

    def start_requests(self):
        ...

    def crawler(self, response):
        for link in response.css('a::attr(href)'):
            # add link to database
            # analyze_link(link)
            if analyze_link(link) == LinkTypes.CORRECT_LINK:
                url = response.urljoin(link)
                scrapy.Request(url, callback=self.crawler)
