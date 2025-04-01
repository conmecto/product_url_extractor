# Product URL Extractor

A high-performance Scrapy crawler that discovers product URLs across multiple e-commerce websites concurrently. 
This project uses Scrapy's asynchronous architecture and implements custom pipelines for efficient data processing.

## Features

- Multi-domain parallel crawling with configurable concurrency
- Asynchronous request handling for maximum performance
- Thread-safe data processing via item pipelines
- Periodic data saving to prevent memory overflow
- Product URL detection using pattern matching

## Project Structure

```
product_url_extractor/
│
├── product_url_extractor/
│   ├── __init__.py
│   ├── items.py           # Defines data structure for scraped items
│   ├── pipelines.py       # Off-thread data processing
│   ├── settings.py        # Project settings and configuration
│   └── spiders/
│       ├── __init__.py
│       └── url_extractor.py  # Main spider implementation
│
├── run.py                 # Convenient script to run the crawler
└── scrapy.cfg             # Scrapy configuration file
```

## Performance Optimization

This crawler is optimized for performance in several ways:

1. **Parallel Request Processing**: 
   - Configurable concurrent requests (16 globally, 8 per domain)
   - Non-blocking I/O operations using Twisted's event-driven architecture

2. **Thread Isolation**:
   - Crawling logic runs separately from data processing
   - URL discovery is not slowed down by I/O operations

3. **Memory Management**:
   - Periodic data saving and buffer clearing
   - Visited URL tracking to prevent duplicate processing

4. **Thread Safety**:
   - Lock mechanisms to prevent race conditions
   - Safe file operations across multiple threads

## Usage

### Installation

1. Create a Python virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Scrapy:
   ```
   pip install scrapy
   ```

3. Clone or copy this project structure

### Running the Crawler

```
python run.py
```

### Configuration

Edit `settings.py` to customize crawler behavior:

- `CONCURRENT_REQUESTS`: Number of simultaneous requests across all domains
- `CONCURRENT_REQUESTS_PER_DOMAIN`: Number of simultaneous requests per domain
- `DOWNLOAD_DELAY`: Time delay between requests (seconds)
- `SAVE_INTERVAL`: How often to save discovered URLs (seconds)

## Customization

### Adding New Target Websites

Edit `run.py` to modify the `start_urls` list:

```python
start_urls = [
    'https://www.virgio.com/', 
    'https://www.tatacliq.com/', 
    'https://nykaafashion.com/', 
    'https://www.westside.com/',
    # Add more..
]
```

### Adjusting Product URL Patterns

Edit the `PRODUCT_PATTERNS` list in `spiders/url_spider.py` to match your target websites:

```python
PRODUCT_PATTERNS = [
    r"/product/", 
    r"/products/",
    # Add more patterns here
]
```

## Performance Monitoring

The crawler logs information at the INFO level. Monitor performance by checking:

- Request rate
- URL discovery rate
- Memory usage
- File write frequency

Adjust settings as needed for optimal performance on your hardware.
