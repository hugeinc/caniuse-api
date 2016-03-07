from flask import Blueprint, render_template
from flask import session, g, redirect, url_for
from caniuse_api.apps.caniuse_proxy.service import FeatureService
from caniuse_api.apps.core.auth import get_api_token, logout_user
from caniuse_api.apps.google_auth.model import User, TokenInvalid

main_blueprint = Blueprint(
    'main_blueprint',
    __name__,
    template_folder='templates'
)


@main_blueprint.route('/')
def index():
    api_token = get_api_token()
    user = g.user
    features = FeatureService.get_instance()
    feature_slugs = features.qp.valid_slugs
    return render_template(
        'index.html',
        token=api_token,
        user=user,
        feature_slugs=feature_slugs
    )


@main_blueprint.route('/login')
def login():
    api_token = get_api_token()
    user = g.user
    return render_template(
        'login.html',
        token=api_token,
        user=user
    )


@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_blueprint.index'))


@main_blueprint.before_request
def before_request():
    g.user = None
    if 'access_token' in session:
        user = User()
        try:
            user.load(session['access_token'][0])
            g.user = user
        except TokenInvalid:
            pass
