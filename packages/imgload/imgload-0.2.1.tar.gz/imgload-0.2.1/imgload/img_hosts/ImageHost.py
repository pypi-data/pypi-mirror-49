class ImageHost():

    def __init__(self):
        self.base_url = None

    def get_link(self, link, session):
        """
        Should find a direct image url from a link to the hoster.

        :param link: the link to the hoster you can handle
        :param session: the requests session to use for http operations
        :return: the direct link to an image
        """
        raise NotImplementedError("Please Implement this method")

    def can_handle(self, link):
        '''
        Can the hoster handle this link
        :param link: the link to check
        :return: boolean if this plugin can handle the link
        '''
        raise NotImplementedError("Please Implement this method")
