import scrapy

from scrapy import Spider

from wikipedia.enums import LinkTypes
from wikipedia.glob import links
from wikipedia.utils import analyze_link


class WikipediaSpider(Spider):
    name = "wikipedia"

    def start_requests(self):
        yield scrapy.Request('https://fa.wikipedia.org/', callback=self.link_crawler)

    def link_crawler(self, response):
        for link in response.css('a::attr(href)').getall():
            # add link to database
            if analyze_link(link) == LinkTypes.CORRECT_LINK and not link in links:
                url = response.urljoin(link)
                links.add(link)
                yield scrapy.Request(url, callback=self.link_crawler)
