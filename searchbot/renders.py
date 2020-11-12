import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def get_render_by_filename(filename):
    """селектор рендера по расширению файла либо дефолтный"""
    fname = filename or ''  # может быть None на входе
    ext = fname.split('.')[-1]
    renders = {
        'json': json_render,
        'csv': csv_render,
        'terminal': terminal_render
    }
    render_name = ext if ext in renders else 'terminal'
    logger.debug(f'Choosing the {render_name} render')
    return renders[render_name]


def json_render(data, filename):
    logger.debug(f'Writing results to "{filename}"...')
    results = [
        dict(item=item, title=title, url=url) for item, title, url in data
    ]
    with open(Path() / filename, 'w') as fp:
        json.dump({'results': results}, fp, ensure_ascii=False, indent=2)


def csv_render(data, filename):
    logger.debug(f'Writing results to "{filename}"...')
    fieldnames = 'item', 'title', 'url'
    with open(Path() / filename, 'w', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(fieldnames)
        writer.writerows(data)


def terminal_render(data, filename):
    logger.debug(f'Sending results to the terminal...')
    width = len(str(len(data)))
    header = ' Результаты поиска '.center(80, '-')
    print(header)
    for item, title, url in data:
        print(f'{item:>{width}}. {title} ({url})')
