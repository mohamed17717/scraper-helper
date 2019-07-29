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

### **Scraper** class

> `downlaod video`

```python
from scraper import Scraper
s = Scraper()
video_link = 'https://video.faly2-1.fna.fbcdn.net/v/t42.9040-2/62397431_315586462709416_146625252862984192_n.mp4?_nc_cat=102&efg=eyJ2ZW5jb2RlX3RhZyI6InN2ZV9zZCJ9&_nc_oc=AQkgWetwMBu9sezw9cSv95KrlX03X1wX_ZOaSzMxtmcfq1_Ix_tXVWefEr2Xyq_8Ka4&_nc_ht=video.faly2-1.fna&oh=4ca74f2b4d64ea2856819efa3ce4fe4f&oe=5D3E91FB'
s.download(link=video_link)
```

> `download Facebook video using cookies`

``` python
from scraper import *
from urllib.parse import unquote

url = 'https://www.facebook.com/livingin2077/videos/2296419330686852/'
url = url.replace('www.', 'm.')
parsed_url = UrlParser(url)

s = Scraper()

cookies = s.get_cookies('firefox', parsed_url.domain)
s.set_cookies(cookies)

s.get(url)
soup = s.html_soup()

a = soup.select_one('a[href^="/video_redirect"]')
video_link = unquote( a['href'].replace('/video_redirect/?src=', '') )
s.download(video_link)
```

### **Browser** class

> `Login to instagram`

``` python
from scraper import Browser
from time import sleep

b = Browser(hide=False)
b.get('http://instagram.com', with_cookies=False)
sleep(1)
b.click_btn('a[href^="/accounts/login"]')
sleep(1)
b.fill_input('input[name="username"]', 'any_user')
b.fill_input('input[name="password"]', 'wrong password')
b.click_btn('button[type="submit"]')
```

> and so on.\
> scripts are much smaller than before.\
> there is much more capabilites i hope u find out

## Built With

- **Requests** - Lib for Scraping the web
- **Beautiful Soup** - Parse HTML
- **Selenium** - To control the browser

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
