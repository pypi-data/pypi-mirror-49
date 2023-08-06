[![PyPI Version](https://img.shields.io/pypi/v/news-fetch.svg)](https://pypi.org/project/news-fetch)
[![Coverage Status](https://coveralls.io/repos/github/santhoshse7en/news-fetch/badge.svg?branch=master)](https://coveralls.io/github/santhoshse7en/news-fetch?branch=master)
[![License](https://img.shields.io/pypi/l/news-fetch.svg)](https://pypi.python.org/pypi/news-fetch/)
[![Documentation Status](https://readthedocs.org/projects/pip/badge/?version=latest&style=flat)](https://santhoshse7en.github.io/news-fetch_doc)

# news-fetch

news-fetch was built on top of [news-please](https://pypi.org/project/news-please/) - [Felix Hamborg](https://www.linkedin.com/in/felixhamborg/) and [Newspaper3K](https://pypi.org/project/newspaper3k/) - [Lucas (欧阳象) Ou-Yang](https://www.linkedin.com/in/lucasouyang/) 'Thank You' both you without them it will be very hard to extract online newspaper. This package consist of both features provided my Felix's work and Lucas' work

news-fetch is an open source, easy-to-use news crawler that extracts structured information from almost any news website. . I built this to reduce most of NaN or '' or [] or 'None' values while scraping for some newspapers. Platform-independent and written in Python 3. This package can be very easily used by programmers and developers to provide access to the news data to their programs.

| Source         | Link                                         |
| ---            |  ---                                         |
| PyPI:          | https://pypi.org/project/news-fetch/             |
| Repository:    | https://santhoshse7en.github.io/news-fetch/      |
| Documentation: | https://santhoshse7en.github.io/news-fetch_doc/  |

## Dependencies

- news-please
- newspaper3k
- beautifulsoup4
- fake_useragent
- selenium
- chromedriver-binary
- fake_useragent
- spacy
- pandas

## Dependencies Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following
```bash
pip install -r requirements.txt
```

## Usage

Download it by clicking the green download button here on [Github](https://github.com/santhoshse7en/news-fetch/archive/master.zip). To extract URLs from targeted website call google_search function, you only need to parse argument of keyword and newspaper link.

```python
>>> from newsfetch.news import google_search
>>> google = google_search('Alcoholics Anonymous', 'https://timesofindia.indiatimes.com/')
```

**Directory of google search results urls**

![google](https://user-images.githubusercontent.com/47944792/60381562-67363380-9a74-11e9-99ea-51c27bf08abc.PNG)

To scrape the all news details call newspaper function

```python
>>> from newsfetch.news import newspaper
>>> news = newspaper('https://www.bbc.co.uk/news/world-48810070')
```

**Directory of news**

![newsdir](https://user-images.githubusercontent.com/47944792/60564817-c058dc80-9d7e-11e9-9b3e-d0b5a903d972.PNG)

```python
>>> news.headline

'g20 summit: trump and xi agree to restart us china trade talks'
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
