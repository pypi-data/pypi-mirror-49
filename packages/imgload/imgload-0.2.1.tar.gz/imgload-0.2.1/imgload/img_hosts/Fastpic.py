import re

from requests_html import HTMLSession

from imgload.img_hosts.ImageHost import ImageHost


class FastpicRu(ImageHost):

    def __init__(self):
        super(ImageHost, self).__init__()
        self.base_url = "fastpic.ru"
        self.regexs = [r'\A(http*(s)://i\d{1,}.fastpic.ru/)+\w',
                       r'\A(http*(s)://fastpic.ru/view)+.', ]

    def can_handle(self, link):
        for regex in self.regexs:
            result = re.search(regex, link)
            if result is not None:
                return True
        return False

    def get_link(self, link, session: HTMLSession):
        resp = session.get(link)

        resp.html.render()
        if resp.status_code is not 200:
            return None

        url = resp.html.xpath("//div[contains(@id, 'picContainer')]//img")
        if url is not None:
            return url[0].attrs.get('src')

        return None
