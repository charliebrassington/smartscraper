import bs4

from adapters import http_adapter


class HttpService:
    def __init__(self):
        self._http_adapter = http_adapter.HttpRequestAdapter()

    def get_parsed_html(self, url: str) -> bs4.BeautifulSoup:
        return self._http_adapter.send_request(url)
