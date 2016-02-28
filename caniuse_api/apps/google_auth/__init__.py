from flask_oauth import OAuth


def get_auth_client(config):

    client_id = config.get('GOOGLE_CLIENT_ID', '')
    client_secret = config.get('GOOGLE_CLIENT_SECRET', '')

    oauth = OAuth()
    google = oauth.remote_app(
        'google',
        base_url='https://www.google.com/accounts/',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        request_token_url=None,
        request_token_params={
            'scope': 'https://www.googleapis.com/auth/userinfo.email',
            'response_type': 'code'
        },
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_method='POST',
        access_token_params={'grant_type': 'authorization_code'},
        consumer_key=client_id,
        consumer_secret=client_secret
    )
    return google
