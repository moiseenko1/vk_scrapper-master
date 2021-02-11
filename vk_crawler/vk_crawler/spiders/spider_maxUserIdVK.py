# -*- coding: utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from vk_crawler.items import MaxUserID

# Regular expressions for items parsing
REGEXP_MAX_USER_VK_ID = '(?<=maxUserId: )\d+'


class SpiderMaxUserIdVK(scrapy.Spider):
    name = "spider_maxUserID"
    start_url = 'https://vkfaces.com/vk/users'

    def start_requests(self):
        url = self.start_url
        yield scrapy.FormRequest(url, callback=self.parse)

    def parse(self, response):
        loader = ItemLoader(item=MaxUserID(), response=response)
        loader.add_xpath('max_user_id', "//script[contains(., 'maxUserId')]/text()", re=REGEXP_MAX_USER_VK_ID)

        yield loader.load_item()