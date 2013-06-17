import discogs_client

from .utils import CaseInsensitiveDict, simplify

discogs_client.user_agent = 'iTunesLoader +https://github.com/vladmos/iTunesLoader'

ARTISTS = CaseInsensitiveDict()


def _equal_name(db_name, name):
    return simplify(db_name) == simplify(name)


class Track(object):
    def __init__(self, name, index, cd_index):
        self.name = name
        self.index = index
        self.cd_index = cd_index

    def __repr__(self):
        return 'Track(%s, %s, %s)' % (repr(self.name), self.index, self.cd_index)


class TrackList(object):
    def __init__(self, tracklist):
        self._tracks = CaseInsensitiveDict()
        self.cd_count = 0
        self._tracks_count = {}

        for i, track in enumerate(tracklist):
            position = track['position']
            if '-' in position:
                cd_index, track_index = tuple(map(int, position.split('-')))
            elif position and position.isdigit():
                cd_index, track_index = 1, int(position)
            else:
                cd_index, track_index = 1, i + 1

            self.cd_count = max(cd_index, self.cd_count)
            self._tracks_count[cd_index] = max(track_index, self._tracks_count.get(cd_index, 0))
            self._tracks[track['title']] = Track(track['title'], track_index, cd_index)

    def get_track(self, track_name):
        return self._tracks.get_closest(track_name) or Track(None, None, None)

    def get_cd_track_count(self, cd_index):
        return self._tracks_count.get(cd_index, None)


def get_album_data(artist_name, album_name):
    if artist_name not in ARTISTS:
        ARTISTS[artist_name] = CaseInsensitiveDict()
        print 'Fetching info about %s' % artist_name
        search_data = discogs_client.Search(artist_name)
        search_results = list(search_data.exactresults)
        print 'Found %s candidates' % len(search_results)
        for artist_data in search_results:
            releases = list(artist_data.releases)
            print 'Found %s releases for %s' % (len(releases), artist_data.name)
            for release in releases:
                print 'Fetching album %s - %s' % (artist_data.name, album_name)
                ARTISTS[artist_name][release.title] = release

    release = ARTISTS[artist_name].get_closest(album_name)
    if release:
        year = release.data['year']
        track_list = TrackList(release.data['tracklist'])
        return year, track_list

    return None, TrackList([])
