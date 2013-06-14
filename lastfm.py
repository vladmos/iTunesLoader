import urllib
import tempfile
import re
try:
    from json import loads as json_loads
except ImportError:
    from simplejson import loads as json_loads

from config import LASTFM_API_KEY as API_KEY

API_URL = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&format=json&%s'
YEAR_REGEX = re.compile(r'^.*[^\d]([\d]{4})[^\d].*$')


class DataStorage(object):
    def __init__(self):
        self._storage = {}

    def __contains__(self, item):
        return item in self._storage

    def get(self, artist, album):
        return self._storage[artist, album]

    def store(self, artist, album, year, image):
        image_file_name = None
        if image:
            handle, image_file_name = tempfile.mkstemp(suffix='.jpg')
            with open(image_file_name, 'w') as f:
                f.write(image)
        self._storage[artist, album] = (year, image_file_name)


data_storage = DataStorage()


def _get_release_year(data):
    year = data['album']['releasedate']
    year_match = YEAR_REGEX.match(year)
    if year_match:
        return year_match.group(1)


def _get_coverart_url(data):
    images = data['album'].get('image', [])

    for image in images:
        if image['size'] == 'large':
            return image['#text']


def get_album_data(artist, album):
    if (artist, album) not in data_storage:

        url = API_URL % urllib.urlencode({
            'api_key': API_KEY,
            'artist': artist,
            'album': album,
        })

        request = urllib.urlopen(url)
        json = request.read()
        data = json_loads(json)

        year = _get_release_year(data)
        image_url = _get_coverart_url(data)

        image = None
        if image_url:
            image_request = urllib.urlopen(image_url)
            image = image_request.read()

        data_storage.store(artist, album, year, image)

    return data_storage.get(artist, album)
