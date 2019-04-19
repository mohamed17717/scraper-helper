import sys
sys.path.insert(0,'..')

from scraper import *
from urllib.parse import unquote
url = input('Enter video url: ').replace('https://www', 'https://m')
s = Scraper()
## to scrape from closed group uncomment
cookies = s.get_cookies('firefox', 'facebook.com')
s.set_cookies(cookies)
s.get(url)
soup = s.html_soup()
a = soup.select_one('a[href^="/video_redirect/?src="]')
if a:
  a = unquote( a['href'].replace('/video_redirect/?src=', '') )
  s.download(a)

