import requests
from bs4 import BeautifulSoup
import html, re

class Deezer:
    def __init__(self, url: None):
        self._url_ = url
        self.__regex__url_deezer = re.match(
            r"https?://(www.deezer.com/us/track)\/(.*)", url)
        self._headers_ ={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
         
    @property
    def title(self):
        if not self.__regex__url_deezer:
            return "Invaild url format (Music-debugger) (i.e https://www.deezer.com/us/track/1257838602)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:title").get('content'))

    @property
    def type(self):
        if not self.__regex__url_deezer:
            return "Invaild url format (Music-debugger) (i.e https://www.deezer.com/us/track/1257838602)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:type").get('content'))

    @property
    def description(self):
        if not self.__regex__url_deezer:
            return "Invaild url format (Music-debugger) (i.e https://www.deezer.com/us/track/1257838602)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:description").get('content'))


    @property
    def author(self):
        if not self.__regex__url_deezer:
            return "Invaild url format (Music-debugger) (i.e https://www.deezer.com/us/track/1257838602)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="music:musician").get('content'))

    @property
    def image(self):
        if not self.__regex__url_deezer:
            return "Invaild url format (Music-debugger) (i.e https://www.deezer.com/us/track/1257838602)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:image").get('content'))

    @property
    def audio(self):
        if not self.__regex__url_deezer:
            return "Invaild url format (Music-debugger) (i.e https://www.deezer.com/us/track/1257838602)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:audio").get('content'))
