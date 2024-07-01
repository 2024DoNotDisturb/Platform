from flask_oauthlib.client import OAuth
from flask import current_app

oauth = OAuth()

def init_google_oauth(consumer_key, consumer_secret):
    global google
    google = oauth.remote_app(
        'google',
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        request_token_params={'scope': 'email'},
        base_url='https://www.googleapis.com/oauth2/v1/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
    )
    return google
