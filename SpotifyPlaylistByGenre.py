#! /usr/bin/python

import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
import pandas as pd

CSV_FILE = "tracks.csv"

class SpotifyPlaylistByGenre:
    def __init__(self, spotify_client):
        self.sp_client = spotify_client
        self.csv_file = CSV_FILE # majority of recurrent requests will be using this file
    
    # ITERACTING WITH SPOTIFY API

    # Do Actual Calls .. Function is Abstracted to Fully Utilize 
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

            return str(len(all_songs))

        else:
            iter = 0
            items = func(limit, offset = iter * 50)['items']
            print(items)
            return items

    def get_tracks_deprecated(self, limit = None, offset = None):
        items = self._handle_calls(self.sp_client.current_user_saved_tracks)
        return str(items)

    # Get Tracks (optional lizit, offset parameter .. no args => default all)
    def get_user_tracks(self, limit = None, offset = None):
        pass

    # Getting Artists
    def get_user_artists(self, limit = None, offset = None):
        pass

    # Check What Playlists Are Currently Saved For the User
    def get_current_genre_playlists(self):
        pass

    # ITERACTING WITH DB "CSV"

    # Pull tracks from db and compare modification time of songs
    def pull_tracks_from_db(self):
        pass




    

    

    