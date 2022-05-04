# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MovieItem(Item):
    name = Field()  # 名字
    category = Field()  # 类别
    score = Field()  # 评分
    drama = Field()  # 简介
    directors = Field()  # 导演
    actors = Field()  # 演员
