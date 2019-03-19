from scraper import *
from os import mkdir
userName = input('Enter userName: ')
url = 'https://twitter.com/%s/' % userName
b = Browser(hide= False)
b.get(url)
jsCode = '''var username=window.location.pathname.split("/")[1],gifs=[],repeated=0,scroll_height=0,scroll_intrvl=setInterval(()=>{repeated>=10&&(clearInterval(scroll_intrvl),clearInterval(capture_gifs_intrvl)),scroll_height>=document.body.scrollHeight?repeated++:(scroll_height+=window.innerHeight,repeated=0,window.scrollBy(0,window.innerHeight))},500),capture_gifs_intrvl=setInterval(()=>{vids=document.querySelectorAll("video"),vids.forEach(e=>{src=e.src,src.endsWith(".mp4")&&!gifs.includes(src)&&gifs.push(src)})},250);'''
gifs = b.exec_js(jsCode, returnVar='gifs')
output_location = './%s-gifs/' % userName
mkdir(output_location)
s= Scraper()
for gif in gifs:
	print(gif)
	gifName = gif.split('/')[-1]
	s.download(gif, output_location + gifName)
