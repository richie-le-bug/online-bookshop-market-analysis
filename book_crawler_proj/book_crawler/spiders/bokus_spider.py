import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from book_crawler.items import BookCrawlerItem


class BokusSpiderSpider(scrapy.Spider):
    name = "bokus_spider"
    allowed_domains = ["bokus.com"]
    start_urls = ["https://www.bokus.com/nyheter"]

    custom_settings = {
        'FEEDS': {
            'bokus.csv': {'format': 'csv', 'overwrite': False},
        }
    }

    def parse(self, response):
        books = response.css('li.ProductList__item')

        for book in books:
            yield {
                "title": book.css("h3 a::text").get().strip(),
                "author": book.css("h4 a::text").get().strip().replace("\r\n", "").replace("  ", " "),
                "price": book.css("div.pricing span::text").get().strip().replace("\r\n", "").replace("  ", " "),
                "discount": book.css("div.stickers span::text").get().strip().replace("\r\n", "").replace("  ", " "),
                #"url": book.css('h3.Item__title a').attrib['href']
            }

        next_page = response.css('ol.ProductList__pagination li a ::attr(href)').get() #needs a class or go through each page by page number

        # '/cgi-bin/product_search.cgi?is_paginate=1&language=svenska&binding_normalized=inbunden&campaign_tags=NYHET&nyhet=nyhet&from=2' <- extract the 2 and add a function to add other numbers
        # example: next_page_url = 'https://www.bokus.com/' + next_page[url without number] + number func

        #if next_page is not None:
            #next_page_url = 'https://www.bokus.com/' + next_page
            #yield response.follow(next_page_url, callback= self.parse)

        if next_page is not None:
            next_page_url = 'https://www.bokus.com/' + next_page
            yield response.follow(next_page_url, callback= self.parse)

# export to csv run in terminal -> scrapy crawl (spider name) -o adlibris.json or adlibris.csv
# if the settings file is setup is only needed to -> scrapy crawl (spider name)
