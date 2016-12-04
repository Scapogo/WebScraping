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

        def get_int(text):
            result = re.findall(r'\d+\ *\d*', text)

            if len(result) > 0:
                return result[0]
            else:
                return 0

        def get_m2(text):
            results = re.findall(r'\d+', text)

            area = ''

            for result in results:
                area += str(int(result))

            if len(result) > 0:
                return area
            else:
                return 0

        def get_id(text):
            result = re.findall(r'\d+', text)

            if len(result) > 0:
                return result[0]
            else:
                return 0

        l = ItemLoader(item=Advert(), response=response)

        str_value = str(response.xpath('//div[@id="breadcrumbs"]/text()').extract())
        value = get_id(str_value)
        l.add_value('Id', value)

        l.add_xpath('Link', '//meta[@property="og:url"]/@content')

        str_value = str(response.xpath('//strong[@id="data-price"]/text()').extract())
        value = get_int(str_value)
        l.add_value('Price', value)

        l.add_xpath('NumberOfRooms', '//strong[@id="categoryNameJS"]/text()')   # categoryNameJS

        # Get all parameters of estate
        parameters = response.xpath('//div[@id="params"]/p')

        for parameter in parameters:
            text = str(parameter.xpath('.//span[@class="tlste"]/text()').extract())
            if "Úžitková plocha" in text:
                # Area in square meters
                str_area = str(parameter.xpath('.//strong/text()').extract())
                value = get_m2(str_area)
                l.add_value('LivingAreaM2', value)
            elif "Dátum aktualizácie" in text:
                # Last update of advert
                str_date = str(parameter.xpath('.//strong/text()').extract())[2:-2]
                l.add_value('LastUpdate', str_date)
            elif "Stav" in text:
                # Categorical new or older building
                str_age = str(parameter.xpath('.//strong/text()').extract())[2:-2]
                l.add_value('Age', str_age)
            elif "Plocha pozemku" in text:
                # Whole are in square meters
                str_area = str(parameter.xpath('.//strong/text()').extract())
                value = get_m2(str_area)
                l.add_value('LandAreaM2', value)
            elif "Lokalita" in text:
                # Location of estate
                str_location = parameter.xpath('.//strong/text()').extract()
                value = ''.join(str_location)
                l.add_value('Location', value)

        return l.load_item()
