from flask import url_for, session, redirect
from flask import Blueprint, current_app
from caniuse_api.apps.google_auth import get_auth_client
from caniuse_api.apps.google_auth.model import User, TokenInvalid


def get_google_auth_blueprint(config):

    google = get_auth_client(config)

    gauth_blueprint = Blueprint(
        'google_auth',
        __name__,
        template_folder='templates'
    )

    @gauth_blueprint.route('/get-token')
    def get_token():
        access_token = session.get('access_token')
        if access_token is None:
            return redirect(url_for('google_auth.login'))
        access_token = access_token[0]
        user = User()
        try:
            resp = user.load(access_token)
        except TokenInvalid:
            session.pop('access_token', None)
            return redirect(url_for('google_auth.login'))
        return resp

    @gauth_blueprint.route('/login')
    def login():
        callback = url_for('google_auth.authorized', _external=True)
        return google.authorize(callback=callback)

    @gauth_blueprint.route('/callback')
    @google.authorized_handler
    def authorized(resp):
        access_token = resp['access_token']
        session['access_token'] = access_token, ''
        session['api_token'] = current_app.config.get('TOKEN')
        return redirect(url_for('main_blueprint.login'))

    @google.tokengetter
    def get_access_token():
        return session.get('access_token')

    return gauth_blueprint
