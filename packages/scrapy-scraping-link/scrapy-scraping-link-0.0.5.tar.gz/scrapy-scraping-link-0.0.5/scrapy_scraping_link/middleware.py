import logging

from scrapy import Request
from scrapy.exceptions import NotConfigured

from .request import ScrapingLinkRequest

logger = logging.getLogger(__name__)


class ScrapingLinkMiddleware:
    api_url = 'https://app.scraping.link/api/scrape'

    def __init__(self, api_key):
        self.api_key = api_key

    @classmethod
    def from_crawler(cls, crawler):
        api_key = crawler.settings.get('SCRAPINGLINK_API_KEY')
        if not api_key:
            raise NotConfigured

        return cls(api_key=api_key)

    def _get_url(self, params):
        qs_params = dict()
        qs_params.update(params)
        qs_params["api_token"] = self.api_key

        qs = '&'.join(f'{k}={v}' for k, v in qs_params.items())
        return f'{self.api_url}?{qs}'

    @staticmethod
    def _replace_response_url(response):
        resolved_url = response.headers.get(
            'ScrapingLink-Resolved-Url', def_val=response.url)

        if resolved_url:
            return response.replace(
                url=resolved_url.decode(response.headers.encoding))
        return response.url

    def process_request(self, request, spider):
        if not isinstance(request, ScrapingLinkRequest):
            return

        url = self._get_url(
            request.meta['ScrapingLink']['params'])

        new_request = request.replace(
            cls=Request, url=url, meta=request.meta)

        return new_request

    def process_response(self, request, response, spider):
        if 'ScrapingLink' not in request.meta:
            return response

        new_response = self._replace_response_url(response)

        return new_response
