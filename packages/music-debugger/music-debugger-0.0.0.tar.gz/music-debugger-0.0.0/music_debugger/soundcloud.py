import requests
from bs4 import BeautifulSoup
import html, re

class SoundCloud:
    def __init__(self, url):
        self._url_ = url
        self.__regex__url_sound_cloud = re.match(r"https?://(soundcloud.com|snd.sc)\/(.*)", url)
        self._headers_ ={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        }
         
    @property
    def title(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/smilez/happy-ft-snoop-dogg-1)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:title").get('content'))

    @property
    def type(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/smilez/happy-ft-snoop-dogg-1)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:type").get('content'))

    @property
    def description(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/smilez/happy-ft-snoop-dogg-1)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:description").get('content'))

    @property
    def like_count(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/smilez/happy-ft-snoop-dogg-1)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="soundcloud:like_count").get('content'))

    @property
    def play_count(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/smilez/happy-ft-snoop-dogg-1)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="soundcloud:play_count").get('content'))

    @property
    def download_count(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/smilez/happy-ft-snoop-dogg-1)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="soundcloud:download_count").get('content'))

    @property
    def comments_count(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/smilez/happy-ft-snoop-dogg-1)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="soundcloud:comments_count").get('content'))

    @property
    def author(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/smilez/happy-ft-snoop-dogg-1)"
        req = requests.get(
            self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="soundcloud:user").get('content'))

    @property
    def image(self):
        if not self.__regex__url_sound_cloud:
            return "Invaild url format (Music-debugger) (i.e https://soundcloud.com/smilez/happy-ft-snoop-dogg-1)"
        req = requests.get(self._url_, headers=self._headers_)
        soup = BeautifulSoup(req.content, 'html.parser')
        return html.unescape(soup.find("meta", property="og:image").get('content'))