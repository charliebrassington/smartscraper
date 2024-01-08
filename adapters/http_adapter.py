import requests
import tls_client
import bs4


class HttpRequestAdapter:

    def __init__(self):
        self.sessions = (
            tls_client.Session(client_identifier="chrome112", random_tls_extension_order=True),
            requests.Session()
        )

    def send_request(self, url: str) -> bs4.BeautifulSoup:
        response = self.sessions[url.startswith("http://")].get(url=url)
        return bs4.BeautifulSoup(response.text)
