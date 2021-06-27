# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 18:25:39 2020

@author: adamp
"""

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

#SPOTIPY_CLIENT_ID = "2550571af39c4045892ab8f88fb8025b"
#SPOTIPY_CLIENT_SECRET = "edfa5eaa25754de79c44c36b19ddaf18"

# Ger the username from the terminal
username = "1227414957"
#sys.argv[1]
#1227414957
# https://open.spotify.com/user/1227414957?si=OQ1YwCARR52vr6fCCsG0HQ
#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
# artist name
# artist id
# artist popularity
# artist genre
#artist_ = spotify.artist(uri)

# artist id under artists list>dict>id
# album release date
# album id
# album name
# there are several dups due to Japan releases
#artist_albums_ = spotify.artist_albums(uri, album_type = 'album')

#album_uri = []
#album_name = []
#for i, album in enumerate(artist_albums_['items']):
 #   print(i)
#    album_uri.append(album['uri'])
  #  album_name.append(album['name'])

# I can get all of the above from artist_top_tracks
# artist top ten tracks by country
# artist id under artists list>dict>id
# song duration = duration_ms
# song id
# song popularity
# song name
# Himmelsrand = 7ldJhE5mB9ukNh3OjuX85T
    
# create a spotify object with the connection
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
#sp = spotipy.Spotify(auth=token)
# Adam Curry's username
username = "1227414957"

"""
Get the user's total playlist population
"""
playlists = spotify.user_playlists(username)

playlist_tracks = []

"""
for loop to appendeach playlist to a list object
"""
for playlist in playlists['items']:
    playlist_tracks.append(spotify.user_playlist_tracks
                           (username,playlist_id=playlist['uri']))

playlist_data = []
"""
For loop will append each track from a user's total public playlists to a dict
"""
for plist in playlist_tracks:
    try:
        for i in plist['items']:
            plist_dict = {
            'playlist_track_name' : None,
            'playlist_album_name' : None,
            'playlist_album_uri' : None,
            'playlist_track_popularity' : None,
            'playlist_track_duration' : None,
            'track_uri' : None,
            'playlist_artist_name' : None,
            'playlist_artist_uri' : None
            }
            try:
                plist_dict['playlist_track_name'] = (i['track']['name'])#track name
                plist_dict['playlist_album_name'] = (i['track']['album']['name'])#album name
                plist_dict['playlist_album_uri'] = (i['track']['album']['uri'])
                plist_dict['playlist_track_popularity'] = (i['track']['popularity'])
                plist_dict['playlist_track_duration'] = (i['track']['duration_ms'])
                plist_dict['track_uri'] = (i['track']['uri'])
                plist_dict['playlist_artist_name'] = (i['track']['artists'][0]['name'])
                plist_dict['playlist_artist_uri'] = (i['track']['artists'][0]['uri'])
                playlist_data.append(plist_dict)
            except Exception as ee:
                print(ee)+'inner'
                continue
    except Exception as e:
        print(e)
        continue

"""
from the population of the playlist tracks, get the track featers from spotify
"""
audio_features_ = []
for track in playlist_data:
    audio_features_.append(spotify.audio_features(track['playlist_track_uri']))

"""
For loop will append each track's audio features to a dict
"""
track_data = []
for i, t in enumerate(audio_features_):
    track_dict = {
        'track_uri' : None,
        'acousticness' : None,
        'danceability' : None,
        'energy' : None,
        'instrumentalness' : None,
        'key' : None,
        'liveness' : None,
        'loudness' : None,
        'speechiness' : None,
        'tempo' : None,
        'time_signature' : None,
        'valence' : None
        }
    try:
        track_dict['track_uri'] = (t[0]['uri'])
        track_dict['acousticness'] = (t[0]['acousticness'])
        track_dict['danceability'] = (t[0]['danceability'])
        track_dict['energy'] = (t[0]['energy'])
        track_dict['instrumentalness'] = (t[0]['instrumentalness'])
        track_dict['key'] = (t[0]['key'])
        track_dict['liveness'] = (t[0]['liveness'])
        track_dict['loudness'] = (t[0]['loudness'])
        track_dict['speechiness'] = (t[0]['speechiness'])
        track_dict['tempo'] = (t[0]['tempo'])
        track_dict['time_signature'] = (t[0]['time_signature'])
        track_dict['valence'] = (t[0]['valence'])
        track_data.append(track_dict)
    except Exception:
        pass   
# this function will get the audio analysis, more song related data
#audio_analysis_ = spotify.audio_analysis(Himmelsrand)


df_track_data = pd.DataFrame(track_data)
df_playlist_data = pd.DataFrame(playlist_data)

df_playlist_data = df_playlist_data.rename(columns={'playlist_track_uri': 'track_uri'})

df_final = df_track_data.merge(df_playlist_data,how='inner',on='track_uri')

df_final.head(5)






