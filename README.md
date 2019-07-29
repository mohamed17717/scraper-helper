# Scraping Helper

Classes that saves time doing repeated stuff in scraping process.

## Getting Started

### Prerequisites

- [Python3.6](https://www.python.org/downloads/) or later

#### For Browser class

- [Firefox](https://www.mozilla.org/en-US/firefox/)
- [Selenium](https://pypi.org/project/selenium/)
- [Geckodriver](https://github.com/mozilla/geckodriver/releases)

### Installing

#### Clone The repository and install dependencies

``` bash
git clone https://github.com/mohamed17717/scraper-helper.git <filename>
cd <filename>
pip install -r requirements.txt
```

## Running the tests

Explain how to run the automated tests for this system

> **Scraper** class.\
> `scrape facebook video using your login cookies`

```python
from scraper import Scraper
s = Scraper()
video_link = 'https://www.facebook.com/livingin2077/videos/2296419330686852/'
s.download(link=video_link)
```

## Built With

- **Requests** - Lib for Scraping the web
- **Beautiful Soup** - Parse HTML
- **Selenium** - To control the browser

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
