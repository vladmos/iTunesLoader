import urllib
import tempfile

import requests

from config import LASTFM_API_KEY as API_KEY

API_URL = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&format=json&%s'


def _get_coverart(data):
    images = data['album'].get('image', [])

    for image in images:
        if image['size'] == 'extralarge':
            image_url = image['#text']
            suffix = image_url.split('.')[-1].lower()
            image = requests.get(image_url).content
            return image, suffix


def get_album_coverart(artist, album):
    url = API_URL % urllib.urlencode({
        'api_key': API_KEY,
        'artist': artist.encode('utf-8'),
        'album': album.encode('utf-8'),
    })

    data = requests.get(url).json()

    image, suffix = _get_coverart(data)
    if image:
        handle, image_file_name = tempfile.mkstemp(suffix='.%s' % suffix)
        with open(image_file_name, 'w') as f:
            f.write(image)
        return image_file_name
