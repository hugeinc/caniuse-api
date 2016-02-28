from flask import jsonify, Blueprint, render_template
from caniuse_api.apps.caniuse_proxy.service import FeatureService
main_blueprint = Blueprint(
    'main_blueprint',
    __name__,
    template_folder='templates'
)


@main_blueprint.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@main_blueprint.route('/')
def index():
    features = FeatureService.get_instance()
    feature_slugs = features.qp.valid_slugs
    return render_template(
        'index.html',
        feature_slugs=feature_slugs
    )
