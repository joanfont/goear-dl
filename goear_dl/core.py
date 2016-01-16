from string import capwords
import requests
import os
from bs4 import BeautifulSoup

from goear_dl.entities import Song
from goear_dl.compat import url_quote


class SongNotFoundError(Exception):
    pass


class GoearSearch(object):
    GOEAR_SEARCH = 'http://www.goear.com/search'
    GOEAR_PLAY = 'http://www.goear.com/listen'

    WRAPPER_ID = 'main'
    LIST_OF_ELEMENTS_CLASS = 'board_list'
    LIST_ITEM_CLASS = 'board_item'
    BOARD_CONTENT_CLASS = 'board_content'
    SONG_URL_PROP = 'redir'
    SONG_TITLE_CLASS = 'title'
    SONG_ARTIST_CLASS = 'band'
    SONG_BIT_RATE_CLASS = 'kbps'
    SONG_LENGTH_CLASS = 'length'

    SONG_TITLE_META_OG_PROPERTY = 'og:title'

    @classmethod
    def search(cls, criteria):
        url = cls.__build_search_url(criteria)
        raw_soup = cls.__get_soup(url)
        soup = raw_soup.find('div', {'id': cls.WRAPPER_ID})

        list_of_elements = soup.find({'ol', cls.LIST_OF_ELEMENTS_CLASS})
        elements = list_of_elements.find_all('li', {'class': cls.LIST_ITEM_CLASS})

        return map(cls.__get_song_from_list, elements)

    @classmethod
    def find_by_url(cls, song_url):
        soup = cls.__get_soup(song_url)

        og_title_tag = soup.find('meta', attrs={'property': cls.SONG_TITLE_META_OG_PROPERTY})
        og_title = og_title_tag.get('content')

        song_url_parts = song_url.split('/')
        song_id = song_url_parts[4]

        title, artist = og_title.split(' - ', 1)
        title = capwords(title)
        artist = capwords(artist)

        song_dict = {
            'song_id': song_id,
            'title': title,
            'artist': artist,
            'url': song_url
        }

        return Song(**song_dict)

    @classmethod
    def find_by_id(cls, song_id):
        song_url = '{base_url}/{song_id}'.format(cls.GOEAR_PLAY, song_id)
        return cls.find_by_url(song_url)

    @classmethod
    def __build_search_url(cls, criteria, page=1):
        criteria_encoded = url_quote(criteria.lower())
        url = '{base_url}/{criteria}'.format(base_url=cls.GOEAR_SEARCH, criteria=criteria_encoded)
        if page != 1:
            url = '{base_url}/{page}'.format(base_url=url, page=page)
        return url

    @classmethod
    def __get_soup(cls, url):
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @classmethod
    def __get_song_from_list(cls, element):
        ul = element.find('ul', {'class': cls.BOARD_CONTENT_CLASS})

        url = ul.get(cls.SONG_URL_PROP)

        id_parts = url.split('/')
        song_id = id_parts[4] if len(id_parts) > 4 else None

        title_item = ul.find('li', {'class': cls.SONG_TITLE_CLASS})
        title = capwords(title_item.text) if title_item else None

        artist_item = ul.find('li', {'class': cls.SONG_ARTIST_CLASS})
        artist = capwords(artist_item.text) if artist_item else None

        bit_rate = ul.find('li', {'class': cls.SONG_BIT_RATE_CLASS}).text
        bit_rate_parts = bit_rate.split()
        bit_rate = bit_rate_parts[0] if bit_rate_parts else None

        length = ul.find('li', {'class': cls.SONG_LENGTH_CLASS}).text
        length = Song.get_length_from_string(length)

        song_dict = {
            'song_id': song_id,
            'title': title,
            'artist': artist,
            'bit_rate': bit_rate,
            'length': length,
            'url': url
        }

        return Song(**song_dict)


class GoearEngine(object):
    DOWNLOAD_URL = 'http://www.goear.com/action/sound/get/{song_id}'
    PLAYER_SONG_URL = 'http://www.goear.com/playersong/{song_id}'
    PLAY_URL = 'http://www.goear.com/listen/{song_id}'

    CHUNK_SIZE = 1024

    @classmethod
    def download(cls, song, destination_folder=''):

        song_iter = cls.__download_iter(song)
        song_path = os.path.join(destination_folder, song.file_name)
        with open(song_path, 'wb') as f:
            for block in song_iter:
                f.write(block)

    @classmethod
    def __download_iter(cls, song):
        song_iter = cls.get_song_response(song.song_id)

        if not song_iter.ok:
            raise SongNotFoundError()

        return song_iter.iter_content(cls.CHUNK_SIZE)

    @classmethod
    def __get_sesssion(cls):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:38.0) Gecko/20100101 Firefox/38.0',
            'Referer': 'http://www.goear.com/npla/swf/soundmanager2_flash9.swf',
        })

        return session

    @classmethod
    def get_song_response(cls, song_id):
        session = cls.__get_sesssion()

        play_url = cls.PLAY_URL.format(song_id=song_id)
        session.get(play_url)

        player_song_url = cls.PLAYER_SONG_URL.format(song_id=song_id)
        session.get(player_song_url)

        download_url = cls.DOWNLOAD_URL.format(song_id=song_id)
        return session.get(download_url, stream=True)
