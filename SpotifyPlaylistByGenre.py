#! /usr/bin/python

import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
import pandas as pd

SONGS_CSV_FILE = "songs.csv"
PLAYLISTS_CSV_FILE = "playlists.csv"
ALBUMS_CSV_FILE = "albums.csv"
ARTISTS_CSV_FILE = "artists.csv"

class SpotifyPlaylistByGenre:
    def __init__(self, spotify_client):
        self.sp_client = spotify_client
        self.songs_csv_file = SONGS_CSV_FILE # majority of recurrent requests will be using this file
        self.playlists_csv_file = PLAYLISTS_CSV_FILE
        self.albums_csv_file = ALBUMS_CSV_FILE
        self.artists_csv_file = ARTISTS_CSV_FILE

        self.genre_names = []
        self.all_genre_objs = []

    # ITERACTING WITH SPOTIFY API

    # Do Actual Calls .. Function is Abstracted to Fully Utilize D.R.Y
    # Majority of Spotify API return in array format
    def _handle_calls(self, func, limit = None, offset = None):
        
        if limit is None:
            # Doing All and Iterating Through

            all_songs = []
            iter = 0

            while True:
                items = func(limit = 50, offset = iter * 50)['items']
                iter += 1
                all_songs += items

                if len(items) < 50:
                    break

            return all_songs

        else:
            iter = 0
            items = func(limit, offset = iter * 50)['items']
            print(items)
            return items

    def get_tracks_deprecated(self, limit = None, offset = None):
        items = self._handle_calls(self.sp_client.current_user_saved_tracks)
        return str(items)

    # Get Tracks (optional lizit, offset parameter .. no args => default all)
    def get_all_user_tracks(self, limit = None, offset = None):
        pass

    # Getting Artists
    def get_user_artists(self, limit = None, offset = None):
        pass

    # Check What Playlists Are Currently Saved For the User
    #   Want Dictionary To Get List of Genres By Name
    # ['items'] is default for actual values
    def get_current_user_genre_playlists(self):

        genres_names = []
        entire_playlist_obj = self.sp_client.current_user_playlists()['items']

        # Iterate through all items returned from function call
        # Saving all for future-proofs safe but only care about genres for now
        for playlist in entire_playlist_obj:
            
            name = playlist['name'] # Str
            desc = playlist['description'] # Str
            id = playlist['id'] # Str
            href = playlist['href'] # Str

            # Returns Dictionary
            # "display_name" => str
            # "external_urls" => dictionary
            #       "spotify" => str
            #  "href" => str
            # "id" => str
            # "type" => str
            # "uri" => str
            owner = playlist['owner'] # Dictionary -> "display_name", "exter"
            
            public = playlist["public"] # Str
            snapshot_id = playlist["snapshot_id"] # Str

            # Returns Dictionary
            # "href" => str
            # "total" => int
            tracks = playlist["tracks"] # Dictionary
            uri = playlist["uri"] # Str
            external_urls = playlist["external_urls"]

            del playlist["images"]
            self.all_genre_objs.append(playlist)
        
            genres_names.append(name)

        return str(self.all_genre_objs)

    # ITERACTING WITH DB "CSV"

    # Pull tracks from db and compare modification time of songs
    def pull_tracks_from_db(self):
        pass




    

    

    