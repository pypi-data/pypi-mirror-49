from .model import Anime

import requests
from bs4 import BeautifulSoup

import time


class MALScraper:
    """Scrapes https://myanimelist.net/ using BeautifulSoup4."""

    # MAL search url
    MAL_URL = 'https://myanimelist.net/anime.php?q='

    @classmethod
    def get_anime(cls, anime):
        anime_url = cls.get_anime_url(anime)
        return Anime(anime_url)

    @classmethod
    def get_anime_url(cls, anime):
        url = cls.MAL_URL + anime

        res = requests.get(url)
        while res.status_code != 200:
            time.sleep(1)
            res = requests.get(url)

        soup = BeautifulSoup(res.text, features='lxml')
        lnk = None
        try:
            a = soup.find('a', {'class': 'hoverinfo_trigger fw-b fl-l'})
            lnk = a['href']
        except Exception as e:
            print('Error getting anime url.\nError: {e}')
        return lnk
