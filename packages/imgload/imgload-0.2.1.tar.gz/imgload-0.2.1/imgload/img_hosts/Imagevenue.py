import re
from urllib.parse import urljoin

from requests_html import HTMLSession

from imgload.img_hosts.ImageHost import ImageHost


class ImagevenueCom(ImageHost):

    def __init__(self):
        super(ImageHost, self).__init__()
        self.base_url = "imagevenue.com"
        self.regex = r'http*\D://img\d{1,}.imagevenue.com/img.php.+'

    def can_handle(self, link):
        result = re.search(self.regex, link)
        if result is not None:
            return True
        return False

    def get_link(self, link, session: HTMLSession):
        resp = session.get(link)

        resp.html.render()
        if resp.status_code is not 200:
            return None

        url = resp.html.xpath("//img[contains(@id, 'thepic')]")
        if url:
            relative_url = url[0].attrs.get('src')
            return urljoin(resp.url, relative_url)

        return None
