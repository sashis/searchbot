import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name='searchbot',
    version='0.1.0',
    py_modules=['searchbot'],
    include_package_data=True,
    license='MIT License',
    description='a simple search bot performing a recursive page scanning',
    long_description=README,
    url='https://github.com/sashis/searchbot',
    author='Aleksandr Kropanev',
    author_email='kropanev@mail.ru',
    keywords = ['search', 'bot', 'training', 'OTUS'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'click',
    ],
    entry_points='''
        [console_scripts]
        searchbot=searchbot:main
    ''',
)
