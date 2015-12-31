# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field  

class TutorialItem(Item):  
    # define the fields for your item here like:  
    # name = Field()  
    pass  
  
class JdbookItem(Item):  
    name = Field()
    price = Field()
    publisher = Field()
    author = Field()
    commit = Field()
    shop = Field()
#     category = Field()
#     link = Field()  
#     desc = Field()
#     rank = Field()
    