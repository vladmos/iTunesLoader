import urllib
import tempfile
try:
    from json import loads as json_loads
except ImportError:
    from simplejson import loads as json_loads

import requests

from config import LASTFM_API_KEY as API_KEY

API_URL = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&format=json&%s'


def _get_coverart(data):
    images = data['album'].get('image', [])

    for image in images:
        if image['size'] == 'large':
            image_url = image['#text']
            image = requests.get(image_url).content
            return image


def get_album_coverart(artist, album):
    url = API_URL % urllib.urlencode({
        'api_key': API_KEY,
        'artist': artist,
        'album': album,
    })

    data = requests.get(url).json()

    image = _get_coverart(data)
    if image:
        handle, image_file_name = tempfile.mkstemp(suffix='.jpg')
        with open(image_file_name, 'w') as f:
            f.write(image)
        return image_file_name
