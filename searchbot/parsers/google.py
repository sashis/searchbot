from .common import SearchEngineResponseParser


class GoogleResponseParser(SearchEngineResponseParser):
    base_url = 'https://google.com/search'
    query_key = 'q'
    page_key = 'start'

    def _link_mapper(self, link):
        return self._get_query_key(link['href'], 'q')

    def _get_links(self):
        return self.dom.select('a[href^="/url?q="]')

    def _get_nav_links(self):
        return self.dom.select('footer a[href^="/search"]')
