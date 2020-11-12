import logging
import click

from searchbot.searchtools import make_search, format_data
from searchbot.renders import get_render_by_filename

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s [%(levelname)s]: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def set_verbosity(level):
    limit_level = level if level <= 2 else 2
    verbosity = logging.ERROR, logging.INFO, logging.DEBUG
    logger.setLevel(verbosity[limit_level])


@click.command()
@click.option('-c', '--count', default=1,
              show_default=True, help='a number of results')
@click.option('-e', '--engine', type=click.Choice(['google', 'yandex']),
              required=True, help='a search engine for initial results')
@click.option('--recursive/--no-recursive', '-r/ ', default=False,
              show_default=True, help='a search method')
@click.option('-o', '--output', metavar='FILE',
              help='write results to a file instead of terminal '
                   '(supported: csv, json)')
@click.option('-v', '--verbosity', count=True,
              help='show process details: -v, -vv')
@click.argument('query')
def main(query, engine, count, recursive, output, verbosity):
    """a simple search bot with a deep scanning feature"""

    set_verbosity(verbosity)
    results = make_search(query, engine, count, recursive)
    render = get_render_by_filename(output)
    render(format_data(results), output)
    logger.info('The results is successfully rendered.')
