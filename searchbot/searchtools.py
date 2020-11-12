import logging

import requests

from searchbot.parsers import CommonResponseParser, get_parser

logger = logging.getLogger(__name__)


def format_data(data):
    """форматирование данных для рендера"""
    return tuple(
        (i, title, url) for i, (url, title) in enumerate(data.items(), 1)
    )


def fetch_page(url, session=None):
    """
    Мягкий фетчер страниц, отдает при любых IO- и HTTP-ошибках пустой объект

    :param url: сслыка на страницу
    :param session: можно передать сессию для сохранения куков и прочего
    :return: объект Response() загруженной страницы или пустой
    """
    fetcher = session or requests
    try:
        response = fetcher.get(url)
        response.raise_for_status()
    except requests.RequestException:
        response = requests.Response()
    return response


def se_search(query, parser):
    """
    Поиск строки в поисковой системе

    :param query: строка поиска
    :param parser: парсер страниц поисковой системы
    :return: генератор результатов поиска
    """
    session = requests.Session()
    url = parser.make_init_url(query)
    while url:
        page = parser(fetch_page(url, session))
        yield from page.get_results()
        url = page.get_next_page_url()


def deep_search(url, count, results):
    """
    Рекурсивный поиск от стартовой точки.

    Условия выхода: найдено нужное количество ссылок,
    либо закончились уникальные ссылки.
    Для обеспечения уникальности результатов состояние результатов
    доступно в каждой итерации, поэтому функция грязная.

    :param url: стартовая точка
    :param count: предельное количество ссылок
    :param results: словарь результатов поиска
    :return: словарь {ссылка: наименование}
    """
    if url in results:
        logger.debug(f'Already have {url}, skip it.')
        return {}
    if len(results) == count:
        return {}
    logger.debug(f'Dive in {url}...')
    page = CommonResponseParser(fetch_page(url))
    title = page.get_title()
    if not title or title in results.values():
        logger.debug(f'Already have \'{title}\', skip it.')
        return {}
    new_urls = [url for url in page.get_results() if url not in results]
    logger.debug(f'...got {len(new_urls)} new url(s).')
    results[page.url] = title
    logger.info(f'Store new result {title}: {url} ({len(results)}/{count})')
    [deep_search(new_url, count, results) for new_url in new_urls]
    return results


def make_search(query, parser_name, count, is_recursive):
    """
    Главная функция поиска. Берем результаты с поисковой страницы
    и рекурсивно бежим внутрь, без рекурсии - берем только текущую ссылку

    :param query: строка поиска
    :param parser_name: поисковая система
    :param count: количество результатов
    :param is_recursive: флаг рекурсивного поиска
    :return: словарь {ссылка: наименование}
    """
    results = {}
    parser = get_parser(parser_name)
    logger.info(
        f'Initialize new search for {count} links of \'{query}\' in '
        f'{parser_name} with {is_recursive and " " or "no "}recursion.'
    )
    for url in se_search(query, parser):
        deep_count = count - len(results) if is_recursive else 1
        results.update(deep_search(url, deep_count, {}))
        if len(results) == count:
            break
    logger.info(f'Finished, got {len(results)} result(s).')
    return results
