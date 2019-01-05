#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from json import loads, dumps
from time import sleep, time
import requests
from re import findall
from bs4 import BeautifulSoup
import browser_cookie3

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
            jsCode = returnVar and jsCode.replace('done();', 'done(%s);' % returnVar) or jsCode
            jsCode = 'var done = arguments[0]; %s' % jsCode

            func = self.driver.execute_async_script
        else:
            jsCode = jsCode.rstrip(';') + '; return %s;' % returnVar 
            func = self.driver.execute_script            
        return func(jsCode)


    def infinite_scroll(self):
        self.exec_js('var intrvl = setInterval(()=>{ window.scrollBy(0, 500) }, 500)', returnVar='intrvl')

    def get(self, link, with_cookies=False):
        self.driver.get(link)
        if with_cookies:
            ## .removeProtocol.removePath.removeSubDomain
            domain = '.'.join(link.split('//')[-1].split('/', 1)[0].split('.')[-2:])
            cookies = self.get_cookies('firefox', domain )
            self.set_cookies(cookies)
            self.driver.get(link)

    def page_src(self):
        return self.driver.page_source

class Scraper(Cookies):
    '''
        scrape using requests.session
        this is functions uses alot
    '''
    def __init__(self):
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

    def regex(self, ptrn):
        ptrns = {
            'ilink': r'(href|src)="(/[^"\s]+)"*?',
            'xlink': r'(href|src)="(http[s]*://[^"\s]+)"',
            'link' : r'(href|src)="((https:/)*/[^"\s]+)"',
        }
        ptrn = ptrns.get(ptrn) or ptrn
        find = findall(ptrn, self.src)
        return find

    def download(self, link, location):
        with open(location, 'wb') as f:
            res = requests.get(link)
            f.write(res.content)
            f.close()

    def write(self, data, location):
        with open(location, 'a') as f:
            f.write(data)
            f.close()

    def html_soup(self):
        if self.src:
            return BeautifulSoup(self.src, 'html.parser')
        return BeautifulSoup('', 'html.parser')



