from scraper import *
from os import mkdir
userName = input('Enter userName: ')
url = 'https://twitter.com/%s/media' % userName
b = Browser(hide= True)
b.get(url)
jsCode = '''var pop_intrvl=setInterval(()=>{var pop_elm=document.querySelectorAll('div.rn-13w96dm:nth-child(1)');if(pop_elm[0]){pop_elm[0].click();clearInterval(pop_intrvl);}},500);var repeated=0,scroll_height=0,scroll_intrvl=setInterval(()=>{if(repeated>5){clearInterval(scroll_intrvl);captureGifs();setTimeout(scrollToTop(),200);} if(scroll_height===document.body.scrollHeight){repeated++;}else{scroll_height=document.body.scrollHeight;repeated=0;window.scrollBy(0,scroll_height);}},700);function scrollToTop(){var scroll=pageYOffset,inverse_scroll_intrvl=setInterval(()=>{if(scroll<=0){clearInterval(inverse_scroll_intrvl);clearInterval(capture_gifs_intrvl);done();} scroll-=1500;scrollTo(0,scroll);},700);} var gifs=[],capture_gifs_intrvl=0;function captureGifs(){capture_gifs_intrvl=setInterval(()=>{vids=document.querySelectorAll('video');vids.forEach((elm)=>{src=elm.src;if(src.endsWith('.mp4')&&!gifs.includes(src)){gifs.push(src);}})},500);}'''
gifs = b.exec_js(jsCode, returnVar='gifs')
s= Scraper()
output_location = input('output location : ') + '/%s-gifs/' % userName
mkdir(output_location)
for gif in gifs:
	print(gif)
	gifName = gif.split('/')[-1]
	s.download(gif, output_location + gifName)