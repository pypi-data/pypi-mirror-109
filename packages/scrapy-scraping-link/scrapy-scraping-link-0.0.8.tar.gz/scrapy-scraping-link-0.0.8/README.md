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
    'scrapy_scraping_link.ScrapingLinkMiddleware': 700,
}

CONCURRENT_REQUESTS = 1
```

### Usage

Inherit your spiders from `ScrapingLinkSpider` and yield a `ScrapingLinkRequest`.

Below you can see an example from the spider in [parascrapear.py](examples/parascrapear/parascrapear/spiders/parascrapear.py).

```python
from scrapy import Spider
from scrapy_scraping_link import ScrapingLinkSpider, ScrapingLinkRequest


class ParascrapearSpider(Spider):
    name = 'parascrapear'
    allowed_domains = ['parascrapear.com']
    start_urls = ['http://parascrapear.com/']

    def parse(self, response):
        print('Parseando ' + response.url)       
        
        next_urls = response.css('a::attr(href)').getall()
        for next_url in next_urls:
            if next_url is not None:
                yield ScrapingLinkRequest(response.urljoin(next_url))
        
        sentences = response.css('q::text').getall()
        for sentence in sentences:
            print(sentence)

```

You can pass [ScrapingLink parameters](https://scraping.link/documentacion/) in the params argument of a ScrapingLinkRequest. Headers and cookies are passed like a normal Scrapy Request. ScrapingLinkRequests formats all parameters, headers and cookies to the format expected by the API.

### Examples

Add your API key to [settings.py](examples/parascrapear/parascrapear/settings.py).

To run the examples you need to clone this repository. In your terminal, go to `examples/parascrapear/parascrapear` and run the example spider with:

```bash
scrapy runspider parascrapear.py
```

#### Customer Support
Simply reach out to us via [Telegram Group](https://t.me/joinchat/AwFbIh1PuwuEgCk0gVgS4g) or or write us an [email](mailto:info@scraping.link).

[Sign up for our free plan](https://app.scraping.link/register) to get a free API key loaded with 100 free credits. No credit card required!
