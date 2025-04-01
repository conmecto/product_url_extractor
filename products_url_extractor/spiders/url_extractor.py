import scrapy
import re
from urllib.parse import urlparse
from datetime import datetime
from ..items import ProductURLItem

class URLExtractor(scrapy.Spider):
    name = 'url_extractor'
    
    PRODUCT_PATTERNS = [
        r"/product/", r"/products/", r"/item/", r"/p/", r"/shop/", r"/store/", r"/buy/",
        r"/goods/", r"/detail/", r"/listing/", r"/sku/", r"/dp/", r"/offer/", r"/catalog/"
    ]
    
    def __init__(self, start_urls=None, allowed_domains=None, max_depth=5, *args, **kwargs):
        super(URLExtractor, self).__init__(*args, **kwargs)
        self.start_urls = start_urls
        if allowed_domains:
            self.allowed_domains = allowed_domains
        else:
            self.allowed_domains = [urlparse(url).netloc for url in self.start_urls]
            
        self.max_depth = int(max_depth)
        self.visited_urls = set()
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={'depth': 1})
    
    def parse(self, response):
        current_url = response.url
        self.logger.info(f"Processing: {current_url}")
        domain = urlparse(current_url).netloc
        current_depth = response.meta.get('depth', 1)

        if current_url in self.visited_urls:
            return
        
        self.visited_urls.add(current_url)
        
        if self.is_product_url(current_url):
            item = ProductURLItem()
            item['url'] = current_url
            item['domain'] = domain
            item['discovery_depth'] = current_depth
            item['timestamp'] = datetime.now().isoformat()
            yield item
        
        if current_depth >= self.max_depth:
            return
        
        links = response.css('a::attr(href)').getall()
        for link in links:
            absolute_url = response.urljoin(link)
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc in self.allowed_domains and absolute_url not in self.visited_urls:
                yield scrapy.Request(
                    url=absolute_url,
                    callback=self.parse,
                    meta={'depth': current_depth + 1}
                )

    def is_product_url(self, url):
        return any(re.search(pattern, url) for pattern in self.PRODUCT_PATTERNS)