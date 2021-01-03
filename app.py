#! /usr/bin/python

from flask import Flask, request, url_for, session, redirect 
import spotipy 
from spotipy.oauth2 import SpotifyOAuth
import json

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

@app.route('/getTracks')
def getTracks():
    return "Some Tracks"

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = client.get("spotify_client_id"),
        client_secret = client.get("spotify_secret_key"),
        redirect_uri = url_for('redirectPage', _external = True),
        scope = "user-library-read"
    )