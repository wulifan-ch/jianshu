# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    image = scrapy.Field()
    article_id = scrapy.Field()
    origin_url = scrapy.Field()
    content = scrapy.Field()
    like_count = scrapy.Field()
    subjects = scrapy.Field()
