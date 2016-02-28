from flask import Blueprint, render_template, session
from caniuse_api.apps.caniuse_proxy.service import FeatureService
from caniuse_api.apps.core.auth import get_api_token

main_blueprint = Blueprint(
    'main_blueprint',
    __name__,
    template_folder='templates'
)


@main_blueprint.route('/')
def index():
    api_token = get_api_token()
    features = FeatureService.get_instance()
    feature_slugs = features.qp.valid_slugs
    return render_template(
        'index.html',
        token=api_token,
        feature_slugs=feature_slugs
    )


@main_blueprint.route('/auth-token')
def auth_token():
    api_token = get_api_token()
    return render_template(
        'auth-token.html',
        token=api_token
    )
