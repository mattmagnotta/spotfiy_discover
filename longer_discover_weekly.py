import sys
import argparse
import random
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


def get_related_artists(artists):


    artist_related_artists_list = []

    for artist in artists:
        artist_name = artist
        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        result = sp.search(q='artist:' + artist_name, type='artist')

        try:
            name = result['artists']['items'][0]['name']
            uri = result['artists']['items'][0]['uri']

            related = sp.artist_related_artists(uri)

            for artist in related['artists']:
                artist_related_artists_list.append(artist['name'])
        except BaseException:
            print("usage show_related.py [artist-name]")

    return artist_related_artists_list


def get_artist_top_tracks(artists):
    random_artist_list = random.sample(artists, 100)
    top_tracks_list = []

    for artist in random_artist_list:
        artist_name = artist

        client_credentials_manager = SpotifyClientCredentials()
        sp = spotipy.Spotify(
            client_credentials_manager=client_credentials_manager)
        result = sp.search(q='artist:' + artist_name, type='artist')
        try:
            name = result['artists']['items'][0]['name']
            uri = result['artists']['items'][0]['uri']

            related = sp.artist_related_artists(uri)

        except BaseException:
            print("usage show_related.py [artist-name]")
        artist_top_track = sp.artist_top_tracks(uri)
        for track in artist_top_track['tracks'][:1]:
            top_tracks_list.append(track['uri'])
    
    return top_tracks_list
#
def create_playlist(sp,tracks):

    print('Creating Playlist...')
    user_id = sp.me()['id']

    playlist = sp.user_playlist_create(user_id, sys.argv[2])
    playlist_uri = playlist['uri']
    print('Playlist Created...')



    sp.playlist_add_items(playlist_uri, tracks)



if __name__ == '__main__':
    scope = 'user-library-read playlist-read-private playlist-modify '

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        print('Aquiring data for your playlist...')
        artists = []
        for item in results['items']:
            track = item['track']
            artists.append(track['artists'][0]['name'])
    else:
        print("Can't get token for", username)

    get_related_artists(artists)
    get_artist_top_tracks(get_related_artists(artists))
    create_playlist(sp,get_artist_top_tracks(get_related_artists(artists)))
