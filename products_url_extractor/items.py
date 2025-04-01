import scrapy

class ProductURLItem(scrapy.Item):
    url = scrapy.Field()
    domain = scrapy.Field()
    discovery_depth = scrapy.Field()
    timestamp = scrapy.Field()