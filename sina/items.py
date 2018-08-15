# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaItem(scrapy.Item):
    # 大类标题
    par_title = scrapy.Field()
    # 大类链接
    par_urls = scrapy.Field()

    # 小类标题
    sub_title = scrapy.Field()
    # 小类链接
    sub_urls = scrapy.Field()
    # 小类目录存储路径
    sub_filename = scrapy.Field()

    # 文章链接
    urls = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 文章内容
    content = scrapy.Field()
