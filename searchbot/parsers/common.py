import logging
from abc import ABC, abstractmethod
from urllib.parse import urljoin, urlencode, urlsplit, parse_qs

from bs4 import BeautifulSoup
from bs4.element import SoupStrainer

logger = logging.getLogger(__name__)


class ResponseParser(ABC):
    """Общий парсер страниц"""
    def __init__(self, response, init_parser=None):
        self.url = response.url
        logger.debug(f'Parsing {response.url}...')
        self.dom = BeautifulSoup(response.text, 'html.parser',
                                 parse_only=init_parser)

    @abstractmethod
    def _link_mapper(self, link):
        """правило преобразования ссылок"""
        pass

    @abstractmethod
    def _get_links(self):
        """находит ссылки на странице"""
        pass

    def get_title(self):
        """вовзращает название страницы"""
        title = getattr(self.dom.title, 'string', '').strip()
        title = title.translate(title.maketrans('', '', '\r\n\t'))
        logger.debug(f'...got title: {title}.')
        return title

    def get_results(self):
        """возвращает найденные ссылки"""
        return map(self._link_mapper, self._get_links())


class CommonResponseParser(ResponseParser):
    """Парсер произвольных страниц"""
    def __init__(self, response):
        super().__init__(response, init_parser=SoupStrainer(['title', 'a']))

    def _link_mapper(self, link):
        url_no_fragment = link['href'].split('#')[0]
        return urljoin(self.url, url_no_fragment)

    def _get_links(self):
        return self.dom.select('a[href*="/"]')


class SearchEngineResponseParser(ResponseParser):
    """Общий парсер страниц результатов поисковых систем"""
    base_url: str
    query_key: str
    page_key: str

    def __init__(self, response):
        super().__init__(response)
        self.url = response.url

    @classmethod
    def make_init_url(cls, query):
        """Создает url поискового запроса (больше некуда влепить)"""
        qs = '?' + urlencode({cls.query_key: query})
        return urljoin(cls.base_url, qs)

    @abstractmethod
    def _get_nav_links(self):
        """находит ссылки пагинации"""
        pass

    @staticmethod
    def _get_query_key(url, key):
        """
        хелпер достает ключи из GET-параметров
        _get_query_key('/url?foo=bar', 'foo') -> 'bar'
        """
        query = urlsplit(url).query
        values = parse_qs(query).get(key, [''])
        return values if len(values) > 1 else values[0]

    def _get_page_num(self, url):
        """достает идентификатор пагинации из url"""
        page_str = self._get_query_key(url, self.page_key)
        return int(page_str) if page_str else 0

    def _map_nav_link(self, link=None):
        """
        преобразует ссылки пагинации в кортежи (номер страницы, url)
        для последующей сортировки
        """
        url = self.url if link is None else link['href']
        return self._get_page_num(url), urljoin(self.base_url, url)

    def get_next_page_url(self):
        """возвращает url следующей за текущей страницы (если есть)"""
        current = self._map_nav_link()
        page_links = map(self._map_nav_link, self._get_nav_links())
        next_pages = sorted(filter(lambda page: page > current, page_links))
        next_pages_url = next_pages[0][1] if next_pages else ''
        logger.debug(f'...got {next_pages_url or "no"} next page.')
        return next_pages_url
