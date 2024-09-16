from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlingSpider(CrawlSpider):
    name = "adlibris_spider"
    allowed_domains = ["adlibris.com"]
    start_urls = ["https://www.adlibris.com/se/kampanj/boktips-nyhet"]

# IP adress of the proxy server
    #PROXY_SERVER = "127.0.0.1"

# check later the links to adjust the rule tupple
    rules = (
        Rule(LinkExtractor(allow="se/kampanj/boktips-nyhet")),
        Rule(LinkExtractor(allow="kampanj", deny="category"), callback="parse_item")
    )

    def parse_item(self, response):
        books = response.css('div.product_info')

        for book in books:
            yield {
                "title": book.css(".js-get-product-height-info h3::text").get().strip(),
                "author": book.css(".heading--product-panel-author-brand span::text").get().strip().replace("\r\n", "").replace("  ", " "),
                "price": book.css(".btn--first-divider span::text").get().strip().replace("\r\n", "").replace("  ", " "),
                "prev_price": book.css(".product__purchase__extra-info div::text").get().strip().replace("\r\n", "").replace("  ", " "),
                "url": book.css("div a::text").attrib['href']
            }

        # next_page = response.css('').get()

        if next_page is not None:
            next_page_url = '' + next_page

# export to csv run in terminal -> scrapy crawl [spider name] -o adlibris.json or adlibris.csv