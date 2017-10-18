import sys

import spotipy
import spotipy.util as util
from spotipy.client import SpotifyException


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Usage: %s username" % (sys.argv[0],))
    sys.exit()


def user_top_artists(limit=10, ranges=['short_term']):
    result = []

    try:
        for range in ranges:
            print "range:", range
            results = sp.current_user_top_artists(time_range=range, limit=limit)
            for i, item in enumerate(results['items']):
                print i, item['name'], '//', item['id']
                result.append(item['id'])
            print
    except SpotifyException as e:
        print "ERROR! {}".format(e)

    return result

def artists_similar_artists(artist_ids):
    result = []

    try:
        for artist_id in artist_ids:
            results = sp.artist_related_artists(artist_id)
            for similar_artist in results['artists'][:3]:
                print similar_artist['name'] , '//', similar_artist['id']
                result.append(similar_artist['id'])
    except SpotifyException as e:
        print "ERROR! {}".format(e)

    return result

def artists_top_tracks(artists, limit=3):
    result = []

    try:
        for artist_id in artists:
            results = sp.artist_top_tracks(artist_id)
            if len(results['tracks']) > limit:
                tracks = results['tracks'][:limit]
            for track in tracks:
                print track['name'] , '//', track['id']
                result.append(track['id'])
    except SpotifyException as e:
        print "ERROR! {}".format(e)

    return result

def create_playlist(track_ids):

    try:
        import datetime
        today = datetime.date.today()
        playlist_name = str(today)
        new_playlist = sp.user_playlist_create(username, playlist_name)
        sp.user_playlist_add_tracks(username, new_playlist['id'], track_ids)
    except SpotifyException as e:
        print "ERROR! {}".format(e)

if __name__ == '__main__':
    scope = 'user-top-read playlist-modify-public'
    token = util.prompt_for_user_token(username, scope)
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        #ranges = ['short_term', 'medium_term', 'long_term'] could be used to find top artists
        top_artists_ids = user_top_artists()
        similar_artists = artists_similar_artists(top_artists_ids)
        top_tracks_ids =  artists_top_tracks(similar_artists)
        create_playlist(top_tracks_ids)
    else:
        print("Can't get token for", username)
