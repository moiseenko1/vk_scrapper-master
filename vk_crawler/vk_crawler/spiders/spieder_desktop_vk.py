# -*- coding: utf-8 -*-
import random

import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader
from vk_crawler.items import User

# Regular expressions for items parsing
REGEXP_VK_ID = 'vk.com/id(.+)'
REGEXP_DOMAIN_ID = '(?<=vk\.com\/).*'
REGEXP_CITY = '(?<=c\[city\]=)\d+'
REGEXP_COUNTRY = '(?<=c\[country\]=)\d+'


class SpiderVK(scrapy.Spider):
    name = "spider_vk1"

    def list_of_id(self, amount):
        # For generating list of input IDs
        list = []
        for vk_id in range(amount):
            list.append('https://vk.com/id900{0}'.format(vk_id))
        return list

    def start_requests(self):
        start_urls = self.list_of_id(2000)
        for url in start_urls:
            yield scrapy.FormRequest(url, callback=self.parse)

    def parse(self, response):
        user_loader = ItemLoader(item=User(), response=response)
        profile_status = response.xpath('//div[contains(@class, "message_page_body")]/text() | '
                                        '//h5[contains(@class, "profile_blocked page_block")]/text() | '
                                        '//h5[contains(@class, "profile_deleted_text")]/text()').getall()
        page_name = response.xpath('//h1[@class="page_name"]/text()').get()
        user_loader.add_value('crawling_datetime', datetime.now())
        user_loader.add_value('vk_id', response.url, re=REGEXP_VK_ID)
        user_loader.add_xpath('domain', '//link[contains(@rel, "canonical")]/@href', re=REGEXP_DOMAIN_ID)
        user_loader.add_value('page_name', page_name)
        user_loader.add_value('firstname', page_name)
        user_loader.add_value('lastname', page_name)
        user_loader.add_xpath('birthdate', '//a[contains(@href, "c[bday]")]/text()')
        user_loader.add_xpath('birthdate', '//a[contains(@href, "c[byear]")]/text()')
        user_loader.add_value('profile_status', profile_status or '')
        user_loader.add_xpath('city', '//a[contains(@href, "c[city]")]/@href', re=REGEXP_CITY)
        user_loader.add_xpath('martial_status', '//a[contains(@href, "c[status]")]/text()')
        user_loader.add_xpath('country', '//a[contains(@href, "c[country]")]/@href', re=REGEXP_COUNTRY)
        user_loader.add_xpath('phone', '//div[contains(text(),"Моб. телефон:")]/../div[2]/text()')
        user_loader.add_xpath('hometown', '//a[contains(@href, "c[hometown]")]/text()')
        user_loader.add_css('last_activity', 'div.profile_online_lv::text')

        return user_loader.load_item()
