import logging

from .google import GoogleResponseParser
from .yandex import YandexResponseParser
from .common import CommonResponseParser

logger = logging.getLogger(__name__)
available_parsers = {
    'google': GoogleResponseParser,
    'yandex': YandexResponseParser,
    'default': CommonResponseParser
}


def get_parser(name='default'):
    try:
        return available_parsers[name]
    except KeyError:
        logger.error(f'{name} parser not implemented.')
