#!/usr/bin/python

import requests
import re
import browser_cookie3
import random
import string
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bs4 import BeautifulSoup


class String:
	def clean_string(self, string):
		return re.sub(r'\W', '', string)
	
	def random_string(self, length=20):
		space = self.clean_string(string.printable)
		return ''.join([random.choice(space) for i in range(length)])


class UrlParser:
	def __init__(self, url):

		prorocol_link = url.split('://')
		if len(prorocol_link) == 1:
			prorocol_link = ['', url]
		
		protocol, link = prorocol_link
		host, *path = link.split('/')
		path = '/'.join(path)

		path_query = path.split('?')
		if len(path_query) == 1:
			path_query = [path, '']

		path, query = path_query
		domain = '.'.join(host.split('.')[-2:]).split(':')[0]
		
		self.protocol = protocol
		self.path = path
		self.domain = domain
		self.host = host
		self.query = query

		self.__get_params()

	def __get_params(self):
		query = self.query
		if not query: return

		params = {}
		query = query.split('&')

		for q in query:
			name, val = q.split('=')
			params[name] = val

		self.params = params


class Cookies:
	def get_cookies(self, browser, website):
		""" 
			get all cookies from the browser 
			determine the browser firefox | chrome | both
			then filter the output on specific website

			output return in [{'name': 'cookie_name', 'value': 'cookie_value'}, {...}, .....]
		"""
		if browser == 'firefox':
			browser = browser_cookie3.firefox
		elif browser == 'chrome':
			browser = browser_cookie3.chrome
		else:
			browser = browser_cookie3.load
		cookie_jar = browser(domain_name = website)
		
		cookies = []
		for c in cookie_jar:
			cookie = {'domain': None, 'name': c.name, 'value': c.value, 'secure': c.secure and True or False}
			if c.expires: cookie['expiry'] = c.expires
			if c.path_specified: cookie['path'] = c.path
			cookies.append(cookie)
		return cookies


class Browser(Cookies):
	'''
		scrape using selenium firefox
		this is functions uses alot
	'''
	def __init__(self, hide=False):
		self.__config_browser__(hide)
		print('browser has configured')

	def __config_browser__(self, hide):
		options = Options()

		options.set_headless(headless=hide)

		self.driver = webdriver.Firefox(firefox_options=options)
		self.driver.implicitly_wait(20)
		self.driver.set_script_timeout(1000)
		print('browser has opened')

	def fill_input(self, selector, value):
		element = self.driver.find_element_by_css_selector(selector)
		element.clear()
		element.send_keys(value)

	def click_btn(self, selector):
		self.driver.find_element_by_css_selector(selector).click()

	def set_cookies(self, cookies):
		for cookie in cookies:
			# print(cookie)
			self.driver.add_cookie(cookie)

	def exec_js(self, jsCode, returnVar=''):
		""" 
			put "done();" whenever you want stop if your code need to wait 
			returnVar is variable you want its value
		"""
		index = jsCode.find('done();')
		if index >= 0:
			jsCode = jsCode.replace('done();', f'done({returnVar});')
			jsCode = 'var done = arguments[0]; ' + jsCode

			func = self.driver.execute_async_script
		else:
			jsCode = f'{jsCode.rstrip(";")}; return {returnVar};'
			func = self.driver.execute_script            
		return func(jsCode)

	def infinite_scroll(self):
		self.exec_js('var intrvl = setInterval(()=>{ window.scrollBy(0, 500) }, 500)', returnVar='intrvl')

	def get(self, link, with_cookies=False):
		self.driver.get(link)
		if with_cookies:
			## .removeProtocol.removePath.removeSubDomain
			# domain = '.'.join(link.split('//')[-1].split('/', 1)[0].split('.')[-2:])
			link = UrlParser(link)
			cookies = self.get_cookies('firefox', link.domain )
			time.sleep(2)
			self.set_cookies(cookies)
			time.sleep(2)
			self.driver.get(link)

	def page_src(self):
		return self.driver.page_source


class Scraper(Cookies, String):
	'''
		scrape using requests.session
		this is functions uses alot
	'''
	def __init__(self):
		## args
		self.soup = None
		self.src = None

		self.__setup__()

	def __setup__(self):
		self.session = requests.Session()
		self.session.headers.update({
			## very common user-agent
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
		})

	def set_cookies(self, cookies):
		for cookie in cookies:
			self.session.cookies.set(cookie['name'], cookie['value'])

	def get(self, link):
		response = self.session.get(link)
		self.src = response.text
		return response

	def post(self, link, data= {}):
		response = self.session.post(link, data = data)
		self.src = response.text
		return response

	def regex(self, ptrn):
		ptrns = {
			'ilink': r'(href|src)="(/[^"\s]+)"*?',
			'xlink': r'(href|src)="(http[s]*://[^"\s]+)"',
			'link' : r'(href|src)="((https:/)*/[^"\s]+)"',
		}
		ptrn = ptrns.get(ptrn) or ptrn
		find = re.findall(ptrn, self.src)
		return find

	def download(self, link, location=None):
		url = UrlParser(link)
		location = location or './' + url.path.strip('/').split('/')[-1]
		
		res = requests.get(link)
		
		with open(location, 'wb') as f:
			f.write(res.content)

	def write(self, data, location, append=True):
		encode = {'encoding': 'UTF-8', 'errors': 'ignore'}
		data = data.encode(**encode).decode(**encode)

		location = location or f'./{self.random_string()}.txt'

		with open(location, 'a' if append else 'w') as f:
			f.write(data)

	def html_soup(self):
		if self.src:
			return BeautifulSoup(self.src, 'html.parser')
		return BeautifulSoup('', 'html.parser')


class ExtraBeautifulSoup:
	"""docstring for ExtraBeautifulSoup"""
	def __init__(self, soup):
		super(ExtraBeautifulSoup, self).__init__()

		self.main = soup ## main soup will never change when created instance
		self.soup = soup ## change with functions


	def elm_text_contain(self, selector, text):
		elms = self.soup.select(selector) 
		text = text.lower()
		return list( filter( lambda elm: text in elm.text.lower(), elms) )

	def elm_contain_elm(self, selectorParent, selectorChild):
		elms = self.soup.select(selectorParent)
		return list( filter( lambda elm: elm.select_one(selectorChild) != None , elms ) )

	def elm_contain_elm_with_text(self, selectorParent, selectorChild, text):
		elms = self.elm_contain_elm(selectorParent, selectorChild)
		filtered = []
		for elm in elms:
			self.soup = elm
			if self.elm_text_contain(selectorChild, text):
				filtered.append(elm)
		## for future work
		self.soup = self.main

		return filtered

	def parent_until(selectorChild, selectorParent):
		pass

	def brother_to(selector, selectorWanted):
		pass
