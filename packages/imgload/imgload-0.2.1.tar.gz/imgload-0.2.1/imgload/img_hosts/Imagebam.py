import re

from requests_html import HTMLSession

from imgload.img_hosts.ImageHost import ImageHost


class ImagebamCom(ImageHost):

    def __init__(self):
        super(ImageHost, self).__init__()
        self.base_url = "imagebam.com"
        self.regex = r'http?\D://www.imagebam.com/image/\w+'

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

        url = resp.html.xpath("//meta[contains(@property, 'og:image')]")
        if url:
            return url[0].attrs.get('content')

        return None
