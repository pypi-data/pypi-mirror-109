## Scrapy ScrapingLink Middleware

### Acknowledgements

Thanks to [arimbr](https://github.com/arimbr) and [ScrapingBee](https://github.com/ScrapingBee/scrapy-scrapingbee), this is adaptation of their work.

### Installation

`pip install scrapy-scraping-link`

### Configuration

Add your `ScrapingLink_API_KEY` and the `ScrapingLinkMiddleware` to your project settings.py. Don't forget to set `CONCURRENT_REQUESTS` according to your [ScrapingLink plan](https://scraping.link/precios/).

```python
SCRAPINGLINK_API_KEY = 'REPLACE-WITH-YOUR-API-KEY'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_ScrapingLink.ScrapingLinkMiddleware': 700,
}

CONCURRENT_REQUESTS = 1
```

### Usage

Inherit your spiders from `ScrapingLinkSpider` and yield a `ScrapingLinkRequest`.

Below you can see an example from the spider in [httpbin.py](examples/httpbin/httpbin/spiders/httpbin.py).

```python
from scrapy import Spider
from scrapy_scraping_link import ScrapingLinkSpider, ScrapingLinkRequest

class HttpbinSpider(Spider):
    name = 'httpbin'
    start_urls = [
        'https://httpbin.org',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield ScrapingLinkRequest(url, params={
                # 'render': False,
            },
            headers={
                # 'Accept-Language': 'En-US',
            },
            cookies={
                # 'name_1': 'value_1',
            })

    def parse(self, response):
        ...
```

You can pass [ScrapingLink parameters](https://scraping.link/documentacion/) in the params argument of a ScrapingLinkRequest. Headers and cookies are passed like a normal Scrapy Request. ScrapingLinkRequests formats all parameters, headers and cookies to the format expected by the API.

### Examples

Add your API key to [settings.py](examples/httpbin/httpbin/settings.py).

To run the examples you need to clone this repository. In your terminal, go to `examples/httpbin/httpbin` and run the example spider with:

```bash
scrapy crawl httpbin
```

#### Customer Support
Simply reach out to us via [Telegram Group](https://t.me/joinchat/AwFbIh1PuwuEgCk0gVgS4g) or or write us an [email](mailto:info@scraping.link).

[Sign up for our free plan](https://app.scraping.link/register) to get a free API key loaded with 100 free credits. No credit card required!
