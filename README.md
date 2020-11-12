# searchbot
Программа-поисковик.

Осуществляет поиск заданной строки в посковой системе (Google/Yandex), от
результатов на поисковой странице осуществляет рекурсивный поиск вглубь, либо
просто забирает результаты поиска.

## Установка
* Клонируйте репозиторий в выбранную папку
* Создайте PYTHON-окружение
```bash
python -m venv venv
source venv/bin/activate
```
* Соберите и установите пакет
```bash
pip install wheel
python setup.py bdist_wheel
cd dist
pip install *.whl
```

## Использование
Все параметры задаются ключами
```bash
searchbot --help

Usage: searchbot [OPTIONS] QUERY

  a simple search bot with a deep scanning feature

Options:
  -c, --count INTEGER             a number of results  [default: 1]
  -e, --engine [google|yandex]    a search engine for initial results
                                  [required]

  -r, --recursive / --no-recursive
                                  a search method  [default: False]
  -o, --output FILE               write results to a file instead of terminal
                                  (supported: csv, json)

  -v, --verbosity                 show process details: -v, -vv
  --help                          Show this message and exit.

```

Пример использования.
```bash
searchbot OTUS -c 10 -e google -r -o results.json -vv
```
Ищет в Google "OTUS", от первой ссылки начинает рекурсивный поиск, собирает 10
ссылок, результаты сохраняет в файл results.json в формате JSON, в консоль
осоществляется вывод отладочной информации.

## Фичи
1. -e - доступны поисковые системы Google и Yandex
2. -o - сохранение результатов в CSV и JSON (выбирается по расширению файла),
либо вывод в терминал
3. -r - рекурсивный поиск
4. -v - логирование в STDERR, уровни: 0 - ERROR, 1 - INFO, 2 - DEBUG 
