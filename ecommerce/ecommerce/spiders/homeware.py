from urllib.parse import urljoin

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

#
# class HomewareSpider(CrawlSpider):
#     name = 'homeware'
#     allowed_domains = ['https://cultartfusion.com/collections/furniture']
#     start_urls = ['http://https://cultartfusion.com/collections/furniture/']
#
#     rules = (
#         Rule(LinkExtractor(allow=r'/collections/furniture\?page=[0-9]'), callback='parse_item', follow=True),
#     )
#
#     def parse_item(self, response):
#         item = {}
#         #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
#         #item['name'] = response.xpath('//div[@id="name"]').get()
#         #item['description'] = response.xpath('//div[@id="description"]').get()
#         return item


class HomewareSpider(scrapy.Spider):
    name = "homeware"

    def start_requests(self):
        yield scrapy.Request(url='https://cultartfusion.com/collections/furniture/', callback=self.parse_response)

    def parse_response(self, response):
        base_url = 'https://cultartfusion.com'

        products_urls = response.xpath('//a[@class="product-grid-item"]/@href').extract()

        # Follows links to product_url pages
        for product_url in products_urls:
            yield scrapy.Request(url=urljoin(base_url, product_url), callback=self.parse_product_page)

        next_page = response.xpath('//a[@title="Next »"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(url=urljoin(base_url, next_page), callback=self.parse_response)

    def parse_product_page(self, response):
        yield {
            'Name': response.css('h1::text').extract_first().strip(),
            'Description': response.css('div.product-description').get(),
            'RegularPrice': response.xpath('//meta[@itemprop="price"]/@content').get(),
            'Category': response.xpath('//nav[@class="breadcrumb"]/a[2]/text()').extract_first(),
            'Images': response.xpath('//ul[contains(concat(" ", normalize-space(@class)," "), "product-photo-thumbs")]/li/a/@href').getall(),
        }
