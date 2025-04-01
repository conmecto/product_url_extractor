from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from products_url_extractor.spiders.url_extractor import URLExtractor

if __name__ == '__main__':
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    start_urls = [
        'https://www.virgio.com/', 
        'https://www.tatacliq.com/', 
        'https://nykaafashion.com/', 
        'https://www.westside.com/'
    ]
    max_depth = 10
    process.crawl(URLExtractor, start_urls=start_urls, max_depth=max_depth)
    process.start()