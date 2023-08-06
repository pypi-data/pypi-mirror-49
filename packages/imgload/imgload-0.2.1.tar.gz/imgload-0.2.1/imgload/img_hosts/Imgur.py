import re

from requests_html import HTMLSession

from imgload.img_hosts.ImageHost import ImageHost


class ImgurCom(ImageHost):

    def __init__(self):
        super(ImageHost, self).__init__()
        self.base_url = "imgur.com"
        self.regex = r'\A(http*(s)://imgur.com/)+'

    def can_handle(self, link):
        result = re.search(self.regex, link)
        if result is None:
            return False
        return True

    def get_link(self, link, session: HTMLSession):
        resp = session.get(link)

        resp.html.render()
        if resp.status_code is not 200:
            return None

        url = resp.html.xpath("//a[contains(@class, 'zoom')]")
        if url is not None:
            return url[0].absolute_links.pop()

        return None
