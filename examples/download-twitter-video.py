import sys
sys.path.insert(0,'..')

from scraper import *
from sys import argv
# tweet_url = 'https://twitter.com/Tezha4me/status/1014920049843372044'
tweet_url = argv[1]
api_url = 'http://twittervideodownloader.com/'

s = Scraper()
s.get(api_url)
soup = s.html_soup()
form = soup.select_one('form')
csrf = form.select_one('input[type="hidden"]')
form_data = {
  'tweet': tweet_url,
  csrf['name']: csrf['value'],
}
res = s.post(api_url+'download', data= form_data)
if res.status_code == 200:
  soup = s.html_soup()
  anchors = soup.select('a[href^="https://video"]')
  anchors = [a['href'] for a in anchors]
  ## get a with the highest resolution
  link = ''
  resolution = 0
  from re import search
  resolution_ptrn = r'\d+x\d+'
  for a in anchors:
    r = search(resolution_ptrn, a)
    r = r and int(r.group().split('x')[0])
    if r > resolution:
      resolution = r
      link = a
  s.download(link, './' + link.split('/')[-1].split('?')[0]  )
