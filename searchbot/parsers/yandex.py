from .common import SearchEngineResponseParser


class YandexResponseParser(SearchEngineResponseParser):
    base_url = 'https://yandex.ru/search/'
    query_key = 'text'
    page_key = 'p'

    def _link_mapper(self, link):
        return link['href']

    def _get_links(self):
        return self.dom.select('li h2 a:not([href*="yandex.ru"])')

    def _get_nav_links(self):
        return self.dom.select('[role="navigation"] a[href^="/search/"]')
