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

SPOTIFY_PLAYLIST_NAMES_DICT = {
    "Pop": [],
    "Hip Hop": [],
    "Country": [],
    "R&B": [],
    "Worship": [],

}

SPOTIFY_PLAYLIST_NAMES = [
    'pop',
    'jazz',
    'hip hop',
]

class SpotifyPlaylistByGenre:
    def __init__(self, spotify_client):
        self.sp_client = spotify_client
        self.songs_csv_file = SONGS_CSV_FILE # majority of recurrent requests will be using this file
        self.playlists_csv_file = PLAYLISTS_CSV_FILE
        self.albums_csv_file = ALBUMS_CSV_FILE
        self.artists_csv_file = ARTISTS_CSV_FILE
        self.user_id = self.sp_client.current_user()['id']

        self.playlist_names = []
        self.all_playlist_objs = []
        self.get_current_user_playlists() # Fill All Genre Objects

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
            return items

    def get_tracks_deprecated(self, limit = None, offset = None):
        items = self._handle_calls(self.sp_client.current_user_saved_tracks)
        return str(items)

    # Get Tracks (optional lizit, offset parameter .. no args => default all)
    def get_all_user_tracks(self, limit = None, offset = None):

        track_objs = []
        artists_ids = set() # Represents Artists IDS
        artists_ids_dict = dict() # Same as above but stores in format Artist Name : Artist ID
        all_genres = set()
        all_artists_songs = list() # Main Object
        all_art_songs = dict()

        # Structure of All Artists Songs
        #           List Format
        # [

        #    {
        #        "name_of_artist": "name",
        #        "artist_id": "artist_id",
        #        "genres": [list of genres],
        #        "songs": [list of songs]
        #    },
        #    {
        #        "name_of_artist": "name",
        #        "artist_id": "artist_id",
        #        "genres": [list of genres],
        #        "songs": [list of songs]
        #    },

        # ]

        #           Dict Format (PREFERRED)
        # {
        #   "artist_id" : {
        #                   "name_of_artist": "name", 
        #                   "genres": [list of genres],
        #                   "songs": [list of songs]
        #                 },

        #   "artist_id" : {
        #                   "name_of_artist": "name", 
        #                   "genres": [list of genres],
        #                   "songs": [list of songs]
        #                 }
        # }

    
        # First .... ALL LIKED SONGS
        all_liked_songs = self._handle_calls(self.sp_client.current_user_saved_tracks, limit=10) # All Liked Songs

        # Album: "album" => album object "dictionary"
        # Artist: "artists" => artist object "dictionary"
        # Name: "name" => str
        # URI : "uri" => str
        # ID : "id" => str
        # HREF: "href" => str
        """
        # Loop through all songs for artist
        for song in all_liked_songs[:30]:

            track_id = song["track"]["id"] # Get ID for Track
            track_name = song["track"]["name"] # Get Name of Track

            for artist in song["track"]["artists"]:

                # Check If Artist Already Has Dictionary Created for Him/Her .. if so, all we have to do is add song to songs of artist_id
                artist_id = artist["id"]
                
                # New Artists -> Need to Create Dictionary for Artist
                if artist_id not in all_art_songs:

                    idv_artist = dict()

                    # Extract Relevant Information for Artist
                    artist_name = artist["name"]
                    artist_genres = self.sp_client.artist(artist["id"])["genres"] # Get List of Genres for Artists

                    # Update IDV Object
                    idv_artist["name"] = artist["name"]
                    idv_artist["genres"] = artist_genres
                    #idv_artist["songs"] = [track_id]
                    idv_artist["songs"] = {
                        track_name : track_id
                    }

                    all_art_songs[artist_id] = idv_artist # Create and Assign New Dict

                    # Update Outer Variables 
                    artists_ids.add(artist["id"]) # Add Artists ID to global set of Artists ID just in case becomes handy in the future
                    artists_ids_dict[artist_name] = artist_id
                    all_genres.update(artist_genres) # Update Global List to Keep Track of All Genres

                # Already Existing Artists -> Dict Already Exists Just Need to Add Current Song to Artist Songs
                else:
                    idv_artist["songs"].update({
                        track_name: track_id
                    })

                break # Only care about first artist , primary artist so continue on to next song (could use [0] instead but nah)
        """

        # Second All Albums
        all_albums = self._handle_calls(self.sp_client.current_user_saved_albums, limit=1) # All Album Objects

        album_ids = set()
        album_names = set()
        album_uris = set()
        for album in all_albums:
            
            album_id = album["album"]["id"]
            album_ids.add(album_id)

            album_name = album["album"]["name"]
            album_names.add(album_name)

            album_uri = album["album"]["uri"]
            album_uris.add(album_uri)

            # Now time for the fun part, tracks



            break

        # Name of Song, Artist, Album
        
        return str(all_liked_songs)

    def create_playlist(self, list_of_tracks, playlist_name):
        # user_playlist_create -> Creating Playlist

        # user_playlist_add_tracks -> Adding Tracks to Playlist

        pass

    # Getting Artists
    def get_user_artists(self, limit = None, offset = None):
        pass

    # Check What Playlists Are Currently Saved For the User
    #   Want Dictionary To Get List of Genres By Name
    # ['items'] is default for actual values
    def get_current_user_playlists(self):

        entire_playlist_obj = self.sp_client.current_user_playlists()['items']

        # Iterate through all items returned from function call
        # Saving all for future-proofs safe but only care about genres for now
        for item in entire_playlist_obj:
            del item["images"]

        self.all_playlist_objs = entire_playlist_obj
        self.playlist_names = [ item["name"] for item in entire_playlist_obj ]
        
    # Simple Getters
    def get_playlist_names(self):
        return str(self.playlist_names)

    def get_playlist_objs(self):
        return str(self.all_playlist_objs)




    # ITERACTING WITH DB "CSV"

    # Pull tracks from db and compare modification time of songs
    def pull_tracks_from_db(self):
        pass




    

    

    