#! /usr/bin/python

from flask import Flask, request, url_for, session, redirect, jsonify
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import json
import time
import pandas as pd
from SpotifyPlaylistByGenre import SpotifyPlaylistByGenre

# Get Secret Tokens Needed
keys = json.load(open("client_secret.json"))
client = {
    "flask_secret_key": keys["flask_secret_key"],
    "flask_session_cookie": keys["flask_session_cookie"],
    "spotify_client_id": keys["spotify_client_id"],
    "spotify_secret_key": keys["spotify_secret_key"]
}

app = Flask(__name__)
app.secret_key = client.get("flask_secret_key") # Random Key Used For Signing Session Key
app.config["SESSION_COOKIE_NAME"] = client.get("flask_session_cookie")
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external = True))

# Useful Keys That Are Generated From Saved Tracks
    # items['added_at']
    # items['external_urls']['uri']
    # items['external_urls']['name']

@app.route('/getTracks')
def getTracks():
    token_info = ""
    try:
        token_info = get_token()
    except:
        print("User Not Logged In")
        return redirect("/")

    sp = SpotifyPlaylistByGenre(spotipy.Spotify(auth=token_info['access_token']))
    return sp.get_tracks_deprecated()
    
# Check if Access Token is Expired .. if so Generate Refresh Token and make sure there is token data

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if token_info is None:
        raise "exception"

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.requests_timeout(token_info['refresh_token'])
    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = client.get("spotify_client_id"),
        client_secret = client.get("spotify_secret_key"),
        redirect_uri = url_for('redirectPage', _external = True),
        scope = "user-library-read"
    )