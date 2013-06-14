from .lastfm import get_album_coverart
from .discogs import get_album_data
from .utils import CaseInsensitiveDict


class Album(object):
    def __init__(self, year, cover_art_file_name, track_list):
        self.year = year
        self.cover_art_file_name = cover_art_file_name
        self.track_list = track_list


class AlbumStorage(object):
    def __init__(self):
        self._storage = CaseInsensitiveDict()

    def __contains__(self, item):
        return item in self._storage

    def get(self, artist_name, album_name):
        return self._storage[artist_name, album_name]

    def store(self, artist_name, album_name, year, image_file_name, track_list):
        self._storage[artist_name, album_name] = Album(year, image_file_name, track_list)


ALBUM_STORAGE = AlbumStorage()


class TrackInfo(object):
    def __init__(self, artist_name, album_name, track_name):
        if (artist_name, album_name) not in ALBUM_STORAGE:
            cover_art_file_name = get_album_coverart(artist_name, album_name)
            year, track_list = get_album_data(artist_name, album_name)
            ALBUM_STORAGE.store(artist_name, album_name, year, cover_art_file_name, track_list)

        album = ALBUM_STORAGE.get(artist_name, album_name)
        track = album.track_list.get_track(track_name)

        self.track_index = track.index
        self.cd_index = track.cd_index
        self.track_name = track.name
        self.cd_track_count = album.track_list.get_cd_track_count(self.cd_index)
        self.cd_count = album.track_list.cd_count
        self.cover_art_file_name = album.cover_art_file_name
        self.year = album.year
