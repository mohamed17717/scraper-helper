import sys
sys.path.insert(0,'..')

from scraper import  *
from time import sleep
from random import choice

class FbAcc:
	"""docstring for FbAcc"""
	def __init__(self, userUrl):
		super(FbAcc, self).__init__()
		
		url = userUrl.replace('https://www', 'https://mbasic')
		*base, profileId = url.split('/')

		self.userUrl   = userUrl
		self.base      = '/'.join(base)
		self.profileId = profileId
		self.s         = Scraper()

		self.allowedAlbums = [
			'Cover Photos',
			'Instagram Photos',
			'Profile Pictures'
		]

		## sections
		self.photosUrl = None
		self.infoUrl   = None
		## albums
		self.albums    = None
		## imgs inside albums
		self.albumsImgs= None
		## page of opened img
		self.imgUrls   = None

		self.s.set_cookies( self.s.get_cookies('firefox', 'facebook.com') )

		self.__generateUrl__()
		
	def __generateUrl__(self):
		## generate photoUrl and InfoUrl
		profileId = self.profileId

		if profileId.startswith('profile.php?id='):
			profileId = profileId.split('&')[0]
			self.profileId = profileId[len('profile.php?id='):]
			profileId += '&v=%s'
			photosUrl = profileId % 'photos'
			infoUrl = profileId % 'info'
		else:
			profileId = profileId.split('?')[0]
			self.profileId = profileId
			photosUrl = f'{profileId}/photos'
			infoUrl = f'{profileId}/about'

		self.photosUrl = f'{self.base}/{photosUrl}'
		self.infoUrl   = f'{self.base}/{infoUrl}'

	def getAlbums(self):
		print('url:', self.photosUrl)
		self.s.get(self.photosUrl)

		soup = self.s.html_soup()
		print(soup)
		print(self.s.src)

		## get albums area
		divs = soup.select('div')
		albums = None
		for div in divs:
			if div.h3 and div.h3.text.lower() == 'albums':
				albums = div
				break 

		if albums:
			divs   = albums.select('div')
			albums = []

			if len(divs) == 1:
				urls = divs[0].select('a[href]')
				albums.extend( [self.base + url['href'] for url in urls if url.text in self.allowedAlbums] )

			elif len(divs) == 2:
				albumsUrl = divs[1].select_one('a[href]')
				albumsUrl = albumsUrl and self.base + albumsUrl['href']

				
				## loop to get all albums
				while albumsUrl:
					self.s.get(albumsUrl)
					soup = self.s.html_soup()
					*anchors, last = soup.select('table a[href]')
					[albums.append(a['href']) for a in anchors if a.text in self.allowedAlbums]
					if 'owner_id' in last['href']:
						albumsUrl = last['href']
					elif last.text in self.allowedAlbums:
						albums.append(last['href'])
						albumsUrl = None

					sleep(choice([2,3,4]))

			self.albums = albums

	def __checkImgAlt__(self, img):
		#print('start filtering images on alt')
		print(img)
		alt = img['alt']
		whiteList = ['person', 'people']
		# return any( [i in alt.lower() for word in whiteList] )
		for word in whiteList:
			if not alt: break
			if word in alt:
				return True
		return False

	def getAlbumsImages(self):
		print('start get album images')
		albums = self.albums
		if albums:
			images = []
			for albumLink in albums:
				while albumLink:
					self.s.get(albumLink)
					soup = self.s.html_soup()
					anchors = soup.select('table a[href^="/photo"]')
					images.extend( [ self.base + a['href'] for a in anchors if self.__checkImgAlt__(a.img) ] )

					albumLink = soup.select_one(f'table a[href^="/{self.profileId}"]')
					albumLink = albumLink and self.base + albumLink['href'] or None
					sleep(choice([2,3,4]))
			self.albumsImgs = images

	def getImagesUrls(self):
		print('start get images url')
		images = self.albumsImgs
		if images:
			imgUrls = []
			for img in images:
				self.s.get(img)
				soup = self.s.html_soup()
				img = soup.select_one('a[href^="/photo/view_full_size/"]')
				if img: imgUrls.append( self.base+img['href'] )
				sleep(choice([2,3,4]))
			self.imgUrls = imgUrls

	def download(self):
		print('start downloading')
		imgs = self.imgUrls
		num = 0
		for img in imgs:
			self.s.get(img)
			soup = self.s.html_soup()
			script = soup.script
			url = script.text.replace('\\', '')
			url = url[len('document.location.href="'): -1]

			self.s.download(url, f'./{self.profileId}({num}).jpg')
			num += 1

	def run(self):
		self.getAlbums()
		self.getAlbumsImages()
		self.getImagesUrls()
		self.download()

if __name__ == '__main__':
	if len(sys.argv) == 2:
		## modify that link
		userUrl  = sys.argv[1]
		acc = FbAcc(userUrl)
		acc.run()
	else:
		print('you must pass correct argv')
