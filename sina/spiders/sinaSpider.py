# -*- coding: utf-8 -*-
import scrapy
import os
from sina.items import SinaItem


class SinaSpider(scrapy.Spider):
    name = 'sinaSpider'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        """
        解析网址导航的列表页
        :param response: 响应
        """
        # 用于保存小类的标题，链接和目录
        items = []
        # 所有大类的标题和URL
        par_title = response.xpath('//div[@id="tab01"]//div/h3/a/text()').extract()
        par_urls = response.xpath('//div[@id="tab01"]//div/h3/a/@href').extract()

        # 所有小类的标题和URL
        sub_title = response.xpath('//div[@id="tab01"]//div/ul/li/a/text()').extract()
        sub_urls = response.xpath('//div[@id="tab01"]//div/ul/li/a/@href').extract()

        # 给每个大类创建一个路径
        for i in range(0, len(par_title)):
            par_filename = './Data/' + par_title[i]

            # 如果这个大类的目录不存在，则创建
            if not os.path.exists(par_filename):
                os.makedirs(par_filename)

            # 将大类的标题与链接保存
            item = SinaItem()
            item['par_title'] = par_title[i]
            item['par_urls'] = par_urls[i]

            for j in range(0, len(sub_title)):

                # 判断小类链接的前缀与大类链接是否一致
                if_belong = sub_urls[j].startswith(item['par_urls'])
                if if_belong:

                    # 拼接大类目录/小类目录
                    sub_filename = par_filename + '/' + sub_title[j]

                    # 如果小类目录不存在，则创建
                    if not os.path.exists(sub_filename):
                        os.makedirs(sub_filename)

                    # 将小类的链接与标题保存
                    item['sub_urls'] = sub_urls[j]
                    item['sub_title'] = sub_title[j]
                    item['sub_filename'] = sub_filename

                    # 添加到items的列表中
                    items.append(item)

        for item in items:
            # 访问每个小类链接，注意meta是可选参数
            yield scrapy.Request(url=item['sub_urls'], meta={'meta_1': item}, callback=self.second_parse)

    def second_parse(self, response):
        """
        解析小类的列表页
        :param response: 响应
        """
        items = []

        # 提取出每次response的meta数据
        meta_1 = response.meta['meta_1']

        # 所有小类下的链接
        urls = response.xpath('//a/@href').extract()

        for i in range(0, len(urls)):
            item = SinaItem()
            # 判断小类的链接是否为文章链接，如是否以大类链接开头和以“.shtml结束”
            if_belong = urls[i].startswith(meta_1['par_urls']) and urls[i].endswith('.shtml')
            if if_belong:
                item['par_title'] = meta_1['par_title']
                item['par_urls'] = meta_1['par_urls']
                item['sub_title'] = meta_1['sub_title']
                item['sub_urls'] = meta_1['sub_urls']
                item['sub_filename'] = meta_1['sub_filename']
                item['urls'] = urls[i]

                items.append(item)
        for item in items:
            yield scrapy.Request(url=item['urls'], meta={'meta_2': item}, callback=self.detail_parse)

    def detail_parse(self, response):
        """
        提取每篇文章的链接标题与内容
        :param response: 响应
        """
        content = ''
        item = response.meta['meta_2']
        title = response.xpath('//h1[@class="main-title"]/text()').extract()
        contents = response.xpath('//div[@class="article"]/p/text()').extract()

        for content_one in contents:
            content += content_one

        item['title'] = title
        item['content'] = content

        yield item
