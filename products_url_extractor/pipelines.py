import json
from datetime import datetime
from collections import defaultdict
from threading import Lock

class URLProcessingPipeline:
    def __init__(self, save_interval=120):
        self.save_interval = save_interval
        self.last_save_time = datetime.now()
        self.urls_buffer = defaultdict(list)
        self.file_lock = Lock()
        self.buffer_lock = Lock()
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            save_interval=crawler.settings.get('SAVE_INTERVAL', 120)
        )
        
    def process_item(self, item, spider):
        domain = item['domain']
        with self.buffer_lock:
            self.urls_buffer[domain].append(item['url'])

        now = datetime.now()
        if (now - self.last_save_time).total_seconds() >= self.save_interval:
            self.save_buffer(spider)
        return item
    
    def save_buffer(self, spider):
        with self.buffer_lock:
            buffer_to_save = self.urls_buffer.copy()
            self.urls_buffer.clear()
            
        if buffer_to_save:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'product_urls_{timestamp}.json'
            
            with self.file_lock:
                with open(filename, 'w') as f:
                    json.dump({"product_urls": buffer_to_save}, f, indent=4)
                
            spider.logger.info(f"URLs saved to {filename}")
            self.last_save_time = datetime.now()

    def close_spider(self, spider):
        self.save_buffer(spider)