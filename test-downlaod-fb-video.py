from scraper import *
from urllib.parse import unquote
url = input('Enter video url: ').replace('https://www', 'https://m')
s = Scraper()
s.get(url)
soup = s.html_soup()
a = soup.select_one('a[href^="/video_redirect/?src="]')
if a:
  a = unquote( a['href'].replace('/video_redirect/?src=', '') )
  s.download(a)

