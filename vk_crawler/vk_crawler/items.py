import scrapy
from itemloaders.processors import MapCompose, Join, TakeFirst


def contain_value(value, status):
    status = ''.join(status)
    if value in status:
        return True


def parse_profile_status(status):
    return {
        contain_value('удалена', status): 'DELETED',
        contain_value('авторизованным', status): 'CLOSED',
        contain_value('обнаружили', status): 'BANNED',
        contain_value('заблокировать', status): 'BANNED',
        status == '': 'ACTIVE'
    }.get(True)


def parse_firstname(name):
    return name.split(' ')[0]

def parse_lastname(name):
    name_split = name.split(' ')
    if '(' in name_split[-1]:
        return name_split[-2]
    else:
        return name_split[-1]


class User(scrapy.Item):
    crawling_datetime = scrapy.Field(output_processor=TakeFirst(), )
    vk_id = scrapy.Field(output_processor=TakeFirst(), )
    page_name = scrapy.Field(output_processor=TakeFirst(), )
    firstname = scrapy.Field(input_processor=MapCompose(parse_firstname),
                                  output_processor=Join(), )
    lastname = scrapy.Field(input_processor=MapCompose(parse_lastname),
                                  output_processor=Join(), )
    birthdate = scrapy.Field(output_processor=Join(), )
    domain = scrapy.Field(output_processor=TakeFirst(), )
    country = scrapy.Field(output_processor=TakeFirst(), )
    city = scrapy.Field(output_processor=TakeFirst(), )
    phone = scrapy.Field(output_processor=TakeFirst(), )
    hometown = scrapy.Field(output_processor=Join(), )
    martial_status = scrapy.Field(output_processor=TakeFirst(), )
    last_activity = scrapy.Field(output_processor=TakeFirst(), )
    profile_status = scrapy.Field(input_processor=MapCompose(parse_profile_status),
                                  output_processor=Join(), )

class MaxUserID(scrapy.Item):
    max_user_id = scrapy.Field(output_processor=TakeFirst(), )
