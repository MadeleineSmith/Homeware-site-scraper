from urllib.parse import urljoin

import scrapy


class HomewareSpider(scrapy.Spider):
    name = "homeware"
    base_url = 'https://cultartfusion.com'

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse_home_page)

    def parse_home_page(self, response):
        product_category_urls = response.xpath('//li[@class="site-nav--has-dropdown "][1]/ul/li/ul/li/a/@href').getall()

        for product_category_url in product_category_urls:
            yield scrapy.Request(url=urljoin(self.base_url, product_category_url), callback=self.parse_product_category_page)

    def parse_product_category_page(self, response):
        products_urls = response.xpath('//a[@class="product-grid-item"]/@href').extract()

        for product_url in products_urls:
            yield scrapy.Request(url=urljoin(self.base_url, product_url), callback=self.parse_product_page)

        next_page = response.xpath('//a[@title="Next »"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(url=urljoin(self.base_url, next_page), callback=self.parse_product_category_page)

    def parse_product_page(self, response):
        yield {
            'Name': response.xpath('//h1/text()').get(),
            'Description': response.xpath('//div[contains(concat(" ", normalize-space(@class)," "), "product-description")]').get(),
            'Regular Price': response.xpath('//meta[@itemprop="price"]/@content').get(),
            'Category': response.xpath('//nav[@class="breadcrumb"]/a[2]/text()').get(),
            'Images': response.xpath('//ul[contains(concat(" ", normalize-space(@class)," "), "product-photo-thumbs")]/li/a/@href').getall()
        }
