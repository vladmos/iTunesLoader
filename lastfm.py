import urllib
import tempfile
try:
    from json import loads as json_loads
except ImportError:
    from simplejson import loads as json_loads

from config import LASTFM_API_KEY as API_KEY

API_URL = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&format=json&%s'


class TempStorage(object):
    def __init__(self):
        self._storage = {}

    def __getitem__(self, item):
        return self._storage[item]

    def __setitem__(self, key, value):
        handle, file_name = tempfile.mkstemp()
        with open(file_name, 'w') as f:
            f.write(value)
        self._storage[key] = file_name

    def __contains__(self, item):
        return item in self._storage

cover_art_storage = TempStorage()


def get_cover_art(artist, album):
    if (artist, album) not in cover_art_storage:

        url = API_URL % urllib.urlencode({
            'api_key': API_KEY,
            'artist': artist,
            'album': album,
        })

        request = urllib.urlopen(url)
        json = request.read()
        data = json_loads(json)

        images = data['album'].get('image', [])

        for image in images:
            if image['size'] == 'large':
                image_url = image['#text']
                break
        else:
            return

        image_request = urllib.urlopen(image_url)
        cover_art_storage[artist, album] = image_request.read()

    return cover_art_storage[artist, album]
