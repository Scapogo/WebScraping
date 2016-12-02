import scrapy
import re
from scrapy.loader import ItemLoader
from WebScraper.items import Advert

class AdvertSpider(scrapy.Spider):
    name = "adverts"
    start_urls = [
        'http://www.nehnutelnosti.sk/senica/predaj',
    ]

    def parse(self, response):
        # follow links to author pages
        print('Parse started' + response.url)
        # yield scrapy.Request(response.url,
        #                      callback=self.parse_advert_response)

        for href in response.css('div.advertisement-head  h2 a::attr(href)').extract():
            # self.parse_to_item(scrapy.Request(response.urljoin(href)))
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_price)

        # follow pagination links
        # next_page = response.css('div.withLeftBox a.next::attr(href)').extract_first()
        # if next_page is not None:
        #     print(next_page)
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        # response.css('div.search-stripe ul.vpravo a.posledne')

    def parse_price(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        yield self.parse_to_item(response)
        #     {
        #     'price': extract_with_css('div.params strong.boldRed.text::text'),
        # }

    def parse_to_item(self, response):
        def get_float(text):
            result = re.findall(r'\d+\.*\d*', text)

            if len(result) > 0:
                return result[0]
            else:
                return 0

        l = ItemLoader(item=Advert(), response=response)
        l.add_xpath('Id', '//div[@id="breadcrumbs"]/text()')
        # response.xpath('//meta[@property="og:url"]/@content').extract()
        l.add_xpath('Link', '//meta[@property="og:url"]/@content')
        l.add_xpath('Price', '//strong[@id="data-price"]/text()')
        l.add_xpath('NumberOfRooms', '//strong[@id="categoryNameJS"]/text()')   # categoryNameJS
        # AreaM2 = scrapy.Field()  # Area in square meters
        str_area = response.xpath('//div[@id="params"]/p[@class="paramNo1"]/strong/text()').extract()[-1]
        value = get_float(str_area)
        l.add_value('AreaM2', value)   # '//div[@id="params"]/p[@class="paramNo1"]/strong/text()').extract()[-1]
        # Age = scrapy.Field()  # Categorical new or older building
        l.add_value('Age', 'New')
        # LastUpdate = scrapy.Field()  # Last update of advert
        value = response.xpath('//div[@id="params"]/p[@class="paramNo0"]/strong/text()').extract()[-1]
        l.add_value('LastUpdate', value)
        return l.load_item()

    def parse_advert_response(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        for inzerat in response.css('div.inzerat'):
            yield {
                    'id': inzerat.css('div.inzerat::attr(id)').extract_first()[1:],
                    'link': inzerat.css('div.advertisement-head  h2 a::attr(href)').extract_first(),
                }
