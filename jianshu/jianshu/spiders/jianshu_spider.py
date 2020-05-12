# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import JianshuItem

class JianshuSpiderSpider(CrawlSpider):
    name = 'jianshu_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        image = response.xpath("//meta[@property='og:image']/@content").get()
        author = response.xpath("//span[@class='_22gUMi']/text()").get()
        content = ''.join(response.xpath("//article[@class='_2rhmJa']//text()").getall())
        origin_url = response.url.split('?')[0]
        article_id = origin_url.split('/')[-1]
        like_count = response.xpath("//span[@class='_1LOh_5']/text()").get()
        subjects = ','.join(response.xpath("//span[@class='_2-Djqu']/text()").getall())
        item = JianshuItem(
            title=title,
            image=image,
            author=author,
            content=content,
            origin_url=origin_url,
            article_id=article_id,
            like_count=like_count,
            subjects=subjects
        )
        yield item

